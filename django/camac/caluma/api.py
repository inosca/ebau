from logging import getLogger

from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_form.validators import AnswerValidator, DocumentValidator
from caluma.caluma_workflow import (
    api as caluma_workflow_api,
    models as caluma_workflow_models,
)
from django.conf import settings
from django.db.models import Q

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
        """Return true if instance was part of RSTA migration."""
        return instance.case.workflow_id == "migrated"

    def is_imported(self, instance):
        """Return true if instance was imported using dossier import."""
        return instance.case.document.form_id == "migriertes-dossier"

    def get_migration_type(self, instance):
        answer = instance.case.document.answers.filter(
            question_id="geschaeftstyp"
        ).first()

        if not answer:  # pragma: no cover
            return None

        option = answer.question.options.get(slug=answer.value)

        return (option.slug, option.label)

    def get_import_type(self, instance):
        answer = instance.case.document.answers.filter(
            question_id="geschaeftstyp-import"
        ).first()

        if not answer:  # pragma: no cover
            return None

        return answer.value

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

    def reassign_work_items(self, instance, from_group_id, to_group_id, user):
        from_group_id = str(from_group_id)
        to_group_id = str(to_group_id)

        for work_item in (
            caluma_workflow_models.WorkItem.objects.filter(
                Q(addressed_groups__contains=[from_group_id])
                | Q(controlling_groups__contains=[from_group_id])
            )
            .filter(
                status__in=[
                    caluma_workflow_models.WorkItem.STATUS_READY,
                    caluma_workflow_models.WorkItem.STATUS_SUSPENDED,
                ],
                case__family__instance=instance,
            )
            .exclude(
                task_id__in=[
                    "create-manual-workitems",
                    settings.DISTRIBUTION["INQUIRY_TASK"],
                    settings.DISTRIBUTION["INQUIRY_ANSWER_FILL_TASK"],
                    settings.DISTRIBUTION["INQUIRY_CREATE_TASK"],
                    settings.DISTRIBUTION["INQUIRY_CHECK_TASK"],
                ]
            )
        ):
            for groups_type in ["addressed_groups", "controlling_groups"]:
                groups = set(getattr(work_item, groups_type))

                if from_group_id not in groups:
                    continue

                groups.remove(from_group_id)
                groups.add(to_group_id)

                # If the addressed groups change, we need to filter out all
                # assigned users that are not member of the new addressed group
                if len(work_item.assigned_users) and groups_type == "addressed_groups":
                    work_item.assigned_users = [
                        username
                        for username in work_item.assigned_users
                        if Service.objects.filter(
                            pk=int(to_group_id), groups__users__username=username
                        ).exists()
                    ]

                setattr(work_item, groups_type, list(groups))

            work_item.save()

        # If there is no work item to allow creation of an inquiry for the new
        # service and the distribution is still running, we need to create one
        distribution = instance.case.work_items.filter(
            task_id=settings.DISTRIBUTION["DISTRIBUTION_TASK"],
            status=caluma_workflow_models.WorkItem.STATUS_READY,
        ).first()

        if (
            distribution
            and not distribution.child_case.work_items.filter(
                task_id=settings.DISTRIBUTION["INQUIRY_CREATE_TASK"],
                addressed_groups__contains=[to_group_id],
                status=caluma_workflow_models.WorkItem.STATUS_READY,
            ).exists()
        ):
            task = caluma_workflow_models.Task.objects.get(
                pk=settings.DISTRIBUTION["INQUIRY_CREATE_TASK"]
            )

            caluma_workflow_models.WorkItem.objects.create(
                task=task,
                name=task.name,
                addressed_groups=[to_group_id],
                controlling_groups=[to_group_id],
                case=distribution.child_case,
                status=caluma_workflow_models.WorkItem.STATUS_READY,
                created_by_user=user.username,
                created_by_group=user.group,
            )

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
