import redis
import logging
import time

#############################################################################
#############################################################################
#############################################################################
# Description:
# A simple procedure to extract data from the cache. The procedure is applicable inside a feature collector to
# extract values of a selected determinant factor (attributes) at the offer and at the trip leg level.
#
# Inputs:
#
# pa_cache - cache identifier
# pa_request_id - request id for which the data should be extracted from cache
# pa_offer_level_items - list of attributes at the offer level that should be extracted from the cache
# pa_tripleg_level_items -  list of attributes at the trip leg level that should be extracted from the cache
#
# Outputs:
#
# output_offer_level_items - dictionary containing values of requested attributed at the offer level. It contains
#                            a list of offer identifiers named "offer_ids" and dictionaries containing values of
#                            requested attributes identified by offer id
# output_tripleg_level_items - dictionary containing values of requested attributed at the trip leg level. For each
#                              offer id it contains a list of trip leg identifiers named "trip legs" and dictionaries
#                              containing values of requested attributes identified by composite keys
def extract_data_from_cache(
        # cache identifier
        pa_cache,
        # request id for which the data should be extracted from cache
        pa_request_id,
        # TODO add list of attributes at the request level?
        # pa_request_level_items,
        # list of attributes at the offer level that should be extracted from the cache
        pa_offer_level_items,
        # list of attributes at the trip leg level that should be extracted from the cache
        pa_tripleg_level_items):

    output_offer_level_items   = {}
    output_tripleg_level_items = {}

    offer_ids = pa_cache.lrange('{}:offers'.format(pa_request_id), 0, -1)
    output_offer_level_items["offer_ids"] = offer_ids
    pipe = pa_cache.pipeline()
    if offer_ids is not None:
        for offer in offer_ids:
            output_offer_level_items[offer] = {}
            for offer_level_item in pa_offer_level_items:
                # assembly key for offer level
                temp_key  = "{}:{}:{}".format(pa_request_id,offer,offer_level_item)
                # extract offer level data from cache
                if (offer_level_item == "bookable_total") or (offer_level_item == "complete_total"):
                    pipe.hgetall(temp_key)
                else:
                    pipe.get(temp_key)
            # extract information at the trip leg level
            output_tripleg_level_items[offer] = {}
            if len(pa_tripleg_level_items) > 0:
                temp_key      = "{}:{}:legs".format(pa_request_id,offer)
                tripleg_ids  = pa_cache.lrange(temp_key, 0, -1)
                output_tripleg_level_items[offer]["triplegs"] = tripleg_ids
                for tripleg_id in tripleg_ids:
                    output_tripleg_level_items[offer][tripleg_id] = {}
                    for tripleg_level_item in pa_tripleg_level_items:
                        temp_key = "{}:{}:{}:{}".format(pa_request_id, offer, tripleg_id,tripleg_level_item)
                        pipe.get(temp_key)
        temp_data = pipe.execute()
        index = 0
        for offer in offer_ids:
            for offer_level_item in pa_offer_level_items:
                output_offer_level_items[offer][offer_level_item] = temp_data[index]
                index += 1
            if len(pa_tripleg_level_items) > 0:
                tripleg_ids  = output_tripleg_level_items[offer]["triplegs"]
                for tripleg_id in tripleg_ids:
                    for tripleg_level_item in pa_tripleg_level_items:
                        output_tripleg_level_items[offer][tripleg_id][tripleg_level_item] = temp_data[index]
                        index += 1

    return output_offer_level_items, output_tripleg_level_items
#############################################################################
#############################################################################
#############################################################################
# Description:
# Wrapper procedure for reading operation from cache used by feature collectors. Wrapper ensures repeated reading
# attempts when reading from cache is failing. After a certain number of unsuccessful attempts an error is raised.
def read_data_from_cache_wrapper(
        # cache identifier
        pa_cache,
        # request id for which the data should be extracted from cache
        pa_request_id,
        # list of attributes at the offer level that should be extracted from the cache
        pa_offer_level_items,
        # list of attributes at the trip leg level that should be extracted from the cache
        pa_tripleg_level_items):
    retries = 5

    while True:
        try:
            return extract_data_from_cache(pa_cache, pa_request_id, pa_offer_level_items, pa_tripleg_level_items)
        except redis.exceptions.ConnectionError as exc:
            logging.debug("Reading from cache by a feature collector failed. Retries remaining: {}".format(retries))
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.1)
#############################################################################
#############################################################################
#############################################################################
# A simple procedure to store data to the cache.
#
# Inputs:
#
# pa_cache - cache identifier
# pa_request_id - dictionary containing data indexed by offer ids that are supposed to be stored to cache
# pa_data - dictionary containing data indexed by offer ids that are supposed to be stored to cache
# pa_sub_key - subkey (final part of the composite key) that is added to request_id and offer_id under which the data
#              is stored in cache
#
# Outputs:
#
# The procedure returns value 1 if the writing was successful.

def store_simple_data_to_cache(
    # cache identifier
    pa_cache,
    # request id for which the data should be stored to cache
    pa_request_id,
    # dictionary containing data indexed by offer ids that are supposed to be stored to cache
    pa_data,
    # subkey (final part of the composite key) that is added to request_id and offer_id under which the data is stored in cache
    pa_sub_key
):
    pipe = pa_cache.pipeline()
    for offer in pa_data:
        temp_key = "{}:{}:{}".format(pa_request_id,offer,pa_sub_key)
        pipe.set(temp_key, pa_data[offer])
    pipe.execute()
    return 1
#############################################################################
#############################################################################
#############################################################################
# Description:
# Wrapper procedure for writing operation to cache used by feature collectors. Wrapper ensures repeated writing attempts
#  when writing to cache is failing. After a certain number of unsuccessful attempts an error is raised.
def store_simple_data_to_cache_wrapper(
        # cache identifier
        pa_cache,
        # request id for which the data should be stored to cache
        pa_request_id,
        # dictionary containing data indexed by offer ids that are supposed to be stored to cache
        pa_data,
        # subkey (final part of the composite key) that is added to request_id and offer_id under which the data is stored in cache
        pa_sub_key):
    retries = 5

    while True:
        try:
            return store_simple_data_to_cache(pa_cache, pa_request_id, pa_data, pa_sub_key)
        except redis.exceptions.ConnectionError as exc:
            logging.debug("Writing to cache by a feature collector failed. Retries remaining: {}".format(retries))
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.1)
#############################################################################
#############################################################################
#############################################################################