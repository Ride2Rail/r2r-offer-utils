#!/usr/bin/env python3

from typing import Mapping
import math
import sys
#############################################################################
#############################################################################
#############################################################################
def zscore(offers: Mapping) -> Mapping:
    n          = 0
    sum        = 0.0
    sum_square = 0.0

    for o in offers:
        value = offers[o]
        if value is not None:
            n = n + 1
            sum = sum + value
            sum_square = sum_square + value*value

    z_scores = {}
    if n > 0:
        average = sum / n
        std = math.sqrt(sum_square / n - average * average)
        for o in offers:
            value = offers[o]
            if value is not None:
                if std == 0:
                    z_scores[o] = 0
                else:
                    z_scores[o] = (value - average)/std
    return z_scores
#############################################################################
#############################################################################
#############################################################################
def flipped_zscore(offers: Mapping) -> Mapping:
    z_scores = zscore(offers)
    for id in z_scores:
        value = z_scores[id]
        if value != 0:
            z_scores[id] = 1 - value
    return z_scores
#############################################################################
#############################################################################
#############################################################################
def minmaxscore(offers: Mapping) -> Mapping:

    min = sys.float_info.max
    max = sys.float_info.min
    n   = 0
    for o in offers:
        value = offers[o]
        if value is not None:
            n = n + 1
            if value > max:
                max = value
            if value < min:
                min = value

    minmax_scores = {}
    diff = max - min
    if (diff > 0) and (n > 0):
        for o in offers:
            value = offers[o]
            if value is not None:
                    minmax_scores[o] = (value-min)/diff
    return minmax_scores
#############################################################################
#############################################################################
#############################################################################
def flipped_minmaxscore(offers: Mapping) -> Mapping:
    minmax_scores = minmaxscore(offers)
    for id in minmax_scores:
        value = minmax_scores[id]
        if value != 0:
            minmax_scores[id] = 1 - value
    return minmax_scores
#############################################################################
#############################################################################
#############################################################################
def aggregate_a_quantity_over_triplegs(
        tripleg_ids,
        weights,
        quantity):
    sum        = 0.0
    result     = 0.0
    num_values = 0

    for tripleg_id in tripleg_ids:
        weight = weights[tripleg_id]
        value  = quantity[tripleg_id]
        if (weight is not None):
            sum = sum + weight
            if (value is not None):
                result += weight*value
                num_values += 1
    if (sum > 0)and(num_values > 0):
        result /= sum
    else:
        return None
    return result
#############################################################################
#############################################################################
#############################################################################

if __name__ == '__main__':
    from pprint import pprint
    print("This is an example")

    offers = {'123x': 0.1,
              '234a': 0.2
              }
    pprint(zscore(offers))

    exit(0)
