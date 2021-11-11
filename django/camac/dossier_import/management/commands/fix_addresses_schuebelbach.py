import pprint
import re

from django.core.management import BaseCommand

from camac.instance.models import FormField


class Command(BaseCommand):

    help = """Fix addresses without house nr for Schübelbach."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            type=bool,
            help="Commit changes to db",
        )

    def handle(self, *args, **options):
        changes = []
        locations = FormField.objects.filter(
            instance__case__meta__has_key="import-id",
            name="ortsbezeichnung-des-vorhabens",
            value__icontains="None",
        )
        for location in locations.iterator():
            if location.instance.pk not in changes:
                changes.append(location.instance.pk)
            search = re.search(r"None$", location.value)
            if search:
                start, end = search.span()
                tail = end - start
                location.value = location.value[:-tail].strip()
                changes.append(location.pk)
                if options["commit"]:
                    location.save()

        for address in FormField.objects.filter(
            instance__case__meta__has_key="import-id",
            name__in=[
                "bauherrschaft",
                "grundeigentumerschaft",
                "projektverfasser-planer",
            ],
            value__0__strasse__icontains="None",
        ).iterator():
            if address.instance.pk not in changes:
                changes.append(address.instance.pk)
            if address.value and address.value[0].get("strasse"):
                search = re.search(r"None$", address.value[0]["strasse"])
                if search:
                    start, end = search.span()
                    tail = end - start
                address.value[0]["strasse"] = address.value[0]["strasse"][
                    :-tail
                ].strip()
                if options["commit"]:
                    address.save()
        self.stdout.write(f"Instances: {pprint.pformat(changes)}")
