#!/usr/bin/env python3

"""Some custom markers for tests.

Enables us to selectively run tests that are not project-agnostic.
"""

import os

import pytest

only_schwyz = pytest.mark.skipif(
    os.environ["APPLICATION"] != "kt_schwyz", reason="Schwyz-only test"
)
only_bern = pytest.mark.skipif(
    os.environ["APPLICATION"] != "kt_bern", reason="Bern-only test"
)
