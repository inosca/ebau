from random import choice, randint

from caluma.caluma_form.models import Form, Question
from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow.api import start_case
from caluma.caluma_workflow.models import Workflow
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from camac.instance.models import Instance, InstanceState
from camac.user.models import Service, User


class Command(BaseCommand):
    help = "Creates an example of a RSTA migrated instance"

    def add_arguments(self, parser):
        parser.add_argument(
            "-c",
            "--count",
            type=int,
            default=1,
            dest="count",
            help="Number of created instances",
            required=False,
        )
        parser.add_argument(
            "-s",
            "--service",
            type=int,
            default=2,  # Burgdorf
            dest="service_id",
            help="Target service for the instance",
            required=False,
        )

    def handle(self, *args, **options):
        workflow = Workflow.objects.get(pk="migrated")
        form = Form.objects.get(pk="migriertes-dossier")
        question = Question.objects.get(pk="geschaeftstyp")
        service = Service.objects.get(pk=options["service_id"])
        instance_state = InstanceState.objects.get(name="in_progress")
        group = service.groups.filter(role__trans__name="Leitung Leitbehörde").first()
        user = User.objects.get(username="service-account-camac-admin")

        caluma_user = BaseUser()
        caluma_user.username = user.username
        caluma_user.group = group.pk

        for _ in range(0, options["count"]):
            instance = Instance.objects.create(
                creation_date=now(),
                modification_date=now(),
                group=group,
                instance_state=instance_state,
                previous_instance_state=instance_state,
                user=user,
                form_id=1,
            )

            instance.instance_services.create(service=service, active=1)

            case = start_case(
                workflow=workflow,
                form=form,
                user=caluma_user,
                meta={
                    "camac-instance-id": instance.pk,
                    "submit-date": now().strftime("%Y-%m-%dT%H:%M:%S%z"),
                    "ebau-number": f"{now().year}-{randint(100,200)}",
                },
            )

            case.document.answers.create(
                question=question,
                value=choice(question.options.values_list("slug", flat=True)),
            )

            case.document.answers.create(question_id="gemeinde", value=service.pk)
