import os

from django.core.management import call_command


def test_dumpdata(db):
    call_command('dumpconfig', stdout=open(os.devnull, 'w'))
