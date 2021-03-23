#!/usr/bin/env python3

from typing import Mapping
import math

def zscore(offers: Mapping) -> Mapping:

    n          = 0
    sum        = 0.0
    sum_square = 0.0

    for o in offers:
        value = offers[o]
        if not(value is None):
            n = n + 1
            sum = sum + value
            sum_square = sum_square + value*value
    average = sum/n
    std     = math.sqrt(sum_square/n - (sum/n)*(sum/n))

    z_scores = {}
    for o in offers:
        value = offers[o]
        if not (value is None):
            z_scores[o] = (value - average)/std
    return z_scores


if __name__ == '__main__':
    from pprint import pprint
    print("This is an example")

    offers = {'123x': 0.1,
              '234a': 0.2
              }
    pprint(zscore(offers))

    exit(0)
