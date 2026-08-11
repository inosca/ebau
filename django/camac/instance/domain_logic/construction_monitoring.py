from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.utils.translation import gettext_noop

from camac.caluma.models import Inquiry
from camac.core.utils import create_history_entry
from camac.ech0211.signals import construction_monitoring_started
from camac.instance.models import Instance
from camac.settings.utils import is_module_enabled
from camac.user.models import Service, User


def can_perform_construction_monitoring(instance: Instance) -> bool:
    """Check whether the construction monitoring process should be started.

    The construction monitoring process should not be included for all
    instances. For instance, a preliminary clarification (Vorabklärung) is an
    informal inquiry and should never cause a construction monitoring process.

    In Kt. UR, the necessity for a construction monitoring process is decided by
    answering the question "Baubewilligungspflichtig" with "Ja" in the
    "complete-check" form.

    In all the other cantons, we check whether the root form is in the
    construction monitoring's `ALLOW_FORMS` config. If there are none configured
    (which is the default), all instances get a construction monitoring process.

    WARNING: `ALLOW_FORMS` does not contain Caluma form slugs but CAMAC form
    names. Kt. SZ is the only canton actually still using those.
    """

    if not is_module_enabled("CONSTRUCTION_MONITORING"):
        return False

    if settings.APPLICATION_NAME == "kt_uri":
        complete_check_work_item = instance.case.work_items.get(
            task_id="complete-check"
        )

        if complete_check_work_item.meta.get("migrated"):  # pragma: no cover
            # If an instance was migrated we don't know if the construction
            # monitoring is required. In this case we always start it (it can be
            # skipped if not required).
            return True

        # In Uri we need to check the "complete-check" work item because not all
        # forms always require a construction monitoring process.
        return complete_check_work_item.document.answers.filter(
            question_id="complete-check-baubewilligungspflichtig",
            value="complete-check-baubewilligungspflichtig-baubewilligungspflichtig",
        ).exists()

    allow_forms = settings.CONSTRUCTION_MONITORING.get("ALLOW_FORMS")
    if not allow_forms:
        return True

    # Get the form slug based on the form backend configuration. For camac-ng
    # (e.g. Kt. SZ), use the form family name if available, otherwise the form
    # name. For Caluma, rely on the case document's form ID.
    if settings.APPLICATION["FORM_BACKEND"] == "camac-ng":
        form_slug = (
            instance.form.family.name if instance.form.family else instance.form.name
        )
    else:
        form_slug = instance.case.document.form_id

    return form_slug in allow_forms


def start_construction_monitoring(
    instance: Instance,
    user: BaseUser,
    camac_user: User,
    sender: str,
) -> None:
    """Apply side effects for starting construction monitoring."""

    create_history_entry(
        instance, camac_user, gettext_noop("Construction monitoring started")
    )
    instance.set_instance_state(
        settings.CONSTRUCTION_MONITORING["CONSTRUCTION_MONITORING_INSTANCE_STATE"],
        camac_user,
    )

    if settings.ECH0211.get("API_LEVEL") != "full":  # pragma: no cover
        return

    construction_monitoring_started.send(
        sender=sender,
        instance=instance,
        user_pk=camac_user.pk,
        group_pk=user.camac_group,
    )

    # In Kt. GR, also create the construction-monitoring status message for ARE
    # if ARE was inquired.
    if settings.APPLICATION_NAME == "kt_gr":
        service_are = Service.objects.get(slug="are")
        if (
            Inquiry.objects.for_instance(instance)
            .addressed_to(service_are)
            .only_active()
            .exists()
        ):
            construction_monitoring_started.send(
                sender=sender,
                instance=instance,
                user_pk=camac_user.pk,
                group_pk=service_are.pk,
                message_receiver=service_are,
            )


def maybe_start_construction_monitoring_after_construction_step(
    instance: Instance, user: BaseUser, camac_user: User
) -> None:
    """Start construction monitoring when the instance is in the expected state."""

    if not is_module_enabled("CONSTRUCTION_MONITORING"):
        return

    if (
        instance.instance_state.name
        != settings.CONSTRUCTION_MONITORING["PREVIOUS_INSTANCE_STATE"]
    ):
        return

    start_construction_monitoring(
        instance,
        user,
        camac_user,
        sender="post_complete_construction_step_work_item",
    )


def maybe_start_construction_monitoring_after_decision(
    instance: Instance, user: BaseUser, camac_user: User
) -> None:
    """Start construction monitoring completed before a positive decision."""

    if not is_module_enabled("CONSTRUCTION_MONITORING"):
        return

    if not settings.CONSTRUCTION_MONITORING.get("START_AFTER_SUBMIT"):
        return

    if (
        instance.instance_state.name
        != settings.CONSTRUCTION_MONITORING["PREVIOUS_INSTANCE_STATE"]
    ):
        return

    init_work_item_exists = instance.case.work_items.filter(
        task_id=settings.CONSTRUCTION_MONITORING["INIT_CONSTRUCTION_MONITORING_TASK"],
        status=WorkItem.STATUS_COMPLETED,
    ).exists()
    if not init_work_item_exists:
        return

    start_construction_monitoring(
        instance,
        user,
        camac_user,
        sender="post_complete_decision",
    )
