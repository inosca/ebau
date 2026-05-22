import glob
import os.path
import random
import re

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from camac.document.models import Attachment, AttachmentVersion
from camac.document.tests.data import _data_path, django_file
from camac.instance.models import Instance


class Command(BaseCommand):
    help = (
        "Put data into all documents of the given instances. "
        "Useful for testing migration on prod dumps"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--instances",
            dest="instances",
            type=str,
            required=False,
            help="Create documents on this instance. Can be a single integer, or a range in the form of A..B",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self._options = options

        print("Storage backend: ", settings.STORAGES["default"]["BACKEND"])

        for attachment in tqdm(self._attachments(), "Updating attachments"):
            attachment.path.save(
                os.path.basename(attachment.path.name),
                self._content(attachment.path.name),
            )
            attachment.save()

        for version in tqdm(self._versions(), "Updating attachment versions"):
            version.path.save(
                os.path.basename(attachment.path.name),
                self._content(attachment.path.name),
            )
            version.save()

    def _instances(self):
        assert self._options["instances"], "No instances given"
        range = re.split(r"\.\.|-", self._options["instances"])
        assert len(range) in [1, 2], "Instances given does not reflect a proper range"

        begin = range[0]

        try:
            end = range[1]
        except IndexError:  # pragma: no cover
            end = begin

        return Instance.objects.filter(pk__gte=begin, pk__lte=end)

    def _attachments(self):
        return Attachment.objects.filter(instance__in=self._instances())

    def _versions(self):
        return AttachmentVersion.objects.filter(
            attachment__instance__in=self._instances()
        )

    def _content(self, previous_name):
        request_suffix = previous_name.rsplit(".", 2)[-1].lower()
        # some replacements needed
        request_suffix = {
            "jpeg": "jpg",
            "tiff": "tif",
            "doc": "docx",
            "xls": "xlsx",
            "heic": "jpg",  # don't have apple images to test
        }.get(request_suffix, request_suffix)

        candidates = glob.glob(f"{_data_path}/**", recursive=True)
        names = [n for n in candidates if n.endswith(f".{request_suffix}")]

        if not names:  # pragma: no cover
            raise RuntimeError(
                f"No test file with suffix {request_suffix} in {_data_path}"
            )
        name = os.path.basename(random.choice(names))
        content = django_file(name)
        content.seek(0)
        return content
