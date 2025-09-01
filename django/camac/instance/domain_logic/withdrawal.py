from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Answer, Question
from caluma.caluma_user.models import OIDCUser
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db import transaction
from django.db.models import Exists, OuterRef, Q
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

from camac.core.utils import create_history_entry
from camac.ech0211.signals import withdrawn
from camac.instance.models import Instance
from camac.notification.utils import send_mail_without_request
from camac.user.models import Group, User


def get_active_and_future_publications(instance: Instance) -> QuerySet[WorkItem]:
    if not settings.PUBLICATION:  # pragma: no cover
        return WorkItem.objects.none()

    work_items = WorkItem.objects.filter(
        **{
            "case": instance.case,
            "task_id": settings.PUBLICATION["FILL_TASKS"]["PUBLIC"],
            "meta__is-published": True,
            "status": WorkItem.STATUS_COMPLETED,
        }
    )

    range_filters = Q()
    for __, end_question in settings.PUBLICATION["RANGE_QUESTIONS"]["PUBLIC"]:
        # return all publication work items that have an end date in the future
        # as we need to cancel them. Those are either currently active or will
        # be active in the future.
        range_filters |= Q(
            Exists(
                Answer.objects.filter(
                    document_id=OuterRef("document_id"),
                    question_id=end_question,
                    date__gte=timezone.now(),
                )
            )
        )

    return work_items.filter(range_filters)


class WithdrawalLogic:
    @classmethod
    @transaction.atomic
    def withdraw_instance(
        cls,
        instance: Instance,
        camac_user: User,
        camac_group: Group,
        caluma_user: OIDCUser,
    ) -> Instance:
        if settings.WITHDRAWAL["TYPE"] == "light":
            instance = cls.withdraw_instance_light(instance, caluma_user)
        else:
            instance = cls.withdraw_instance_full(
                instance, camac_user, camac_group, caluma_user
            )

        # history entry
        create_history_entry(
            instance,
            camac_user,
            settings.WITHDRAWAL["HISTORY_ENTRIES"]["REQUESTED"],
        )

        # send notifications
        for notification in settings.WITHDRAWAL["NOTIFICATIONS"]:
            send_mail_without_request(
                notification["template_slug"],
                camac_user.username,
                camac_group.pk,
                instance={"id": instance.pk, "type": "instances"},
                recipient_types=notification["recipient_types"],
            )

        return instance

    @classmethod
    def withdraw_instance_light(
        cls,
        instance: Instance,
        caluma_user: OIDCUser,
    ) -> Instance:
        request = WorkItem.objects.filter(
            task_id=settings.WITHDRAWAL["REQUEST_TASK"],
            status=WorkItem.STATUS_READY,
            case__family__instance=instance,
        ).first()

        if not request:
            raise ValidationError(_("Withdrawal not possible."))

        instance.case.meta["withdrawal-requested"] = True
        instance.case.save()

        workflow_api.complete_work_item(
            request,
            user=caluma_user,
        )

        return instance

    @classmethod
    def withdraw_instance_full(
        cls,
        instance: Instance,
        camac_user: User,
        camac_group: Group,
        caluma_user: OIDCUser,
    ) -> Instance:
        # process work items
        for task_id, action in settings.WITHDRAWAL["PROCESS_WORK_ITEMS"]:
            for work_item in WorkItem.objects.filter(
                task_id=task_id,
                status=WorkItem.STATUS_READY,
                case__family__instance=instance,
            ):
                getattr(workflow_api, f"{action}_work_item")(work_item, caluma_user)

        # cancel active publications
        for work_item in get_active_and_future_publications(instance):
            work_item.meta["is-published"] = False
            work_item.save()

        # pre-fill decision answer
        save_answer(
            document=instance.case.work_items.get(
                task_id=settings.DECISION["TASK"], status=WorkItem.STATUS_READY
            ).document,
            question=Question.objects.get(
                pk=settings.DECISION["QUESTIONS"]["DECISION"]
            ),
            value=settings.DECISION["ANSWERS"]["DECISION"]["WITHDRAWAL"],
            user=caluma_user,
        )

        # set instance state
        instance.set_instance_state(settings.WITHDRAWAL["INSTANCE_STATE"], camac_user)

        # trigger ech0211 event
        withdrawn.send(
            sender="withdraw_instance",
            instance=instance,
            user_pk=camac_user.pk,
            group_pk=camac_group.pk,
        )

        return instance
