from collections import namedtuple
from datetime import datetime
from itertools import chain
from typing import Set, Union

from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Question
from caluma.caluma_user.models import OIDCUser
from caluma.caluma_workflow import models as workflow_models
from caluma.caluma_workflow.api import complete_work_item, skip_work_item
from django.conf import settings
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import gettext as _

from camac.caluma.api import CalumaApi
from camac.constants import kt_bern as bern_constants
from camac.instance.models import Instance
from camac.user.models import Group, Service, ServiceRelation, User


def get_lead_authority(service):
    """Get lead authority matching a given construction control."""
    try:
        return Service.objects.get(
            service_group__name="municipality",
            trans__language="de",
            trans__name=service.trans.get(language="de").name.replace(
                "Baukontrolle", "Leitbehörde"
            ),
        )
    except Service.DoesNotExist:  # pragma: no cover
        raise Exception(
            _(
                "Could not find lead authority for construction control %(id)d"
                % {"id": service.pk}
            )
        )


def get_construction_control(service):
    """Get construction control matching a given lead authority."""
    try:
        return Service.objects.get(
            service_group__name="construction-control",
            trans__language="de",
            trans__name=service.trans.get(language="de").name.replace(
                "Leitbehörde", "Baukontrolle"
            ),
        )
    except Service.DoesNotExist:  # pragma: no cover
        raise Exception(
            _(
                "Could not find construction control for lead authority %(id)d"
                % {"id": service.pk}
            )
        )


def get_municipality(instance: Instance) -> Service:
    """Return the responsible municipality for the given instance.

    Ideally, the municipality is also the currently active service.
    However in certain situations, there needs to be a fallback,
    for example when active service is an RSTA, or when
    the service is only known in the Caluma form.
    """
    involved_municipalities = instance.instance_services.filter(
        service__service_group__name="municipality"
    )
    active_municipality = involved_municipalities.filter(active=1).first()

    if active_municipality:
        # active service is a municipality, take this one
        municipality = active_municipality.service
    elif involved_municipalities.exists():
        # active service is an RSTA, take involved (but not active) municipality
        municipality = involved_municipalities.first().service
    else:
        # no involved municipality, take fallback from form
        municipality = Service.objects.get(pk=CalumaApi().get_municipality(instance))
    return municipality


def get_municipality_provider_services(
    instance: Union[Instance, str, int], function: str
) -> QuerySet[Service]:
    """
    Return *all* services that provde a function in the context of this instance.

    Take the responsible municipality, and check the service relationships to find
    and find any service providing the desired function.

    The `function` needs to be one of the supported functions from
    `user.ServiceRelation.FUNCTION_CHOICES`
    """
    if not isinstance(instance, Instance):  # Xzibit would be proud!
        instance = Instance.objects.get(pk=instance)

    municipality = get_municipality(instance)
    return get_provider_services(municipality, function)


def get_provider_services(service: Service, function: str) -> QuerySet[Service]:
    """
    Return services that provde `function` to `service`.

    The `function` needs to be one of the supported functions from
    `user.ServiceRelation.FUNCTION_CHOICES`
    """
    relations = ServiceRelation.objects.filter(receiver=service, function=function)
    return Service.objects.filter(pk__in=relations.values("provider"))


def set_construction_control(instance: Instance) -> Service:
    municipality = get_municipality(instance)
    construction_control = get_construction_control(municipality)
    instance.instance_services.create(service=construction_control, active=1)

    return construction_control


def copy_instance(
    instance: Instance,
    group: Group,
    user: User,
    caluma_user: OIDCUser,
    skip_submit: bool = True,
    new_meta: dict = {},
    old_meta: dict = {},
) -> Instance:
    from camac.instance.serializers import CalumaInstanceSerializer

    FakeRequest = namedtuple(
        "FakeRequest", ["group", "user", "caluma_info", "query_params"]
    )
    FakeCalumaInfo = namedtuple("FakeCalumaInfo", ["context"])
    FakeCalumaContext = namedtuple("FakeCalumaContext", ["user"])

    context = {
        "request": FakeRequest(
            group=group,
            user=user,
            caluma_info=FakeCalumaInfo(context=FakeCalumaContext(user=caluma_user)),
            query_params={},
        )
    }

    serializer = CalumaInstanceSerializer(
        data={
            "copy_source": instance.pk,
            "is_modification": False,
        },
        context=context,
    )

    serializer.is_valid(raise_exception=True)
    serializer.save()

    new_instance = serializer.instance
    new_instance.copy_source = instance

    for instance_service in instance.instance_services.exclude(
        service__service_group__name="construction-control"
    ):
        new_instance.instance_services.create(
            service=instance_service.service,
            active=instance_service.active,
            activation_date=now(),
        )

    if instance.case.meta.get("is-bab"):
        new_meta["is-bab"] = True

    if new_meta:
        # Update meta properties of new instance
        new_instance.case.meta.update(new_meta)
        new_instance.case.save()

    if old_meta:
        # Update meta properties of old instance
        instance.case.meta.update(old_meta)
        instance.case.save()

    if skip_submit:
        skip_work_item(
            work_item=new_instance.case.work_items.get(task_id="submit"),
            user=caluma_user,
        )

        if old_submit_date := instance.case.meta.get("submit-date"):
            new_instance.case.meta["submit-date"] = old_submit_date
            new_instance.case.save()

        new_instance.set_instance_state("subm", user)

    from camac.permissions.events import Trigger

    Trigger.instance_copied(None, new_instance, instance)

    return new_instance


def fill_ebau_number(
    instance: Instance, ebau_number: str, caluma_user: OIDCUser
) -> Instance:
    work_item = instance.case.work_items.get(task_id="ebau-number")

    # Answer ebau number form questions
    for question, value in [
        ("ebau-number-has-existing", "ebau-number-has-existing-yes"),
        ("ebau-number-existing", ebau_number),
    ]:
        save_answer(
            question=Question.objects.get(pk=question),
            document=work_item.document,
            value=value,
            user=caluma_user,
        )

    # Update meta
    instance.case.meta.update({"ebau-number": ebau_number})
    instance.case.save()

    # Complete work item
    complete_work_item(work_item=work_item, user=caluma_user)


def geometer_cadastral_survey_is_necessary(answer):
    return answer == bern_constants.GEOMETER_NECESSARY_OPTION_SLUG


def geometer_cadastral_survey_necessary_answer(instance):
    geometer_work_item = instance.case.work_items.filter(
        task_id=bern_constants.GEOMETER_TASK_SLUG,
        status=workflow_models.WorkItem.STATUS_COMPLETED,
    ).first()

    if geometer_work_item:
        return (
            geometer_work_item.document.answers.filter(
                question_id=bern_constants.GEOMETER_NECESSITY_QUESTION_SLUG
            )
            .values_list("value", flat=True)
            .first()
        )

    return None


def get_changeable_forms(current_form: str) -> Set[str]:
    if not settings.CHANGE_FORM:  # pragma: no cover
        return set()

    return set(
        chain(
            *[
                form_list
                for form_list in settings.CHANGE_FORM["INTERCHANGEABLE_FORMS"]
                if current_form in form_list
            ]
        )
    )


def get_geometer_service(instance: Instance) -> Service | None:
    geometer_answer = (
        instance.fields.filter(name__in=settings.APPLICATION["GEOMETER_FORM_FIELDS"])
        .values_list("value", flat=True)
        .first()
    )
    if not geometer_answer:
        return None

    geometer_service_id = settings.APPLICATION["GEOMETER_SERVICE_MAPPING"].get(
        geometer_answer, None
    )
    if not geometer_service_id:
        return None

    return Service.objects.filter(pk=geometer_service_id, disabled=0).first()


def be_should_prevent_process_step_for_deactivated_municipality(
    instance, municipality=None
):
    if not municipality:
        active_municipalities = (
            instance.instance_services.filter(
                active=1, service__service_group__name="municipality"
            )
            .values_list("service", flat=True)
            .distinct()
        )

        # If there is no active lead municipality or multiple,
        # regard as not deactivated
        if active_municipalities.count() != 1:
            return False

        municipality_id = active_municipalities.first()
        municipality = Service.objects.get(pk=municipality_id)

    try:
        municipality_config = municipality.meta.get("deactivated-municipality-at")
        if not municipality_config:
            return False

        # Make configured deactivation date timezone aware if necessary
        deactivation_date_time = datetime.fromisoformat(municipality_config)
        if not timezone.is_aware(deactivation_date_time):
            deactivation_date_time = timezone.make_aware(deactivation_date_time)

        current_date_time = timezone.now()

        # If the current date is past the deactivation date, the current
        # responsible municipality on this instance is regarded as deactivated
        return deactivation_date_time <= current_date_time

    except Exception:
        # Faulty municipality or meta configuration
        # Default to not deactivated
        return False
