import os
import shutil

from django.conf import settings
from django.core.files import File

_data_path = os.path.dirname(os.path.realpath(__file__))


def django_file(name, mode="rb"):
    abspath = os.path.join(_data_path, name)
    new_path = f"{settings.MEDIA_ROOT}/attachments"

    try:
        os.makedirs(new_path)
    except FileExistsError:  # pragma: no cover
        pass

    new_name = os.path.basename(name)
    shutil.copy(abspath, f"{new_path}/{new_name}")

    return File(open(abspath, mode), name=f"attachments/{new_name}")
