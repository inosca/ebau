from django.core.management.base import BaseCommand

from camac.instance.models import Instance


class Command(BaseCommand):
    help = """Migrate the various oereb forms into the new oereb form."""

    def handle(self, *args, **kwargs):
        instances = Instance.objects.filter(form_id=296)
        for instance in instances:
            answer = instance.case.document.answers.filter(
                question_id="form-type"
            ).first()
            old_value = answer.value
            answer.value = "form-type-oereb"
            answer.save()
            print(f"Fixed form type of instance {instance.pk} (was {old_value})")
