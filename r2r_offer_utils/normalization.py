#!/usr/bin/env python3

from typing import Mapping
import math
import sys

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


if __name__ == '__main__':
    from pprint import pprint
    print("This is an example")

    offers = {'123x': 0.1,
              '234a': 0.2
              }
    pprint(zscore(offers))

    exit(0)
