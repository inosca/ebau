from django.apps import apps
from django.core.management.base import CommandError
from reversion.management.commands.deleterevisions import Command as OriginalCommand
from reversion.revisions import is_registered


class Command(OriginalCommand):
    """
    Overload the "upstream" `deleterevisions` command.

    This just reimplements `get_model()` without invoking django admin,
    which we don't need

    """

    def get_models(self, options):  # pragma: no cover
        # Since it's literally a copy, we don't bother enforcing coverage here

        # Get options.
        app_labels = options["app_label"]
        # Parse model classes.
        if len(app_labels) == 0:
            selected_models = apps.get_models()
        else:
            selected_models = set()
            for label in app_labels:
                if "." in label:
                    # This is an app.Model specifier.
                    try:
                        model = apps.get_model(label)
                    except LookupError:
                        raise CommandError("Unknown model: {0}".format(label))
                    selected_models.add(model)
                else:
                    # This is just an app - no model qualifier.
                    app_label = label
                    try:
                        app = apps.get_app_config(app_label)
                    except LookupError:
                        raise CommandError("Unknown app: {0}".format(app_label))
                    selected_models.update(app.get_models())
        for model in selected_models:
            if is_registered(model):
                yield model
