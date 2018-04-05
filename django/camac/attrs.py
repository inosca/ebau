from functools import reduce


def nested_getattr(obj, attr, default=None):
    """
    Get nested attributes with dot annotations.

    If one level doesn't exist default will be returned.
    """
    def getattr_default(obj, name):
        return getattr(obj, name, None)

    val = reduce(getattr_default, attr.split('.'), obj)
    return val if val is not None else default
