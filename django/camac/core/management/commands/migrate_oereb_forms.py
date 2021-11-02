from django.core.management.base import BaseCommand

from camac.instance.models import Form, Instance

OLD_OEREB_FORM_IDS = [
    261,
    281,
    282,
    284,
    285,
    101,
    102,
    103,
    104,
    105,
    106,
    107,
    108,
]


class Command(BaseCommand):
    help = """Migrate the various oereb forms into the new oereb form."""

    def handle(self, *args, **kwargs):
        instances_with_old_forms = Instance.objects.filter(
            form_id__in=OLD_OEREB_FORM_IDS
        )
        self.set_new_oereb_form(instances_with_old_forms)

    def set_new_oereb_form(self, instances):
        new_oereb_form = Form.objects.get(pk=296)
        for instance in instances:
            old_oereb_form = instance.form
            instance.form = new_oereb_form
            instance.save()
            self.stdout.write(
                f"The oereb form for instance {instance.instance_id} has changed from {old_oereb_form} to {new_oereb_form}"
            )
