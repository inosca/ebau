from django.core.management.commands import makemessages


class Command(makemessages.Command):
    def handle(self, *args, **options):
        options["add_location"] = "file"
        options["no_obsolete"] = True
        super().handle(*args, **options)
