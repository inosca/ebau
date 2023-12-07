from caluma.caluma_form.models import Document
from caluma.caluma_user.models import OIDCUser
from caluma.caluma_workflow.api import resume_case, suspend_case
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

from camac.core.utils import create_history_entry
from camac.ech0211.signals import rejected, rejection_reverted
from camac.instance.models import Instance
from camac.notification.utils import send_mail_without_request
from camac.user.models import Group, User


class RejectionLogic:
    @classmethod
    def has_permission(cls, instance: Instance, camac_group: Group) -> bool:
        if not settings.REJECTION:  # pragma: no cover
            return False

        return instance.instance_state.name in [
            settings.REJECTION["INSTANCE_STATE"],
            *settings.REJECTION["ALLOWED_INSTANCE_STATES"],
        ] and (
            instance.responsible_service(filter_type="municipality")
            == camac_group.service
        )

    @classmethod
    def validate_for_rejection(cls, instance: Instance) -> None:
        if WorkItem.objects.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
            status__in=[WorkItem.STATUS_READY, WorkItem.STATUS_SUSPENDED],
            case__family__instance=instance,
        ).exists():
            raise ValidationError(
                _("Instance can't be rejected while there is an open circulation")
            )

        if (
            settings.ADDITIONAL_DEMAND
            and WorkItem.objects.filter(
                task_id=settings.ADDITIONAL_DEMAND["TASK"],
                status=WorkItem.STATUS_READY,
                case__family__instance=instance,
            ).exists()
        ) or (
            settings.APPLICATION_NAME == "kt_bern"
            and Document.objects.filter(
                form_id="nfd-tabelle",
                answers__question_id="nfd-tabelle-status",
                answers__value="nfd-tabelle-status-in-bearbeitung",
                family__work_item__case__instance=instance,
            ).exists()
        ):
            raise ValidationError(
                _("Instance can't be rejected while there are pending claims")
            )

    @classmethod
    @transaction.atomic
    def save_rejection_feedback(
        cls,
        instance: Instance,
        rejection_feedback: str,
    ) -> Instance:

        instance.rejection_feedback = rejection_feedback
        instance.save(update_fields=["rejection_feedback"])

        return instance

    @classmethod
    @transaction.atomic
    def reject_instance(
        cls,
        instance: Instance,
        camac_user: User,
        camac_group: Group,
        caluma_user: OIDCUser,
        rejection_feedback: str,
    ) -> Instance:
        # write text
        instance.rejection_feedback = rejection_feedback
        instance.save(update_fields=["rejection_feedback"])

        # suspend case
        suspend_case(instance.case, caluma_user)

        # set instance state
        instance.set_instance_state(settings.REJECTION["INSTANCE_STATE"], camac_user)

        # trigger ech0211 event
        rejected.send(
            sender="reject_instance",
            instance=instance,
            user_pk=camac_user.pk,
            group_pk=camac_group.pk,
        )

        # history entry
        create_history_entry(
            instance,
            camac_user,
            settings.REJECTION["HISTORY_ENTRIES"]["REJECTED"],
        )

        # send notifications to applicant and municipality
        for notification in settings.REJECTION["NOTIFICATIONS"]["REJECTED"]:
            send_mail_without_request(
                notification["template_slug"],
                camac_user.username,
                camac_group.pk,
                instance={"id": instance.pk, "type": "instances"},
                recipient_types=notification["recipient_types"],
            )

        return instance

    @classmethod
    @transaction.atomic
    def revert_instance_rejection(
        cls,
        instance: Instance,
        camac_user: User,
        camac_group: Group,
        caluma_user: OIDCUser,
    ) -> Instance:
        # resume case
        resume_case(instance.case, caluma_user)

        # reset state to previous
        instance.set_instance_state(instance.previous_instance_state.name, camac_user)

        # trigger ech0211 event
        rejection_reverted.send(
            sender="revert_instance_rejection",
            instance=instance,
            user_pk=camac_user.pk,
            group_pk=camac_group.pk,
        )

        # history entry
        create_history_entry(
            instance,
            camac_user,
            settings.REJECTION["HISTORY_ENTRIES"]["REVERTED"],
        )

        for notification in settings.REJECTION["NOTIFICATIONS"]["REVERTED"]:
            send_mail_without_request(
                notification["template_slug"],
                camac_user.username,
                camac_group.pk,
                instance={"id": instance.pk, "type": "instances"},
                recipient_types=notification["recipient_types"],
            )

        return instance
