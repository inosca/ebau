from collections import namedtuple

from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import AnswerDocument, Option, Question
from caluma.caluma_user.models import OIDCUser
from caluma.caluma_workflow.api import complete_work_item, skip_work_item
from django.db.models import Prefetch
from django.utils.timezone import now
from django.utils.translation import gettext as _

from camac.caluma.api import CalumaApi
from camac.instance.models import Instance
from camac.user.models import Group, Service, User


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


def set_construction_control(instance: Instance) -> Service:
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
