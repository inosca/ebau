#!/usr/bin/env python

import cx_Oracle
import time
import sys

retries = 60

while retries > 0:
    if retries % 2 == 0:
        print("Waiting for oracle service")

    try:
        db = cx_Oracle.connect('system', 'oracle',
                               '%s:%s/XE' % (sys.argv[1], sys.argv[2]))
    except cx_Oracle.DatabaseError:
        time.sleep(1)
        retries -= 1
        continue

    sys.exit(0)

sys.exit(1)
