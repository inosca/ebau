from .api import GeverAPI

"""
GEVER Background tasks

These background tasks are used for longer-running operations in the GEVER
module

The difference here is that the functions are stand-alone, and no API object
is stored, so the serialisation / deserialisation will not cause problems.
"""


def sync_full(instance):
    api = GeverAPI(instance)
    api.sync_full()
