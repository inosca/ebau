from caluma.caluma_form import models as form_models
from caluma.caluma_form.validators import AnswerValidator
from caluma.caluma_workflow import models as workflow_models
from django.core.management.base import BaseCommand


# fake user class
class User:
    def __init__(self):
        self.username = "migration"
        self.group = "migration"
        self.camac_role = "admin"


class Command(BaseCommand):
    """Create missing dynamic options for all migrated dynamic choice question answers."""

    help = "Create missing dynamic options for all migrated dynamic choice question answers."

    def handle(self, *args, **options):
        validator = AnswerValidator()
        user = User("migration", "migration")
        for case in workflow_models.Case.objects.all():
            answers = case.document.answers.filter(
                question__type__in=[
                    form_models.Question.TYPE_DYNAMIC_CHOICE,
                    form_models.Question.TYPE_DYNAMIC_MULTIPLE_CHOICE,
                ]
            )
            for answer in answers:
                validator.validate(
                    document=case.document,
                    question=answer.question,
                    value=str(answer.value),
                    user=user,
                )
