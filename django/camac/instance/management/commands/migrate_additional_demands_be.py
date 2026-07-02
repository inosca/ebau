import math
import textwrap
import traceback
from collections import defaultdict
from datetime import datetime
from itertools import batched

from caluma.caluma_form.models import Answer, Document
from caluma.caluma_workflow.models import Case, Task, Workflow, WorkItem
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Exists, F, OuterRef, Prefetch, Q, Subquery
from django.utils import timezone
from tqdm import tqdm

from camac.document.models import Attachment
from camac.responsible.models import ResponsibleService
from camac.user.models import User

MIGRATION_META_TIMESTAMP_KEY = "nfd-migrated-at"
MIGRATION_META_CLAIM_ID_KEY = "nfd-migrated-from-claimId"
PRECEDING_TASK = "submit"
STATUS_COMPLETED = "completed"  # same for Case and WorkItem
INDENT = "    "  # define standard log indentation

CANCEL_INSTANCE_STATES = [
    "sb1",
    "sb2",
    "conclusion",
    "finished",
    "finished_internal",
    "evaluated",
    "archived",
]
SUSPEND_INSTANCE_STATES = ["rejected", "correction"]

DRAFT_STATUS_VALUE = "nfd-tabelle-status-entwurf"
ANSWERED_STATUS_VALUE = "nfd-tabelle-status-beantwortet"
IN_PROGRESS_STATUS_VALUE = "nfd-tabelle-status-in-bearbeitung"
DONE_STATUS_VALUE = "nfd-tabelle-status-erledigt"

SEND_DEMAND_FORM_ID = "send-additional-demand"
FILL_DEMAND_FORM_ID = "fill-additional-demand"
CHECK_DEMAND_FORM_ID = "check-additional-demand"

BASE_WORKITEM_META = {
    MIGRATION_META_TIMESTAMP_KEY: timezone.now().isoformat(),
    "not-viewed": True,
    "notify-deadline": False,
    "notify-completed": False,
}

BASE_MIGRATION_META = {
    MIGRATION_META_TIMESTAMP_KEY: timezone.now().isoformat(),
}


def get_task_name(task_id):
    return Task.objects.get(pk=task_id).name


WORK_ITEM_NAME_MAPPING = {
    "init-additional-demand": get_task_name("init-additional-demand"),
    "additional-demand": get_task_name("additional-demand"),
    "send-additional-demand": get_task_name("send-additional-demand"),
    "check-additional-demand": get_task_name("check-additional-demand"),
    "fill-additional-demand": get_task_name("fill-additional-demand"),
}


class Command(BaseCommand):
    help = "Migration of claims to additional-demands"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._responsible = {}

        self.STEP_MAP = {
            DRAFT_STATUS_VALUE: [self._run_draft_step],
            IN_PROGRESS_STATUS_VALUE: [
                self._run_draft_step,
                self._run_in_progress_step,
            ],
            ANSWERED_STATUS_VALUE: [
                self._run_draft_step,
                self._run_in_progress_step,
                self._run_answered_step,
            ],
            DONE_STATUS_VALUE: [
                self._run_draft_step,
                self._run_in_progress_step,
                self._run_answered_step,
                self._run_done_step,
            ],
        }

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            dest="reset",
            action="store_true",
            default=False,
            help="Find and delete migrated work items, cases, documents, answers and attachments.",
        )
        parser.add_argument(
            "--commit",
            action="store_true",
            help="Commit the changes to the database.",
        )
        parser.add_argument(
            "--no-logging",
            action="store_true",
            help="Run migration script without the case summary logs.",
        )

    def reset(self):
        self.stdout.write(self.style.WARNING("\n RESET MODE \n"))

        work_items_to_delete = WorkItem.objects.filter(
            task_id__in=[
                settings.ADDITIONAL_DEMAND["CREATE_TASK"],
                settings.ADDITIONAL_DEMAND["TASK"],
                settings.ADDITIONAL_DEMAND["SEND_TASK"],
                settings.ADDITIONAL_DEMAND["FILL_TASK"],
                settings.ADDITIONAL_DEMAND["CHECK_TASK"],
            ],
            meta__has_key=MIGRATION_META_TIMESTAMP_KEY,
        )

        tqdm.write(
            f"Found {work_items_to_delete.count()} migrated work items to delete..."
        )
        if work_items_to_delete.exists():
            work_items_to_delete.delete()

        child_cases_to_delete = Case.objects.filter(
            workflow_id=settings.ADDITIONAL_DEMAND["WORKFLOW"],
            meta__has_key=MIGRATION_META_TIMESTAMP_KEY,
        )
        tqdm.write(
            f"Found {child_cases_to_delete.count()} migrated child cases to delete..."
        )
        if child_cases_to_delete.exists():
            child_cases_to_delete.delete()

        documents_to_delete = Document.objects.filter(
            form_id__in=[
                SEND_DEMAND_FORM_ID,
                FILL_DEMAND_FORM_ID,
                CHECK_DEMAND_FORM_ID,
            ],
            meta__has_key=MIGRATION_META_TIMESTAMP_KEY,
        )

        tqdm.write(
            f"Found {documents_to_delete.count()} migrated documents to delete..."
        )
        if documents_to_delete.exists():
            documents_to_delete.delete()

        attachments_to_revert = Attachment.objects.filter(
            context__has_key=MIGRATION_META_CLAIM_ID_KEY
        )
        attachments_count = attachments_to_revert.count()
        tqdm.write(f"Found {attachments_count} migrated attachments to revert...")
        if attachments_count > 0:
            reverted_attachments_count = 0
            for att in attachments_to_revert:
                try:
                    original_claim_id = att.context.get(MIGRATION_META_CLAIM_ID_KEY)
                    if original_claim_id:
                        att.context["claimId"] = original_claim_id
                        att.context.pop(MIGRATION_META_CLAIM_ID_KEY, None)
                        att.context.pop(MIGRATION_META_TIMESTAMP_KEY, None)
                        att.save(update_fields=["context"])
                        reverted_attachments_count += 1
                except Exception as e:
                    tqdm.write(
                        f"  ERROR: Failed to revert attachment {att.pk}. Error: {e}"
                    )

            tqdm.write(
                f"  => Successfully reverted {reverted_attachments_count} attachments."
            )

        tqdm.write(
            f"Clearing '{MIGRATION_META_TIMESTAMP_KEY}' from all parent cases..."
        )

        updated_count = Case.objects.filter(
            meta__has_key=MIGRATION_META_TIMESTAMP_KEY
        ).update(meta=F("meta") - MIGRATION_META_TIMESTAMP_KEY)

        tqdm.write(f"Cleared migration status from {updated_count} cases.")

    def responsible_user(self, service_id, instance):
        responsible = self._responsible.get((service_id, instance.pk))

        if responsible is None:
            responsible = list(
                ResponsibleService.objects.filter(
                    instance=instance,
                    service_id=service_id,
                    responsible_user__isnull=False,
                ).values_list("responsible_user__username", flat=True)
            )

            self._responsible[(service_id, instance.pk)] = responsible

        return responsible

    @staticmethod
    def _get_datetime_from_answer(answers_dict, key):
        answer = answers_dict.get(key)
        if answer and answer.date:
            naive_dt = datetime.combine(answer.date, datetime.min.time())
            aware_dt = timezone.make_aware(naive_dt)
            return aware_dt
        return None

    def _get_assigned_users(self, service_id, instance):
        return [
            username
            for username in self.responsible_user(
                service_id=service_id, instance=instance
            )
        ]

    @staticmethod
    def _determine_init_status(case):
        instance_state_name = (
            case.instance.instance_state.name if case.instance.instance_state else ""
        )

        is_paper = getattr(case, "is_paper_annotated", False)

        nfd_completed = case.nfd_work_item.status == WorkItem.STATUS_COMPLETED
        is_completed_state = instance_state_name in CANCEL_INSTANCE_STATES

        if is_paper or nfd_completed or is_completed_state:
            return WorkItem.STATUS_CANCELED

        nfd_suspended = case.nfd_work_item.status == WorkItem.STATUS_SUSPENDED
        is_suspended_state = instance_state_name in SUSPEND_INSTANCE_STATES

        if nfd_suspended or is_suspended_state:
            return WorkItem.STATUS_SUSPENDED

        return WorkItem.STATUS_READY

    @staticmethod
    def _build_attachments_map(case):
        mapping = defaultdict(list)

        # prefetched
        claim_attachments = getattr(case.instance, "claim_attachments_list", [])
        for att in claim_attachments:
            claim_id = att.context.get("claimId")
            mapping[str(claim_id)].append(att)

        return mapping

    @staticmethod
    def _complete_object(
        obj,
        closed_by_user,
        closed_by_group=None,
        created_by_user=None,
        created_by_group=None,
        addressed_groups=None,
        controlling_groups=None,
        assigned_users=None,
        closed_at=None,
        original_claim_id=None,
        save=True,
    ):
        updates = {
            "closed_by_user": closed_by_user,
            "closed_by_group": closed_by_group,
            "closed_at": closed_at,
            "created_by_user": created_by_user,
            "created_by_group": created_by_group,
            "addressed_groups": addressed_groups,
            "controlling_groups": controlling_groups,
            "assigned_users": assigned_users,
        }

        obj.status = STATUS_COMPLETED
        fields_to_save = ["status"]

        for field, value in updates.items():
            if value is None:
                continue

            if not hasattr(obj, field):
                continue

            setattr(obj, field, value)
            fields_to_save.append(field)

        if original_claim_id and hasattr(obj, "meta"):
            current_meta = obj.meta or {}
            current_meta[MIGRATION_META_CLAIM_ID_KEY] = original_claim_id
            obj.meta = current_meta
            fields_to_save.append("meta")

        if save:
            obj.save(update_fields=fields_to_save)

    def _create_child_case_and_parent_work_item(
        self,
        parent_case,
        workflow,
        previous_work_item,
        username,
        service_id,
        addressed_groups,
        assigned_users,
        created_at_override=None,
        original_claim_id=None,
        parent_init_status=WorkItem.STATUS_READY,
    ):
        case_meta = BASE_MIGRATION_META.copy()
        work_item_meta = BASE_WORKITEM_META.copy()
        if original_claim_id:
            case_meta[MIGRATION_META_CLAIM_ID_KEY] = original_claim_id
            work_item_meta[MIGRATION_META_CLAIM_ID_KEY] = original_claim_id

        closed_at = None
        closed_by_group = None
        closed_by_user = None
        case_status = Case.STATUS_RUNNING

        if parent_init_status == WorkItem.STATUS_CANCELED:
            case_status = Case.STATUS_CANCELED
            closed_at = parent_case.nfd_work_item.closed_at
            closed_by_group = parent_case.nfd_work_item.closed_by_group
            closed_by_user = parent_case.nfd_work_item.closed_by_user

        elif parent_init_status == WorkItem.STATUS_SUSPENDED:
            case_status = Case.STATUS_SUSPENDED

        child_case = Case.objects.create(
            status=case_status,
            workflow=workflow,
            family=parent_case,
            meta=case_meta,
            created_by_user=username,
            created_by_group=service_id,
            modified_by_user=username,
            modified_by_group=service_id,
            closed_at=closed_at,
            closed_by_group=closed_by_group,
            closed_by_user=closed_by_user,
        )

        additional_demand_work_item = WorkItem.objects.create(
            task_id=settings.ADDITIONAL_DEMAND["TASK"],
            name=WORK_ITEM_NAME_MAPPING.get(settings.ADDITIONAL_DEMAND["TASK"]),
            addressed_groups=addressed_groups,
            controlling_groups=addressed_groups,
            assigned_users=assigned_users,
            status=parent_init_status,
            meta=work_item_meta,
            case=parent_case,
            previous_work_item=previous_work_item,
            created_by_user=username,
            created_by_group=service_id,
            child_case=child_case,
            closed_at=closed_at,
            closed_by_group=closed_by_group,
            closed_by_user=closed_by_user,
        )

        if created_at_override:
            WorkItem.objects.filter(pk=additional_demand_work_item.pk).update(
                created_at=created_at_override
            )
            Case.objects.filter(pk=child_case.pk).update(created_at=created_at_override)

        return child_case, additional_demand_work_item

    @staticmethod
    def _create_document_and_work_item(
        case,
        form_id,
        task_id,
        previous_work_item,
        addressed_groups,
        controlling_groups,
        created_by_user,
        assigned_users=None,
        created_by_group=None,
        created_at_override=None,
        original_claim_id=None,
        parent_init_status=WorkItem.STATUS_READY,
    ):
        document_meta = BASE_MIGRATION_META.copy()
        work_item_meta = BASE_WORKITEM_META.copy()
        if original_claim_id:
            document_meta[MIGRATION_META_CLAIM_ID_KEY] = original_claim_id
            work_item_meta[MIGRATION_META_CLAIM_ID_KEY] = original_claim_id

        document = Document(
            form_id=form_id,
            meta=document_meta,
            created_by_user=created_by_user,
            created_by_group=created_by_group,
        )
        closed_by_group = None
        closed_by_user = None
        closed_at = None

        if parent_init_status == WorkItem.STATUS_CANCELED:
            if task_id != settings.ADDITIONAL_DEMAND["FILL_TASK"]:
                closed_by_group = case.family.nfd_work_item.closed_by_group
            closed_by_user = case.family.nfd_work_item.closed_by_user
            closed_at = case.family.nfd_work_item.closed_at

        work_item = WorkItem(
            task_id=task_id,
            name=WORK_ITEM_NAME_MAPPING.get(task_id),
            status=parent_init_status,
            case=case,
            document=document,
            previous_work_item=previous_work_item,
            addressed_groups=addressed_groups,
            assigned_users=assigned_users if assigned_users else [],
            controlling_groups=controlling_groups,
            meta=work_item_meta,
            created_by_user=created_by_user,
            created_by_group=created_by_group,
            closed_at=closed_at,
            closed_by_group=closed_by_group,
            closed_by_user=closed_by_user,
        )
        # add a temporary attribute to hold created_at_override
        work_item._temp_created_at = created_at_override
        document._temp_created_at = created_at_override

        return document, work_item

    @staticmethod
    def _get_send_document_answers(document, answers_dict):
        answers_to_create = []
        source_deadline_answer = answers_dict.get("nfd-tabelle-frist")
        source_comment_answer = answers_dict.get("nfd-tabelle-beschreibung")

        if source_deadline_answer and source_deadline_answer.date:
            answers_to_create.append(
                Answer(
                    question_id="additional-demand-deadline",
                    document=document,
                    date=source_deadline_answer.date,
                )
            )
        if source_comment_answer and source_comment_answer.value:
            answers_to_create.append(
                Answer(
                    question_id="additional-demand-comment",
                    document=document,
                    value=source_comment_answer.value,
                )
            )
        return answers_to_create

    @staticmethod
    def _get_fill_document_answers(document, answers_dict):
        answers_to_create = []
        source_comment_answer = answers_dict.get("nfd-tabelle-bemerkung")

        if source_comment_answer and source_comment_answer.value:
            answers_to_create.append(
                Answer(
                    question_id="additional-demand-comment-fill",
                    document=document,
                    value=source_comment_answer.value,
                )
            )

        answers_to_create.append(
            Answer(
                question_id="additional-demand-ech0211",  # needed for the ech changes introduced recently
                document=document,
                value="false",  # Standardwert
            )
        )
        return answers_to_create

    @staticmethod
    def _get_check_document_answers(document, answers_dict, status):
        check_answers_to_create = []

        if status == DONE_STATUS_VALUE:
            decision_answer = Answer(
                question_id="additional-demand-decision",
                document=document,
                value=settings.ADDITIONAL_DEMAND["ANSWERS"]["DECISION"].get(
                    "ACCEPTED", None
                ),
            )
            check_answers_to_create.append(decision_answer)

        check_answers_to_create.append(
            Answer(
                question_id="additional-demand-ech0211",  # needed for the ech changes introduced recently
                document=document,
                value="false",  # Standardwert
            )
        )
        return check_answers_to_create

    @staticmethod
    def migrate_attachments(all_related_attachments, row_pk, fill_document):
        original_claim_id = str(row_pk)

        new_claim_id = str(fill_document.pk)
        migration_timestamp = timezone.now().isoformat()

        attachments_to_update = []
        instance_mapping = defaultdict(list)
        for att in all_related_attachments:
            instance_id = str(att.instance.pk)
            instance_mapping[instance_id].append(str(att.pk))
            try:
                att.context[MIGRATION_META_CLAIM_ID_KEY] = original_claim_id
                att.context[MIGRATION_META_TIMESTAMP_KEY] = migration_timestamp
                att.context["claimId"] = new_claim_id
                attachments_to_update.append(att)

            except Exception as e:
                tqdm.write(
                    f" ERROR: Row {row_pk}: Failed to modify Attachment {att.pk} of Instance ({instance_id}) with new 'claimId':{new_claim_id}. Error: {e}"
                )
        if attachments_to_update:
            Attachment.objects.bulk_update(attachments_to_update, ["context"])

        return instance_mapping

    def bulk_create_init_work_items(self, cases_qs):
        created_map = {}
        batch_size = 2000

        # Use itertools.batched approach (Python 3.12+) to batch iterator data into tuples of size batch_size
        # in order to also call bulk_update on chunks (for more historically accurate created_at)
        # slight performance gain
        # https://docs.python.org/3.12/library/itertools.html#itertools.batched
        batch_count = math.ceil(cases_qs.count() / batch_size)
        for chunk in tqdm(
            batched(cases_qs.iterator(chunk_size=batch_size), batch_size),
            total=batch_count,
            desc="Bulk creating 'init-additional-demand' work items",
            mininterval=5,
        ):
            batch_to_create = []

            for case in chunk:
                nfd_work_item = self._get_nfd_work_item(case)
                if not nfd_work_item:
                    continue

                # get nfd work_item once and add it to the case
                case.nfd_work_item = nfd_work_item

                current_responsible_service_id, current_responsible_username = (
                    self._get_current_responsible_info(case)
                )
                initial_status = self._determine_init_status(case)
                assigned_users = self._get_assigned_users(
                    current_responsible_service_id, case.instance
                )
                init_work_item = self._initialize_additional_demand(
                    case=case,
                    previous_work_item_id=case.nfd_work_item.previous_work_item_id,
                    created_by_group=case.nfd_work_item.created_by_group,  # should be None since it's the applicant
                    created_by_user=case.nfd_work_item.created_by_user,
                    addressed_groups=[current_responsible_service_id],
                    assigned_users=assigned_users,
                    status=initial_status,
                    save=False,
                    created_at_override=case.nfd_work_item.created_at,
                )
                batch_to_create.append(init_work_item)

            if not batch_to_create:
                continue

            created_objects = WorkItem.objects.bulk_create(
                batch_to_create, batch_size=batch_size
            )

            work_items_to_update = []

            for work_item in created_objects:
                created_map[work_item.case_id] = work_item

                if (
                    hasattr(work_item, "_temp_created_at")
                    and work_item._temp_created_at
                ):
                    work_item.created_at = work_item._temp_created_at
                    work_items_to_update.append(work_item)

            if work_items_to_update:
                WorkItem.objects.bulk_update(
                    work_items_to_update, ["created_at"], batch_size=batch_size
                )

        tqdm.write(
            f"Bulk created {len(created_map)} 'init-additional-demand' work items."
        )
        return created_map

    @staticmethod
    def _initialize_additional_demand(
        case,
        previous_work_item_id,
        addressed_groups,
        assigned_users,
        created_by_group=None,
        created_by_user=None,
        original_claim_id=None,
        save=True,
        created_at_override=None,
        status=WorkItem.STATUS_READY,
    ):
        meta = BASE_WORKITEM_META.copy()
        if original_claim_id:
            meta[MIGRATION_META_CLAIM_ID_KEY] = original_claim_id

        closed_at = None
        closed_by_user = None
        closed_by_group = None

        if status == WorkItem.STATUS_CANCELED:
            closed_at = case.nfd_work_item.closed_at
            closed_by_group = case.nfd_work_item.closed_by_group
            closed_by_user = case.nfd_work_item.closed_by_user

        init_work_item = WorkItem(
            task_id=settings.ADDITIONAL_DEMAND["CREATE_TASK"],
            name=WORK_ITEM_NAME_MAPPING.get(settings.ADDITIONAL_DEMAND["CREATE_TASK"]),
            addressed_groups=addressed_groups,
            assigned_users=assigned_users,
            status=status,
            meta=meta,
            case=case,
            previous_work_item_id=previous_work_item_id,
            created_by_user=created_by_user,
            created_by_group=created_by_group,
            closed_at=closed_at,
            closed_by_user=closed_by_user,
            closed_by_group=closed_by_group,
        )

        init_work_item._temp_created_at = created_at_override

        if save:
            init_work_item.save()
            if created_at_override:
                WorkItem.objects.filter(pk=init_work_item.pk).update(
                    created_at=created_at_override
                )

        return init_work_item

    @staticmethod
    def _get_original_owner(answers_dict, user_map):
        authority_answer = answers_dict.get("nfd-tabelle-behoerde")
        original_service_id = (
            str(authority_answer.value)
            if authority_answer and authority_answer.value
            else None
        )

        author_answer = answers_dict.get("nfd-tabelle-autorin")
        original_user_id = (
            author_answer.value if author_answer and author_answer.value else None
        )

        original_username = None

        if original_user_id:
            original_username = user_map.get(str(original_user_id))

        return original_username, original_service_id

    def _run_draft_step(self, context):
        row = context["row"]
        case = context["case"]
        init_work_item = context["init_work_item"]
        parent_init_status = context["parent_init_status"]
        current_responsible_service_id = context["service_id"]
        answers_dict = context["answers_dict"]
        user_map = context["user_map"]
        workflow = context["workflow"]
        original_claim_id = context["original_claim_id"]
        step_data = context["step_data"]

        original_username, original_service_id = self._get_original_owner(
            answers_dict,
            user_map,
        )
        original_assigned_users = self._get_assigned_users(
            original_service_id, case.instance
        )

        self._complete_object(
            obj=init_work_item,
            closed_by_user=row.created_by_user,
            closed_by_group=row.created_by_group,
            closed_at=row.created_at,
            addressed_groups=[original_service_id],
            assigned_users=original_assigned_users,
            original_claim_id=original_claim_id,
        )

        assigned_users = self._get_assigned_users(
            current_responsible_service_id, case.instance
        )

        new_init_work_item = self._initialize_additional_demand(
            case=case,
            previous_work_item_id=init_work_item.pk,
            created_by_group=row.created_by_group,
            created_by_user=row.created_by_user,
            addressed_groups=[current_responsible_service_id],
            assigned_users=assigned_users,
            status=parent_init_status,
            created_at_override=row.created_at,
        )

        step_data["new_init_work_item"] = new_init_work_item

        request_datetime = self._get_datetime_from_answer(
            answers_dict=answers_dict, key="nfd-tabelle-datum-anfrage"
        )

        child_case, additional_demand_work_item = (
            self._create_child_case_and_parent_work_item(
                parent_case=case,
                workflow=workflow,
                previous_work_item=init_work_item,
                # created-by-group is used to display in list, which should correspond to the old module, which showed the last modified
                username=original_username,
                service_id=original_service_id,
                addressed_groups=[current_responsible_service_id],
                assigned_users=assigned_users,
                parent_init_status=parent_init_status,
                created_at_override=request_datetime,
                original_claim_id=original_claim_id,
            )
        )

        send_document, send_work_item = self._create_document_and_work_item(
            case=child_case,
            form_id=SEND_DEMAND_FORM_ID,
            task_id=settings.ADDITIONAL_DEMAND["SEND_TASK"],
            previous_work_item=None,
            addressed_groups=[current_responsible_service_id],
            assigned_users=assigned_users,
            controlling_groups=[],
            created_by_user=row.created_by_user,
            created_by_group=row.created_by_group,
            created_at_override=request_datetime,
            parent_init_status=parent_init_status,
            original_claim_id=original_claim_id,
        )

        context["documents_to_create"].append(send_document)

        answers_to_create = self._get_send_document_answers(
            document=send_document, answers_dict=answers_dict
        )
        if answers_to_create:
            context["answers_to_create"].extend(answers_to_create)

        context["work_items_to_create"].append(send_work_item)

        context["step_data"]["child_case"] = child_case
        context["step_data"]["additional_demand_work_item"] = (
            additional_demand_work_item
        )
        context["step_data"]["send_work_item"] = send_work_item
        context["step_data"]["send_document"] = send_document
        context["step_data"]["send_answers"] = answers_to_create
        context["step_data"]["original_username"] = original_username
        context["step_data"]["original_service_id"] = original_service_id

    def _run_in_progress_step(self, context):
        case = context["case"]
        current_responsible_service_id = context["service_id"]
        answers_dict = context["answers_dict"]
        parent_init_status = context["parent_init_status"]
        original_claim_id = context["original_claim_id"]
        step_data = context["step_data"]

        send_work_item = step_data["send_work_item"]
        child_case = step_data["child_case"]
        original_username = step_data["original_username"]
        original_service_id = step_data["original_service_id"]

        request_datetime = self._get_datetime_from_answer(
            answers_dict=answers_dict, key="nfd-tabelle-datum-anfrage"
        )

        self._complete_object(
            obj=send_work_item,
            closed_by_user=original_username,
            closed_by_group=original_service_id,
            closed_at=request_datetime,
            addressed_groups=[original_service_id],
            assigned_users=self._get_assigned_users(original_service_id, case.instance),
            save=False,
        )

        is_paper = getattr(case, "is_paper_annotated", False)
        fill_document, fill_work_item = self._create_document_and_work_item(
            case=child_case,
            form_id=FILL_DEMAND_FORM_ID,
            task_id=settings.ADDITIONAL_DEMAND["FILL_TASK"],
            previous_work_item=send_work_item,
            addressed_groups=[current_responsible_service_id] if is_paper else [],
            assigned_users=self._get_assigned_users(
                current_responsible_service_id, case.instance
            )
            if is_paper
            else [],
            controlling_groups=[current_responsible_service_id],
            created_by_group=send_work_item.closed_by_group,
            created_by_user=send_work_item.closed_by_user,
            created_at_override=request_datetime,
            parent_init_status=parent_init_status,
            original_claim_id=original_claim_id,
        )

        context["documents_to_create"].append(fill_document)

        answers_to_create = self._get_fill_document_answers(
            document=fill_document, answers_dict=answers_dict
        )
        context["answers_to_create"].extend(answers_to_create)

        context["work_items_to_create"].append(fill_work_item)

        context["step_data"]["fill_work_item"] = fill_work_item
        context["step_data"]["fill_document"] = fill_document
        context["step_data"]["fill_answers"] = answers_to_create

    def _run_answered_step(self, context):
        row_attachments = context["row_attachments"]
        case = context["case"]
        answers_dict = context["answers_dict"]
        status = context["status"]
        parent_init_status = context["parent_init_status"]
        original_claim_id = context["original_claim_id"]
        current_responsible_service_id = context["service_id"]
        step_data = context["step_data"]

        child_case = step_data["child_case"]
        fill_work_item = step_data["fill_work_item"]
        original_service_id = step_data["original_service_id"]

        response_datetime = self._get_datetime_from_answer(
            answers_dict=answers_dict, key="nfd-tabelle-datum-antwort"
        )
        source_comment_answer = answers_dict.get("nfd-tabelle-bemerkung")
        latest_attachment = row_attachments[0] if row_attachments else None
        is_paper = getattr(case, "is_paper_annotated", False)

        closed_at = (
            source_comment_answer.modified_at
            if source_comment_answer
            else latest_attachment.date
            if latest_attachment
            else response_datetime
        )

        source_comment_created_at = (
            source_comment_answer.created_at.replace(microsecond=0, second=0)
            if source_comment_answer
            else None
        )
        source_comment_modified_at = (
            source_comment_answer.modified_at.replace(microsecond=0, second=0)
            if source_comment_answer
            else None
        )
        attachment_date = (
            latest_attachment.date.replace(microsecond=0, second=0)
            if latest_attachment
            else None
        )

        # If the closed-by information cannot be determined accurately, we
        # don't include the information.
        closed_by_user = None
        closed_by_group = None

        # If the comment answer hasn't been updated since creation, use the
        # modified-by-user and modified-by-group fields, since they are accurate
        # on creation and were always written when answering a claim. The
        # modified-by fields haven't been updated properly in caluma, so as
        # soon as the answer was updated through a re-open, we can't use it
        # anymore.
        if source_comment_answer and (
            source_comment_created_at == source_comment_modified_at
        ):
            closed_by_user = source_comment_answer.modified_by_user
            if is_paper:
                closed_by_group = source_comment_answer.modified_by_group

        # If an attachment was uploaded with the latest answer of the claim,
        # use the user and service information on the latest attachment
        elif latest_attachment and (attachment_date == source_comment_modified_at):
            if latest_attachment.user:
                closed_by_user = latest_attachment.user.username

            if is_paper and latest_attachment.service:
                closed_by_group = str(latest_attachment.service.pk)

        self._complete_object(
            obj=fill_work_item,
            closed_by_user=closed_by_user,
            closed_by_group=closed_by_group,
            closed_at=closed_at,
            addressed_groups=[original_service_id] if is_paper else [],
            controlling_groups=[original_service_id],
            assigned_users=self._get_assigned_users(original_service_id, case.instance)
            if is_paper
            else [],
            save=False,
        )

        check_document, check_work_item = self._create_document_and_work_item(
            case=child_case,
            form_id=CHECK_DEMAND_FORM_ID,
            task_id=settings.ADDITIONAL_DEMAND["CHECK_TASK"],
            previous_work_item=fill_work_item,
            addressed_groups=[current_responsible_service_id],
            controlling_groups=[current_responsible_service_id],
            assigned_users=self._get_assigned_users(
                current_responsible_service_id, case.instance
            ),
            created_by_user=fill_work_item.closed_by_user,
            created_by_group=fill_work_item.closed_by_group,
            created_at_override=fill_work_item.closed_at,
            parent_init_status=parent_init_status,
            original_claim_id=original_claim_id,
        )

        context["documents_to_create"].append(check_document)

        answers_to_create = self._get_check_document_answers(
            document=check_document, answers_dict=answers_dict, status=status
        )
        context["answers_to_create"].extend(answers_to_create)
        context["work_items_to_create"].append(check_work_item)
        context["step_data"]["check_work_item"] = check_work_item
        context["step_data"]["check_document"] = check_document
        context["step_data"]["check_answers"] = answers_to_create

    def _run_done_step(self, context):
        case = context["case"]
        step_data = context["step_data"]
        answers_dict = context["answers_dict"]

        check_work_item = step_data["check_work_item"]
        child_case = step_data["child_case"]
        additional_demand_work_item = step_data["additional_demand_work_item"]
        original_username = step_data["original_username"]
        original_service_id = step_data["original_service_id"]

        response_datetime = self._get_datetime_from_answer(
            answers_dict=answers_dict, key="nfd-tabelle-datum-antwort"
        )
        source_status_answer = answers_dict.get("nfd-tabelle-status")

        final_closed_at = (
            source_status_answer.modified_at
            if source_status_answer
            else case.nfd_work_item.closed_at or response_datetime
        )

        self._complete_object(
            obj=check_work_item,
            closed_by_user=original_username,
            closed_by_group=original_service_id,
            addressed_groups=[original_service_id],
            controlling_groups=[original_service_id],
            assigned_users=self._get_assigned_users(original_service_id, case.instance),
            closed_at=final_closed_at,
            save=False,
        )

        self._complete_object(
            obj=additional_demand_work_item,
            closed_by_user=original_username,
            closed_by_group=original_service_id,
            addressed_groups=[original_service_id],
            controlling_groups=[original_service_id],
            assigned_users=self._get_assigned_users(original_service_id, case.instance),
            closed_at=final_closed_at,
        )

        self._complete_object(
            obj=child_case,
            closed_by_user=original_username,
            closed_by_group=original_service_id,
            closed_at=final_closed_at,
        )

    def process_nfd_row(
        self,
        row,
        init_work_item,
        parent_init_status,
        case,
        current_responsible_service_id,
        current_responsible_username,
        status,
        answers_dict,
        user_map,
        row_attachments,
        all_related_attachments,
        workflow,
        batch_data,
    ):
        context = {
            "row": row,
            "init_work_item": init_work_item,
            "parent_init_status": parent_init_status,
            "case": case,
            "service_id": current_responsible_service_id,
            "username": current_responsible_username,
            "answers_dict": answers_dict,
            "status": status,
            "user_map": user_map,
            "row_attachments": row_attachments,
            "workflow": workflow,
            "original_claim_id": str(row.pk),
            "documents_to_create": [],
            "answers_to_create": [],
            "work_items_to_create": [],
            "step_data": {},
        }

        steps_to_run = self.STEP_MAP.get(status)
        if not steps_to_run:
            return init_work_item, {}

        try:
            for step_function in steps_to_run:
                step_function(context)

            batch_data["documents"].extend(context["documents_to_create"])
            batch_data["answers"].extend(context["answers_to_create"])
            batch_data["work_items"].extend(context["work_items_to_create"])

            if "fill_document" in context["step_data"]:
                batch_data["attachment_tasks"].append(
                    (
                        all_related_attachments,
                        row.pk,
                        context["step_data"]["fill_document"],
                    )
                )

        except Exception as e:
            tqdm.write(
                f"\n ERROR: FAILED Instance {case.instance.pk}, Case {case.pk}, Row {row.pk}: Error: {e}"
            )
            tqdm.write(traceback.format_exc())
            raise
        next_work_item = context["step_data"].get("new_init_work_item", init_work_item)
        return next_work_item, context["step_data"]

    @staticmethod
    def _build_author_user_map(document_list):
        author_user_ids = {
            answer.value
            for document in document_list
            # the answers have already been prefetched before calling this method
            for answer in document.answers.all()
            if answer.question_id == "nfd-tabelle-autorin" and answer.value
        }

        user_map = {
            str(user.pk): user.username
            for user in User.objects.filter(pk__in=author_user_ids)
        }

        return user_map

    def _get_current_responsible_info(self, case):
        current_responsible_service = case.instance.responsible_service(
            filter_type="municipality"
        )
        current_responsible_service_id = str(current_responsible_service.pk)

        current_user_usernames = self.responsible_user(
            service_id=current_responsible_service_id, instance=case.instance
        )
        current_responsible_username = (
            current_user_usernames[0] if current_user_usernames else None
        )  # take username of first resp user

        return current_responsible_service_id, current_responsible_username

    @staticmethod
    def _get_row_status(init_status, answers_dict, row_attachments):
        # Heuristic to determine what happens for incomplete entries
        has_service = (
            answers_dict.get("nfd-tabelle-behoerde")
            and answers_dict.get("nfd-tabelle-behoerde").value
        )

        # If there is no service answer in the row it means it's an empty row so we want to skip processing
        # by returning a status not in self.STEP_MAP
        if not has_service:
            return "skipped"

        status_answer = answers_dict.get("nfd-tabelle-status")
        status_value = status_answer.value if status_answer else None

        # trust status value if present
        if status_value:
            return status_value

        has_response_date = (
            answers_dict.get("nfd-tabelle-datum-antwort")
            and answers_dict.get("nfd-tabelle-datum-antwort").date
        )
        has_applicant_comment = (
            answers_dict.get("nfd-tabelle-bemerkung")
            and answers_dict.get("nfd-tabelle-bemerkung").value
        )

        has_attachment = len(row_attachments) > 0

        # check for response date/comment/attachment if there is no status
        if any(
            (
                has_response_date,
                has_applicant_comment,
                has_attachment,
            )
        ):
            return ANSWERED_STATUS_VALUE

        # for canceled instances with incomplete entries and no indication of response,
        # we want to show the entry so we return status in progress
        # because the canceled draft additional-demand entries will not be shown
        is_closed_for_editing = init_status in [
            WorkItem.STATUS_SUSPENDED,
            WorkItem.STATUS_CANCELED,
        ]
        if is_closed_for_editing:
            return IN_PROGRESS_STATUS_VALUE

        return DRAFT_STATUS_VALUE

    def _transfer_batch_to_db(self, batch_data, case):  # noqa: C901
        attachment_summary = {}
        try:
            if batch_data["documents"]:
                created_documents = Document.objects.bulk_create(
                    batch_data["documents"]
                )
                documents_to_update = []
                for document in created_documents:
                    if document._temp_created_at:
                        document.created_at = document._temp_created_at
                        documents_to_update.append(document)
                if documents_to_update:
                    Document.objects.bulk_update(documents_to_update, ["created_at"])

            if batch_data["answers"]:
                Answer.objects.bulk_create(batch_data["answers"])

            if batch_data["work_items"]:
                created_work_items = WorkItem.objects.bulk_create(
                    batch_data["work_items"]
                )
                work_items_to_update = []
                # use the temporary attribute to update created_at with created_at_override
                for work_item in created_work_items:
                    if work_item._temp_created_at:
                        work_item.created_at = work_item._temp_created_at
                        work_items_to_update.append(work_item)
                if work_items_to_update:
                    WorkItem.objects.bulk_update(work_items_to_update, ["created_at"])

            if batch_data["attachment_tasks"]:
                for all_related_attachments, row_pk, fill_document in batch_data[
                    "attachment_tasks"
                ]:
                    attachment_info = self.migrate_attachments(
                        all_related_attachments=all_related_attachments,
                        row_pk=row_pk,
                        fill_document=fill_document,
                    )
                    attachment_summary[str(row_pk)] = attachment_info

        except Exception as e:
            tqdm.write(
                f"ERROR: Instance {case.instance.pk}: ERROR while transferring to database: {str(e)}"
            )
            tqdm.write(traceback.format_exc())
            raise

        return attachment_summary

    def migrate_case(
        self, case, workflow, init_work_item, global_attachments_map, global_rows_map
    ):
        current_responsible_service_id, current_responsible_username = (
            self._get_current_responsible_info(case)
        )

        nfd_table_rows = global_rows_map.get(case.pk, [])

        user_map = self._build_author_user_map(nfd_table_rows)
        attachments_map = self._build_attachments_map(case)
        current_init_work_item = init_work_item
        parent_init_status = init_work_item.status

        batch_data = {
            "documents": [],
            "answers": [],
            "work_items": [],
            "attachment_tasks": [],
        }
        # used for logging
        case_trace_data = {"rows": {}, "init_work_item": init_work_item}

        if nfd_table_rows:
            for row in nfd_table_rows:
                answers_dict = {
                    answer.question_id: answer for answer in row.answers.all()
                }
                row_attachments = attachments_map.get(str(row.pk), [])
                all_related_attachments = global_attachments_map.get(str(row.pk), [])
                status = self._get_row_status(
                    init_status=parent_init_status,
                    answers_dict=answers_dict,
                    row_attachments=row_attachments,
                )
                try:
                    next_init_work_item, step_data = self.process_nfd_row(
                        row=row,
                        init_work_item=current_init_work_item,
                        parent_init_status=parent_init_status,
                        case=case,
                        current_responsible_service_id=current_responsible_service_id,
                        current_responsible_username=current_responsible_username,
                        status=status,
                        answers_dict=answers_dict,
                        user_map=user_map,
                        row_attachments=row_attachments,
                        all_related_attachments=all_related_attachments,
                        workflow=workflow,
                        batch_data=batch_data,
                    )

                    if next_init_work_item:
                        current_init_work_item = next_init_work_item

                    case_trace_data["rows"][str(row.pk)] = step_data

                except Exception as e:
                    tqdm.write(
                        f"\n ERROR: FAILED to migrate Row PK {row.pk} for Instance {case.instance.pk}, Case {case.pk}: {str(e)}"
                    )
            attachment_summary = self._transfer_batch_to_db(
                batch_data=batch_data, case=case
            )
            self._log_case_summary(
                case=case,
                case_trace_data=case_trace_data,
                attachment_summary=attachment_summary,
            )
        else:
            # log init additional demand work item (already created with bulk-create).
            self._log_case_summary(
                case=case, case_trace_data=case_trace_data, attachment_summary={}
            )

        case.meta[MIGRATION_META_TIMESTAMP_KEY] = timezone.now().isoformat()
        case.save(update_fields=["meta"])

    @staticmethod
    def _format_work_item_log(step_data, work_item_key):
        if work_item_key not in step_data:
            return None

        work_item = step_data[work_item_key]
        message = (
            f"- {work_item.task_id} work item: {work_item.pk} ({work_item.status})"
        )
        return textwrap.indent(message, INDENT)

    @staticmethod
    def _format_document_log(step_data, document_key, answers_key):
        if document_key not in step_data:
            return None

        document = step_data[document_key]
        answers_list = step_data.get(answers_key, [])

        log_lines = [f"- {document.form_id} document: {document.pk}"]

        answers_info = [
            (str(answer.question_id), str(answer.pk)) for answer in answers_list
        ]

        if answers_info:
            message = f"- {document.form_id} document answers: {answers_info}"
            log_lines.append(textwrap.indent(message, INDENT))

        full_block = "\n".join(log_lines)
        return textwrap.indent(full_block, INDENT)

    @staticmethod
    def _format_attachment_log(row_pk, attachment_summary):
        row_attachments = attachment_summary.get(str(row_pk), {})
        log_lines = []

        if row_attachments:
            log_lines.append("- Attachments:")
            for instance_id, attachment_ids in row_attachments.items():
                message = f"- Instance ({instance_id}): {attachment_ids}"
                log_lines.append(textwrap.indent(message, INDENT))
        else:
            log_lines.append("- Attachments: [NO ATTACHMENTS TO MIGRATE]")

        full_block = "\n".join(log_lines)
        return textwrap.indent(full_block, INDENT)

    def _log_case_summary(self, case, case_trace_data, attachment_summary):
        if self.logging_disabled:
            return

        # header
        log_lines = [f" Instance ({case.instance.pk}), Case: ({case.pk}):"]

        init_work_item = case_trace_data.get("init_work_item")
        if init_work_item:
            init_work_item_message = f"- {init_work_item.task_id} work item: {init_work_item.pk} ({init_work_item.status})"
            log_lines.append(textwrap.indent(init_work_item_message, INDENT))
        else:
            init_work_item_message = (
                "- init-additional-demand work item: [ERROR: NOT CREATED]"
            )
            log_lines.append(textwrap.indent(init_work_item_message, INDENT))

        rows_data = case_trace_data.get("rows", {})
        row_count = len(rows_data)

        row_count_message = f"- NFD Rows Count: {row_count}"
        log_lines.append(textwrap.indent(row_count_message, INDENT))

        for row_pk, step_data in rows_data.items():
            row_header = f"- NFD Row ({row_pk}):"
            log_lines.append(textwrap.indent(row_header, INDENT))

            row_lines = []

            top_work_item_keys = ["new_init_work_item", "additional_demand_work_item"]

            # new_init_work_item and parent_work_item
            for key in top_work_item_keys:
                row_lines.append(
                    self._format_work_item_log(
                        step_data=step_data,
                        work_item_key=key,
                    )
                )

            # child case
            if "child_case" in step_data:
                child_case = step_data["child_case"]
                child_case_message = f"- {child_case.workflow_id} child case: {child_case.pk} ({child_case.status})"
                row_lines.append(textwrap.indent(child_case_message, INDENT))

            stages = ["send", "fill", "check"]

            for stage in stages:
                # child work item
                row_lines.append(
                    self._format_work_item_log(
                        step_data=step_data,
                        work_item_key=f"{stage}_work_item",
                    )
                )

                # document and answers
                row_lines.append(
                    self._format_document_log(
                        step_data=step_data,
                        document_key=f"{stage}_document",
                        answers_key=f"{stage}_answers",
                    )
                )

            # attachments
            row_lines.append(
                self._format_attachment_log(
                    row_pk=row_pk, attachment_summary=attachment_summary
                )
            )

            full_row_block = "\n".join(filter(None, row_lines))
            log_lines.append(textwrap.indent(full_row_block, INDENT))

        tqdm.write("\n".join(log_lines))

    @staticmethod
    def get_cases_to_migrate(only_ids=None):
        nfd_work_item_qs = WorkItem.objects.filter(
            case_id=OuterRef("pk"), task_id="nfd"
        ).order_by("-created_at")

        nfd_prefetch = Prefetch(
            "work_items",
            queryset=WorkItem.objects.filter(task_id="nfd").order_by("-created_at"),
            to_attr="nfd_work_items_list",
        )

        attachments_qs = (
            Attachment.objects.filter(context__has_key="claimId")
            .order_by("-date")
            .select_related("user")
        )

        attachments_prefetch = Prefetch(
            "instance__attachments",
            queryset=attachments_qs,
            to_attr="claim_attachments_list",
        )
        submit_work_item = WorkItem.objects.filter(
            case_id=OuterRef("pk"),
            task_id=PRECEDING_TASK,
            status__in=[WorkItem.STATUS_COMPLETED, WorkItem.STATUS_SKIPPED],
        ).order_by("-created_at")

        is_paper_qs = Answer.objects.filter(
            document__case=OuterRef("pk"), question_id="is-paper", value="is-paper-yes"
        )

        base_qs = (
            Case.objects.annotate(
                submit_work_item_id=Subquery(submit_work_item.values("pk")[:1]),
                is_paper_annotated=Exists(is_paper_qs),
            )
            .select_related("instance", "instance__instance_state")
            .prefetch_related(attachments_prefetch, nfd_prefetch)
            .order_by("pk")
        )

        if only_ids is not None:
            return base_qs.filter(pk__in=only_ids)

        tqdm.write("Finding cases to migrate...")

        is_not_migrated = ~Q(meta__has_key=MIGRATION_META_TIMESTAMP_KEY)

        additional_demand_exists = Exists(
            WorkItem.objects.filter(
                case_id=OuterRef("pk"),
                task_id=settings.ADDITIONAL_DEMAND["CREATE_TASK"],
            )
        )
        return (
            base_qs.filter(
                Exists(nfd_work_item_qs),
                is_not_migrated,
            )
            .exclude(additional_demand_exists)
            .exclude(instance__isnull=True)
            .exclude(workflow_id="migrated")
        )

    @staticmethod
    def _get_nfd_work_item(case):
        nfd_work_items = getattr(case, "nfd_work_items_list", [])
        return nfd_work_items[0] if nfd_work_items else None

    @transaction.atomic
    def handle(self, *args, **options):  # noqa: C901
        self.logging_disabled = options.get("no_logging")

        if options.get("reset"):
            self.reset()
            self.stdout.write(self.style.SUCCESS("\n Reset complete."))
            return

        sid = transaction.savepoint()
        do_commit = options.get("commit")

        if not do_commit:
            self.stdout.write(
                self.style.WARNING(
                    "\n DRY RUN MODE: No changes will be saved to the database.\n"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "\n LIVE MODE: Changes WILL be committed to the database!!!\n"
                )
            )

        try:
            workflow = Workflow.objects.get(pk=settings.ADDITIONAL_DEMAND["WORKFLOW"])
        except Workflow.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f" CRITICAL: Workflow {settings.ADDITIONAL_DEMAND['WORKFLOW']} not found. Aborting migration."
                )
            )  # probably not needed.
            return

        # get the initial queryset that filters cases without init work items
        cases_qs_initial = self.get_cases_to_migrate()

        case_ids = list(cases_qs_initial.values_list("pk", flat=True))

        case_count = len(case_ids)
        if not case_count:
            self.stdout.write(
                self.style.SUCCESS("No new cases found needing migration.")
            )
            return

        tqdm.write(f"Found {case_count} cases to migrate.")

        # filter the initially retrieved ids in order to be able to iterate over the same queryset after we create init work items
        # otherwise, there is a filter in place that excludes cases with init work items
        cases_to_process = self.get_cases_to_migrate(only_ids=case_ids)

        all_rows_qs = (
            Document.objects.filter(
                form_id="nfd-tabelle",
                family__work_item__task_id="nfd",
                family__work_item__case__in=cases_to_process,
            )
            .select_related("family__work_item")
            .prefetch_related("answers")
        )

        global_rows_map = defaultdict(list)
        all_row_ids = []

        for row in all_rows_qs:
            case_id = row.family.work_item.case_id
            global_rows_map[case_id].append(row)

            all_row_ids.append(str(row.pk))

        self.stdout.write(
            f"Mapped {len(all_row_ids)} rows across {len(global_rows_map)} cases."
        )

        # Query for all attachments that point to the original claim document
        # All attachments that point to the original claim document should also be migrated.
        # This is needed for example for copied attachments of project modification.

        all_attachments_qs = Attachment.objects.filter(context__claimId__in=all_row_ids)
        global_attachments_map = defaultdict(list)

        count = 0
        for att in all_attachments_qs.iterator():
            claim_id = att.context.get("claimId")
            if claim_id:
                global_attachments_map[str(claim_id)].append(att)
                count += 1

        self.stdout.write(
            f"Mapped {count} attachments to {len(global_attachments_map)} rows."
        )
        init_work_item_map = self.bulk_create_init_work_items(cases_to_process)

        for case in tqdm(
            cases_to_process.iterator(chunk_size=2000),
            total=case_count,
            desc="Migrating NFD cases",
            mininterval=5,
        ):
            try:
                nfd_work_item = self._get_nfd_work_item(case)
                if not nfd_work_item:
                    continue

                # get nfd work_item once and add it to the case
                case.nfd_work_item = nfd_work_item

                init_work_item = init_work_item_map.get(case.pk)
                self.migrate_case(
                    case=case,
                    workflow=workflow,
                    init_work_item=init_work_item,
                    global_attachments_map=global_attachments_map,
                    global_rows_map=global_rows_map,
                )
            except Exception as e:
                tqdm.write(
                    f"\n ERROR: FAILED to migrate Instance {case.instance.pk}, Case {case.pk}: {str(e)}"
                )
                continue

        if do_commit:
            self.stdout.write(self.style.SUCCESS("\nCommitting changes to database..."))
            transaction.savepoint_commit(sid)
            self.stdout.write(self.style.SUCCESS("Done."))
        else:
            self.stdout.write(
                self.style.WARNING("\nRolling back all changes (DRY RUN)...")
            )
            transaction.savepoint_rollback(sid)
            self.stdout.write(self.style.WARNING("Done. Database is unchanged."))
