from django.core.management.commands import makemessages


class Command(makemessages.Command):
    msgmerge_options = makemessages.Command.msgmerge_options + ["--no-fuzzy-matching"]
    msgattrib_options = makemessages.Command.msgattrib_options + [
        "--clear-fuzzy",
        "--empty",
    ]

    def handle(self, *args, **options):
        options["add_location"] = "file"
        options["no_obsolete"] = True
        super().handle(*args, **options)
