import os

from django.core.management import call_command


def test_loadconfig(db):
    call_command('loadconfig', stdout=open(os.devnull, 'w'))
