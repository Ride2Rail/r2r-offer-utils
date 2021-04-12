#!/usr/bin/env python3

from typing import Mapping
import math
import sys
#############################################################################
#############################################################################
#############################################################################
# A procedure implementing calculation of the z-score weights for a determinant factor across all offers
# Inputs:
#
# offers  - dictionary containing values  of a determinant factor, values are identified by offer identifiers as keys
# flipped - binary value indicating whether resulting weights need to be flipped (i.e. subtracted from 1)
#
# Outputs:
#
# z_score - dictionary containing z-score values for a determinant factor, values are identified by offer identifiers as keys

def zscore(offers: Mapping, flipped = False) -> Mapping:
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
                    if not flipped:
                        z_scores[o] = (value - average)/std
                    else:
                        z_scores[o] = 1 - (value - average) / std
    return z_scores
#############################################################################
#############################################################################
#############################################################################
# A procedure implementing calculation of the minmax-score weights for a determinant factor across all offers
# Inputs:
#
# offers  - dictionary containing values  of a determinant factor, values are identified by offer identifiers as keys
# flipped - binary value indicating whether resulting weights need to be flipped (i.e. subtracted from 1)
#
# Outputs:
#
# minmax_score - dictionary containing minmax-score values for a determinant factor, values are identified by offer identifiers as keys

def minmaxscore(offers: Mapping, flipped = False) -> Mapping:

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
    if (n > 0):
        for o in offers:
            value = offers[o]
            if value is not None:
                if(diff > 0):
                    if not flipped:
                        minmax_scores[o] = (value-min)/diff
                    else:
                        minmax_scores[o] = 1 - (value-min)/diff
                else:
                    minmax_scores[o] = 0.5
    return minmax_scores
#############################################################################
#############################################################################
#############################################################################
# A procedure implementing aggregation of values of a determinant factor for an offer over trip legs belonging
# to the offer

# Inputs:
#
# tripleg_ids - array of trip leg identifiers to be aggregated
# weights     - dictionary containing weights identified by keys (trip leg key indentifiers) that are used as weights
#               in the aggregation. Typically, the duration of trip legs is used as a weight.
# quantity    - dictionary containing values of a determinant factor (identified by trip leg indetifiers) to be
#               aggregated
#
# Outputs:
#
# result      - values of a determinant factor aggregated over trip legs
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
