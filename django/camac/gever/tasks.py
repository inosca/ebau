from .api import GeverAPI

"""
GEVER Background tasks

These background tasks are used for longer-running operations in the GEVER
module

The difference here is that the functions are stand-alone, and no API object
is stored, so the serialisation / deserialisation will not cause problems.
"""


def sync_documents(instance):
    """Perform GEVER sync operations after decision has been decreed."""
    # Spec: "Nach dem Bauentscheid durch die Leitbehörde werden nochmals die
    # Dokumente im BE-GEVER aktualisiert."
    api = GeverAPI(instance)
    if api.get_gever_geschaeft():
        # If there was no sync before, we're not syncing the documents either
        api.sync_documents()


def sync_full(instance):
    api = GeverAPI(instance)
    api.sync_full()
