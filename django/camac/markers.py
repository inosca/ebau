"""Some custom markers for tests.

Enables us to selectively run tests that are not project-agnostic.
"""

import os

import pytest


def only_in(*cantons):
    return pytest.mark.skipif(
        os.environ["APPLICATION"] not in cantons,
        reason="Test runs only in %s" % (", ".join(cantons)),
    )


only_bern = only_in("kt_bern")
