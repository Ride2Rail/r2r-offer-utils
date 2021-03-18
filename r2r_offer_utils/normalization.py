#!/usr/bin/env python3

from typing import Mapping


def zscore(offers: Mapping) -> Mapping:
    # do stuff
    return {o: 0 for o in offers}


if __name__ == '__main__':
    from pprint import pprint
    print("This is an example")

    offers = {'123x': 0.1,
              '234a': 0.2
              }
    pprint(zscore(offers))

    exit(0)
