#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import signal
import sys


def _reconnect_db(_signum, _frame):
    # late import for avoiding circular imports
    # See management command `snapdb` for details
    from django import db

    print("Received external request to re-connect DB")

    for conn in db.connections.all():
        conn.connect()


# This allows other processes to tell us to reconnect
# to the DB.
signal.signal(signal.SIGUSR2, _reconnect_db)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "camac.settings")
    from django.conf import settings
    from django.core.management import execute_from_command_line

    run_main = os.environ.get("RUN_MAIN") or os.environ.get("WERKZEUG_RUN_MAIN")

    if os.environ.get("ENABLE_PTVSD_DEBUGGER") and settings.DEBUG and run_main:
        import debugpy

        debugpy.listen(("0.0.0.0", 5678))
        print("Attached remote debugger for VSCode")

    execute_from_command_line(sys.argv)
