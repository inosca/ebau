import itertools


def flatten(data):
    return list(itertools.chain(*data))
