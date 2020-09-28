from copy import copy
from functools import reduce
from logging import getLogger

from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import (
    api as caluma_workflow_api,
    models as caluma_workflow_models,
)
from caluma.caluma_workflow.utils import get_jexl_groups
from django.conf import settings
from django.db.models import Q
from jwt import decode as jwt_decode

from camac.user.middleware import get_group
from camac.user.models import Service, User

APPLICANT_GROUP_ID = 6

log = getLogger(__name__)


class CalumaApi:
    """
    Class with helper methods to interact with Caluma.

    Initially this was meant as a wrapper for all interactions with Caluma (including
    the models). This is not the case anymore. Instead this class is meant to contain
    convenience methods for more involved caluma interactions or project specific
    meta lookups.
    """

    def _get_main_form(self, instance):
        try:
            return caluma_workflow_models.Case.objects.get(
                **{"meta__camac-instance-id": instance.pk}
            ).document.form
        except caluma_workflow_models.Case.DoesNotExist:
            return None

    def get_form_name(self, instance):
        form = self._get_main_form(instance)
        return form.name if form else None

    def get_form_slug(self, instance):
        form = self._get_main_form(instance)
        return form.slug if form else None

    def _get_main_document(self, instance):
        return caluma_workflow_models.Case.objects.get(
            **{"meta__camac-instance-id": instance.pk}
        ).document

    def get_main_document(self, instance):
        document = self._get_main_document(instance)
        return document.pk if document else None

    def get_source_document_value(self, document_id, field):
        source = caluma_form_models.Document.objects.get(pk=document_id).source
        return getattr(source, field, None) if source else None

    def delete_instance_case(self, instance_id):
        return caluma_workflow_models.Case.objects.filter(
            **{"family__meta__camac-instance-id": instance_id}
        ).delete()

    def get_ebau_number(self, instance):
        case = caluma_workflow_models.Case.objects.filter(
            **{"meta__camac-instance-id": instance.pk}
        ).first()
        return case.meta.get("ebau-number", "-") if case else None

    def get_municipality(self, instance):
        answer = caluma_form_models.Answer.objects.filter(
            **{
                "document__case__meta__camac-instance-id": instance.pk,
                "question_id": "gemeinde",
            }
        ).first()

        return answer.value if answer else None

    def get_nfd_form_permissions(self, instance):
        permissions = set()

        answers = caluma_form_models.Answer.objects.filter(
            **{
                "question_id": "nfd-tabelle-status",
                "document__family__form_id": "nfd",
                "document__family__work_item__case__family__meta__camac-instance-id": instance.pk,
            }
        )

        if answers.exclude(value="nfd-tabelle-status-entwurf").exists():
            permissions.add("read")

        if answers.filter(value="nfd-tabelle-status-in-bearbeitung").exists():
            permissions.add("read")
            permissions.add("write")

        return permissions

    def copy_document(self, source_pk, exclude_form_slugs=None, meta=None, **kwargs):
        """Use to `copy()` function on a document and do some clean-up.

        Caution: `exclude_form_slugs` is only excluding top-level questions
        and doesn't do additional clean-up on nested documents from
        table questions. That's based on the assumption that there are no table
        questions in the excluded form.
        """
        source = caluma_form_models.Document.objects.get(pk=source_pk)
        document = source.copy(**kwargs)

        if exclude_form_slugs:
            document.answers.filter(question__forms__in=exclude_form_slugs).delete()

        # prevent creating a historical record
        document.skip_history_when_saving = True
        try:
            document.save()
        finally:
            del document.skip_history_when_saving

        return document

    def update_or_create_answer(self, document_id, question_slug, value):
        return caluma_form_models.Answer.objects.update_or_create(
            document_id=document_id,
            question_id=question_slug,
            defaults={"value": value},
        )

    def set_submit_date(self, instance_id, submit_date):
        case = caluma_workflow_models.Case.objects.get(
            **{"meta__camac-instance-id": instance_id}
        )

        if "submit-date" in case.meta:  # pragma: no cover
            # instance was already submitted, this is probably a re-submit
            # after correction.
            return False

        new_meta = {
            **case.meta,
            # Caluma date is formatted yyyy-mm-dd so it can be sorted
            "submit-date": submit_date,
        }

        case.meta = new_meta
        case.save()

        return True

    def is_paper(self, instance):
        return caluma_form_models.Answer.objects.filter(
            **{
                "document__case__meta__camac-instance-id": instance.pk,
                "question_id": "papierdossier",
                "value": "papierdossier-ja",
            }
        ).exists()

    def is_modification(self, instance):
        return caluma_form_models.Answer.objects.filter(
            **{
                "document__case__meta__camac-instance-id": instance.pk,
                "question_id": "projektaenderung",
                "value": "projektaenderung-ja",
            }
        ).exists()

    def get_circulation_proposals(self, instance):
        # [(question_id, option, suggested service), ... ]
        suggestions = settings.APPLICATION.get("SUGGESTIONS", [])
        if not suggestions:  # pragma: no cover
            return set()

        suggestion_map = {
            (q_slug, answer): services for q_slug, answer, services in suggestions
        }

        document = self._get_main_document(instance)
        answers = caluma_form_models.Answer.objects.filter(
            document__family=document.family
        )

        _filter = reduce(
            lambda a, b: a | b,
            [
                Q(question_id=q_slug, value=answer)
                | Q(question_id=q_slug, value__contains=answer)
                for q_slug, answer, _ in suggestions
            ],
            Q(pk=None),
        )
        answers = answers.filter(_filter)

        suggestions_out = {
            service
            for ans in answers.filter(
                question__type=caluma_form_models.Question.TYPE_MULTIPLE_CHOICE
            )
            for choice in ans.value
            for service in suggestion_map.get((ans.question_id, choice), [])
        }
        suggestions_out.update(
            {
                service
                for ans in answers.exclude(
                    question__type=caluma_form_models.Question.TYPE_MULTIPLE_CHOICE
                )
                for service in suggestion_map.get((ans.question_id, ans.value), [])
            }
        )
        return suggestions_out

    def copy_table_answer(
        self,
        source_question,
        target_question,
        source_document,
        target_document,
        source_question_fallback=None,
    ):
        # get the source answer with a fallback
        table_answer = source_document.answers.filter(
            question_id=source_question
        ).first()

        if not table_answer or table_answer.documents.count() == 0:
            table_answer = source_document.answers.filter(
                question_id=source_question_fallback
            ).first()

        # nothing to copy
        if not table_answer or table_answer.documents.count() == 0:  # pragma: no cover
            return

        # create a new table answer in the target document
        new_table_answer = caluma_form_models.Answer.objects.create(
            document_id=target_document.pk, question_id=target_question
        )

        # copy all rows into the new table answer
        for row in table_answer.documents.all():
            sb_row = self.copy_document(row.id, family=target_document.family)
            new_table_answer.documents.add(sb_row)

    def _sync_activations(self, child_case, activations, user):
        caluma_settings = settings.APPLICATION.get("CALUMA", {})
        activation_task = caluma_workflow_models.Task.objects.get(
            pk=caluma_settings.get("ACTIVATION_INIT_TASK")
        )

        for activation in activations:
            work_item = child_case.work_items.filter(
                **{"task": activation_task, "meta__activation-id": activation.pk}
            ).first()

            update_data = {
                "description": activation.reason,
                "deadline": activation.deadline_date,
                "addressed_groups": get_jexl_groups(
                    activation_task.address_groups,
                    activation_task,
                    child_case,
                    user,
                    None,
                    {"activation-id": activation.pk},
                ),
                "controlling_groups": get_jexl_groups(
                    activation_task.control_groups,
                    activation_task,
                    child_case,
                    user,
                    None,
                    {"activation-id": activation.pk},
                ),
            }

            if work_item:
                # Activation work item already exists, synchronize with activation
                for key, value in update_data.items():
                    setattr(work_item, key, value)

                work_item.save()
            else:
                # Activation work item does not exist yet, create a new one
                child_case.work_items.create(
                    task=activation_task,
                    status=caluma_workflow_models.WorkItem.STATUS_READY,
                    created_by_user=user.username,
                    created_by_group=user.group,
                    name=activation_task.name,
                    meta={
                        "activation-id": activation.pk,
                        "not-viewed": True,
                        "notify-completed": False,
                        "notify-deadline": True,
                    },
                    **update_data,
                )

        # Note: The activation_ids need to be strings in order for the
        # query to filter correctly (jsonb type casting...)
        activation_ids = list(activations.values_list("pk", flat=True))
        for existing_work_item in child_case.work_items.filter(
            task=activation_task, status=caluma_workflow_models.WorkItem.STATUS_READY
        ):
            # Cancel existing activation work items that don't have an
            # activation anymore.
            if existing_work_item.meta.get("activation-id") not in activation_ids:
                caluma_workflow_api.cancel_work_item(existing_work_item, user)

    def sync_circulation(self, circulation, user):
        """Synchronize a CAMAC circulation with the Caluma workflow.

        This method completely synchronizes the Caluma workflow with an
        existing CAMAC circulation. If there are activations in the
        circulation it creates work items in an existing (or newly created)
        child case. If there are work items for non existing activations it
        cancels them. And if there is a child case but no more activations
        the whole child case will be canceled.
        """

        caluma_settings = settings.APPLICATION.get("CALUMA", {})

        work_item = caluma_workflow_models.WorkItem.objects.filter(
            **{
                "task_id": caluma_settings.get("CIRCULATION_TASK"),
                "case__meta__camac-instance-id": circulation.instance.pk,
                "meta__circulation-id": circulation.pk,
            }
        ).first()

        if not work_item:
            log.error(f"No work item found for circulation {circulation.pk}")
            return

        if circulation.activations.exists():
            # Get or create a child case for the circulation
            child_case = work_item.child_case or caluma_workflow_api.start_case(
                workflow=caluma_workflow_models.Workflow.objects.get(
                    pk=caluma_settings.get("CIRCULATION_WORKFLOW")
                ),
                form=caluma_form_models.Form.objects.get(
                    pk=caluma_settings.get("CIRCULATION_FORM")
                ),
                user=user,
                parent_work_item=work_item,
                context={"activation-id": circulation.activations.first().pk},
            )

            self._sync_activations(child_case, circulation.activations.all(), user)

        elif work_item.child_case:
            # Cancel existing child case since there are no more activations
            caluma_workflow_api.cancel_case(work_item.child_case, user)

    def reassign_work_items(self, instance_id, from_group_id, to_group_id):
        from_group_id = str(from_group_id)
        to_group_id = str(to_group_id)

        for groups_type in ["addressed_groups", "controlling_groups"]:
            for work_item in caluma_workflow_models.WorkItem.objects.filter(
                **{
                    f"{groups_type}__contains": [from_group_id],
                    "status": caluma_workflow_models.WorkItem.STATUS_READY,
                    "case__family__meta__camac-instance-id": instance_id,
                }
            ):
                groups = set(getattr(work_item, groups_type))
                groups.remove(from_group_id)
                groups.add(to_group_id)

                # If the addressed groups change, we need to filter out all
                # assigned users that are not member of the new addressed group
                if len(work_item.assigned_users) and groups_type == "addressed_groups":
                    work_item.assigned_users = list(
                        set(
                            filter(
                                lambda user: Service.objects.filter(
                                    pk=int(to_group_id), groups__users__username=user
                                ).exists(),
                                work_item.assigned_users,
                            )
                        )
                    )

                setattr(work_item, groups_type, list(groups))
                work_item.save()


class CamacRequest:
    """
    A camac request object built from the given caluma info object.

    The request attribute holds a shallow copy of `info.context` with translated
    values where needed (user, group, etc.).
    """

    def __init__(self, info):
        self.request = copy(info.context)
        oidc_user = self.request.user
        self.request.user = self._get_camac_user(oidc_user)
        self.request.auth = jwt_decode(oidc_user.token, verify=False)
        camac_group = get_group(self.request)
        self.request.group = camac_group
        self.request.oidc_user = oidc_user

    def _get_camac_user(self, oidc_user):
        return User.objects.get(username=oidc_user.username)
