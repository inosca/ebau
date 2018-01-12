import os.path

from django.core.files import File

_data_path = os.path.dirname(os.path.realpath(__file__))


def django_file(name, mode='rb'):
    abspath = os.path.join(_data_path, name)
    return File(open(abspath, mode))
