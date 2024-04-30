from collections import namedtuple
from typing import Union

from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import AnswerDocument, Option, Question
from caluma.caluma_user.models import OIDCUser
from caluma.caluma_workflow.api import complete_work_item, skip_work_item
from django.db.models import Prefetch
from django.db.models.query import QuerySet
from django.utils.timezone import now
from django.utils.translation import gettext as _

from camac.caluma.api import CalumaApi
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

    Note: This returns a queryset with zero or multiple services. If you only need
    one, use `get_municipality_provider_service()`.
    """
    if not isinstance(instance, Instance):  # Xzibit would be proud!
        instance = Instance.objects.get(pk=instance)

    municipality = get_municipality(instance)
    relations = ServiceRelation.objects.filter(receiver=municipality, function=function)
    return Service.objects.filter(pk__in=relations.values("provider"))


def set_construction_control(instance: Instance) -> Service:
    municipality = get_municipality(instance)
    construction_control = get_construction_control(municipality)
    instance.instance_services.create(service=construction_control, active=1)

    return construction_control


def build_document_prefetch_statements(prefix="", prefetch_options=False):
    """Build needed prefetch statements to performantly fetch a document.

    This is needed to reduce the query count when almost all the form data
    is needed for a given document, e.g. when exporting a PDF or listing public
    instances (master data).
    """

    question_queryset = Question.objects.select_related(
        "sub_form", "row_form"
    ).order_by("-formquestion__sort")

    if prefetch_options:
        question_queryset = question_queryset.prefetch_related(
            Prefetch(
                "options",
                queryset=Option.objects.order_by("-questionoption__sort"),
            )
        )

    if prefix:
        prefix += "__"

    return [
        f"{prefix}answers",
        f"{prefix}dynamicoption_set",
        Prefetch(
            f"{prefix}answers__answerdocument_set",
            queryset=AnswerDocument.objects.select_related(
                "document__form", "document__family"
            )
            .prefetch_related("document__answers", "document__form__questions")
            .order_by("-sort"),
        ),
        Prefetch(
            # root form -> questions
            f"{prefix}form__questions",
            queryset=question_queryset.prefetch_related(
                Prefetch(
                    # root form -> row forms -> questions
                    "row_form__questions",
                    queryset=question_queryset,
                ),
                Prefetch(
                    # root form -> sub forms -> questions
                    "sub_form__questions",
                    queryset=question_queryset.prefetch_related(
                        Prefetch(
                            # root form -> sub forms -> row forms -> questions
                            "row_form__questions",
                            queryset=question_queryset,
                        ),
                        Prefetch(
                            # root form -> sub forms -> sub forms -> questions
                            "sub_form__questions",
                            queryset=question_queryset.prefetch_related(
                                Prefetch(
                                    # root form -> sub forms -> sub forms -> row forms -> questions
                                    "row_form__questions",
                                    queryset=question_queryset,
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    ]


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

    for instance_service in instance.instance_services.exclude(
        service__service_group__name="construction-control"
    ):
        new_instance.instance_services.create(
            service=instance_service.service,
            active=instance_service.active,
            activation_date=now(),
        )

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
