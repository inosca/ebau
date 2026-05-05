import base64
import random

from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from camac.document import factories
from camac.document.models import Attachment, AttachmentSection
from camac.document.tests.data import django_file
from camac.instance.models import Instance
from camac.user.factories import UserFactory
from camac.user.models import Service, User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--replace",
            dest="replace",
            action="store_true",
            required=False,
            help="Replace previous test files",
        )

        parser.add_argument(
            "--instance",
            dest="instance",
            type=int,
            required=False,
            help="Create documents on this instance (randomly across instances if not given)",
        )
        parser.add_argument(
            "--count",
            dest="count",
            type=int,
            required=True,
            help="Create this many documents",
        )
        parser.add_argument(
            "--versions",
            dest="versions",
            type=int,
            required=False,
            help="Create this many versions of a document (on average, randomized)",
        )
        parser.add_argument(
            "--section",
            dest="section",
            type=int,
            default=None,
            required=False,
            help="Create documents in this section (Randomly across sections if not given)",
        )

    def _section(self):
        if section := self._options.get("section"):
            return AttachmentSection.objects.get(pk=section)
        # TODO maybe make this faster?
        return random.choice(AttachmentSection.objects.all())

    def _instance(self):
        if instance_id := self._options.get("instance"):
            return Instance.objects.get(pk=instance_id)
        # TODO maybe make this faster?
        return random.choice(Instance.objects.all())

    def _num_versions(self):
        if versions := self._options.get("versions"):
            # versions configured. We don't create the exact number
            # of versions though, but +/- a random range

            # variance is 1/2 of the versions. so if cmdline requests 10 versions,
            # the resulting versions count could range from 5 to 15.
            var = random.randint(versions // 2, versions)
            return versions + random.randint(-var, var)

        # If not given, we don't do versions
        return 0

    def _service(self):
        include_sg_names = [
            # TODO extend for UR
            "Fachstellen",
            "Gemeinde",
            "Fachstellen Gemeinden",
        ]
        svc = Service.objects.filter(service_group__name__in=include_sg_names)
        return random.choice(svc)

    def _user(self, service):
        users = User.objects.filter(groups__service=service)
        if users.count():
            return random.choice(users)
        else:
            # service has no users.
            user = UserFactory.build()
            if existing := User.objects.filter(username=user.username).first():
                return existing
            else:
                user.save()
                return user

    def _filename(self, prefix="", version=None):
        prefix = prefix.split(".")[0] or base64.b64encode(random.randbytes(20)).decode(
            "ascii"
        )
        version_suffix = f"_v{version}" if version is not None else ""
        return f"{prefix}{version_suffix}.pdf"

    @transaction.atomic
    def handle(self, *args, **options):
        self._options = options

        if self._options.get("replace"):
            Attachment.objects.filter(context__is_testfile=True).delete()

        content = django_file("multiple-pages.pdf")

        for i in tqdm(range(options["count"])):
            content.seek(0)

            inst = self._instance()
            service = self._service()

            doc = factories.AttachmentFactory(
                context={"is_testfile": True},
                instance=inst,
                size=content.size,
                service=service,
                user=self._user(service),
            )
            doc.name = doc.name.split(".")[0] + ".pdf"

            basename = self._filename()
            doc.path.save(basename, content, save=True)

            tqdm.write(f"New attachment: {doc.pk} [{doc.path}] on instance {inst.pk}")

            section = self._section()
            tqdm.write(f"   in  section: {section}")
            doc.attachment_sections.add(section)
            while random.random() < 0.2:
                # For a small percentage, put the doc in a second (or
                # even third, ...) section
                while (sec := self._section()) in doc.attachment_sections.all():
                    # find a new one, don't add the same section twice
                    pass
                tqdm.write(f"   and section: {sec}")
                doc.attachment_sections.add(sec)

            for v in range(self._num_versions()):
                content.seek(0)
                version = factories.AttachmentVersionFactory(
                    attachment=doc,
                    size=content.size,
                    name=self._filename(basename, v),
                    created_by_user=self._user(self._service()),
                )
                version.path.save(version.name, content, save=True)
                tqdm.write(f"   attachment version: {version.path}")
