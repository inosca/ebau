from functools import reduce
from logging import getLogger

from caluma.caluma_core.events import send_event
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_form.validators import AnswerValidator, DocumentValidator
from caluma.caluma_workflow import (
    api as caluma_workflow_api,
    models as caluma_workflow_models,
)
from caluma.caluma_workflow.events import post_complete_case, post_create_work_item
from caluma.caluma_workflow.utils import get_jexl_groups
from django.conf import settings
from django.db.models import Count, Q
from django.utils.timezone import now

from camac.user.models import Service

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
        return instance.case.document.form if instance.case else None

    def get_form_name(self, instance):
        form = self._get_main_form(instance)
        return form.name if form else None

    def get_form_slug(self, instance):
        form = self._get_main_form(instance)
        return form.slug if form else None

    def _get_main_workflow(self, instance):
        return instance.case.workflow if instance.case else None

    def get_workflow_slug(self, instance):
        workflow = self._get_main_workflow(instance)
        return workflow.slug if workflow else None

    def _get_main_document(self, instance):
        return instance.case.document

    def get_main_document(self, instance):
        document = self._get_main_document(instance)
        return document.pk if document else None

    def get_source_document_value(self, document_id, field):
        source = caluma_form_models.Document.objects.get(pk=document_id).source
        return getattr(source, field, None) if source else None

    def delete_instance_case(self, instance_id):
        return caluma_workflow_models.Case.objects.filter(
            family__instance__pk=instance_id
        ).delete()

    def get_ebau_number(self, instance):
        return instance.case.meta.get("ebau-number", "-")

    def get_dossier_number(self, instance):
        return instance.case.meta.get("dossier-number", "-")

    def get_municipality(self, instance):
        return self.get_answer_value("gemeinde", instance)

    def get_answer_value(self, question_slug, instance):
        answer = instance.case.document.answers.filter(
            question_id=question_slug
        ).first()

        return answer.value if answer else None

    def get_table_answer(self, question_slug, instance):
        try:
            answer = instance.case.document.answers.get(
                question_id=question_slug,
            )
            return answer.documents.all()
        except caluma_form_models.Answer.DoesNotExist:
            return None

    def get_nfd_form_permissions(self, instance):
        permissions = set()

        answers = caluma_form_models.Answer.objects.filter(
            question_id="nfd-tabelle-status",
            document__family__form_id="nfd",
            document__family__work_item__case__family__instance__pk=instance.pk,
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

    def update_or_create_answer(self, document, question_slug, value, user):
        question = caluma_form_models.Question.objects.get(slug=question_slug)

        AnswerValidator().validate(
            question=question, document=document, user=user, value=value
        )

        return caluma_form_models.Answer.objects.update_or_create(
            document=document,
            question_id=question_slug,
            defaults={"value": value},
        )

    def set_submit_date(self, instance_id, submit_date):
        case = caluma_workflow_models.Case.objects.get(instance__pk=instance_id)

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
        return instance.case.document.answers.filter(
            question_id="is-paper",
            value="is-paper-yes",
        ).exists()

    def is_modification(self, instance):
        return instance.case.document.answers.filter(
            question_id="projektaenderung",
            value="projektaenderung-ja",
        ).exists()

    def is_migrated(self, instance):
        return instance.case.workflow_id == "migrated"

    def get_migration_type(self, instance):
        answer = instance.case.document.answers.filter(
            question_id="geschaeftstyp"
        ).first()

        if not answer:  # pragma: no cover
            return None

        option = answer.question.options.get(slug=answer.value)

        return (option.slug, option.label)

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

    def _clean_activations(self, child_case, activations):
        caluma_settings = settings.APPLICATION.get("CALUMA", {})
        existing_ids = list(activations.values_list("pk", flat=True))

        # Delete existing activation work items that don't have an
        # activation anymore.
        child_case.work_items.filter(
            task_id__in=caluma_settings.get("ACTIVATION_TASKS")
        ).exclude(**{"meta__activation-id__in": existing_ids}).delete()

    def _sync_activations(self, child_case, activations, user):
        caluma_settings = settings.APPLICATION.get("CALUMA", {})
        activation_task = caluma_workflow_models.Task.objects.get(
            pk=caluma_settings.get("ACTIVATION_INIT_TASK")
        )

        post_sync = set()

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
                work_item = child_case.work_items.create(
                    task=activation_task,
                    status=caluma_workflow_models.WorkItem.STATUS_READY,
                    created_by_user=user.username,
                    created_by_group=user.group,
                    name=activation_task.name,
                    meta={"activation-id": activation.pk},
                    **update_data,
                )
                send_event(
                    post_create_work_item,
                    sender=self.__class__,
                    work_item=work_item,
                    user=user,
                    context={},
                )

            if (
                activation.circulation_state.name in ["OK", "DONE"]
                and work_item.status == caluma_workflow_models.WorkItem.STATUS_READY
            ):
                post_sync.add(
                    (
                        activation.pk,
                        # Skip if the activation has an answer and cancel if it
                        # doesn't, which means that it was force finished
                        "skip" if activation.circulation_answer else "cancel",
                    )
                )

        for activation_id, action in post_sync:
            fn = getattr(caluma_workflow_api, f"{action}_work_item")

            for task in caluma_settings.get("ACTIVATION_RELEVANT_TASKS", []):
                work_item = child_case.work_items.filter(
                    **{
                        "task_id": task,
                        "status": caluma_workflow_models.WorkItem.STATUS_READY,
                        "meta__activation-id": activation_id,
                    }
                ).first()

                if work_item:
                    fn(
                        work_item=work_item,
                        user=user,
                        context={
                            "activation-id": activation_id,
                            "circulation-id": activations.first().circulation.pk,
                        },
                    )

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

        try:
            work_item = circulation.instance.case.work_items.get(
                **{
                    "task_id": caluma_settings.get("CIRCULATION_TASK"),
                    "meta__circulation-id": circulation.pk,
                }
            )
        except caluma_workflow_models.WorkItem.DoesNotExist:  # pragma: no cover
            log.error(f"No work item found for circulation {circulation.pk}")
            return

        activations = circulation.activations.exclude(circulation_state__name="IDLE")

        excluded_roles = caluma_settings.get("ACTIVATION_EXCLUDE_ROLES", [])

        if excluded_roles:
            activations = activations.annotate(
                service_non_excluded_groups_count=Count(
                    "service__groups",
                    filter=~Q(service__groups__role__name__in=excluded_roles),
                )
            ).exclude(service_non_excluded_groups_count=0)

        if activations.exists():
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
                context={"activation-id": activations.first().pk},
            )

            self._sync_activations(child_case, activations, user)
            self._clean_activations(child_case, activations)

            if (
                not child_case.work_items.filter(
                    status=caluma_workflow_models.WorkItem.STATUS_READY
                )
                and child_case.status == caluma_workflow_models.Case.STATUS_RUNNING
            ):
                # Manually close the case since all work items are completed.
                # This can happen when all activations except one are answered
                # and the remaining is deleted. Caluma can't react in this case
                # since that work item is deleted.
                child_case.status = caluma_workflow_models.Case.STATUS_COMPLETED
                child_case.closed_at = now()
                child_case.closed_by_user = user.username
                child_case.closed_by_group = user.group
                child_case.save()

                # This will automatically complete the parent work item
                send_event(
                    post_complete_case,
                    sender=self.__class__,
                    case=child_case,
                    user=user,
                    context={},
                )
        elif work_item.child_case:
            # Delete existing child case since there are no more activations
            work_item.child_case.delete()

    def reassign_work_items(self, instance_id, from_group_id, to_group_id):
        from_group_id = str(from_group_id)
        to_group_id = str(to_group_id)

        for groups_type in ["addressed_groups", "controlling_groups"]:
            for work_item in caluma_workflow_models.WorkItem.objects.filter(
                **{
                    f"{groups_type}__contains": [from_group_id],
                    "status__in": [
                        caluma_workflow_models.WorkItem.STATUS_READY,
                        caluma_workflow_models.WorkItem.STATUS_SUSPENDED,
                    ],
                    "case__family__instance__pk": instance_id,
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

    def validate_existing_audit_documents(self, instance_id, user):
        """Intermediate validation of existing audits.

        Make sure that those documents which are linked to the three
        table questions covering the "audit" functionality are valid.

        This is used when the responsible service is changed, where we
        want to make sure that filled audits are valid, but the entire
        document doesn't have to be valid yet.
        """
        caluma_settings = settings.APPLICATION.get("CALUMA", {})

        audit_work_item = caluma_workflow_models.WorkItem.objects.filter(
            **{
                "task_id": caluma_settings.get("AUDIT_TASK"),
                "status": caluma_workflow_models.WorkItem.STATUS_READY,
                "case__family__instance__pk": instance_id,
            }
        ).first()

        if not audit_work_item:
            return

        for table_answer in audit_work_item.document.answers.filter(
            question__type=caluma_form_models.Question.TYPE_TABLE
        ):
            for document in table_answer.documents.all():
                DocumentValidator().validate(document, user)

    def close_publication(self, instance, user):
        caluma_settings = settings.APPLICATION.get("CALUMA", {})
        publication_slug = caluma_settings.get("PUBLICATION_TASK_SLUG", "")

        work_item = caluma_workflow_models.WorkItem.objects.filter(
            status=caluma_workflow_models.WorkItem.STATUS_READY,
            case__family__instance__pk=instance.pk,
            task__slug=publication_slug,
        ).first()

        if work_item:
            caluma_workflow_api.complete_work_item(work_item, user)

    def _get_answer(self, document, slug):
        return str(
            document.answers.filter(question_id=slug)
            .values_list("value", flat=True)
            .first()
            or ""
        ).strip()

    def get_address(self, document):
        street, number, city, migrated = [
            self._get_answer(document, ans)
            for ans in [
                "strasse-flurname",
                "nr",
                "ort-grundstueck",
                "standort-migriert",
            ]
        ]

        address_lines = [f"{street} {number}".strip(), city]

        return ", ".join(address_lines) if all(address_lines) else migrated

    def get_gesuchsteller(self, document):
        table_ans = document.answers.filter(
            question_id="personalien-gesuchstellerin"
        ).first()
        if not table_ans or not table_ans.documents.exists():  # pragma: no cover
            return ""

        def _get_name(doc):
            name_jurist, first_name, last_name = [
                self._get_answer(doc, ans)
                for ans in [
                    "name-juristische-person-gesuchstellerin",
                    "vorname-gesuchstellerin",
                    "name-gesuchstellerin",
                ]
            ]

            return name_jurist or f"{first_name} {last_name}".strip()

        return ", ".join(  # pragma: no cover
            [_get_name(row_doc) for row_doc in table_ans.documents.all()]
        )

    def get_gemeinde(self, document):
        return self._get_answer(document, "gemeinde")
