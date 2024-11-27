from caluma.caluma_form.models import Answer, Document
from caluma.caluma_workflow.models import WorkItem
from django.db.models import Q
from django.utils.translation import gettext as _
from rest_framework import serializers

from camac.core.models import WorkflowEntry


class WorkItemsField(serializers.ReadOnlyField):
    def __init__(
        self,
        slug="",
        label="",
        task=[],
        field="created_at",
        status=None,
        include_child_cases=True,
        filter=None,
        order_by=None,
        limit=None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.slug = slug
        self.label = _(label)
        self.task = task
        self.field = field
        self.status = status
        self.filter = filter
        self.order_by = order_by
        self.limit = limit
        self.include_child_cases = include_child_cases

    def get_attribute(self, instance):
        cases = instance._child_cases if self.include_child_cases else [instance.case]

        work_items = WorkItem.objects.filter(
            task=self.task,
            case__in=cases,
        ).exclude(**{self.field: None})

        work_items = (
            work_items.filter(status=self.status) if self.status else work_items
        )

        if self.filter:
            work_items = work_items.filter(self.filter(instance))

        if self.order_by:
            work_items = work_items.order_by(self.order_by)

        if self.limit:
            work_items = work_items[: self.limit]

        return work_items.values_list(self.field, flat=True)


# This has no test coverage because Uri will use this in the future
# but hasn't decided yet which answers they are going to use here
# It therefore doesn't show up in the snapshot tests and that means no coverage.
class AnswerField(serializers.ReadOnlyField):
    def __init__(
        self,
        slug="",
        label="",
        document="",
        family_form_id="",
        **kwargs,
    ):  # pragma: no cover
        super().__init__(**kwargs)

        self.slug = slug
        self.label = _(label)
        self.document = document
        self.family_form_id = family_form_id

    def get_attribute(self, instance):  # pragma: no cover
        documents = Document.objects.filter(form__slug=self.document)

        if self.family_form_id:
            documents = documents.filter(family__form_id=self.family_form_id)
        else:
            documents = documents.filter(
                (Q(case=instance.case) | Q(work_item__in=instance._all_work_items))
            )

        answers = Answer.objects.filter(
            question__slug=self.slug,
            document__in=documents,
        )
        # filter the answers for empty values
        answers = answers.exclude(Q(value__isnull=True) & Q(date__isnull=True))

        return answers.exclude(date__isnull=True).values_list("date", flat=True)


class MilestonesField(serializers.ReadOnlyField):
    def __init__(self, sections=[], **kwargs):
        super().__init__(**kwargs)

        self.sections = sections

    def get_attribute(self, instance):
        return [
            {
                "slug": section.slug,
                "label": section.label,
                "fields": [
                    {
                        "slug": field.slug,
                        "label": field.label,
                        "value": field.to_representation(field.get_attribute(instance)),
                    }
                    for field in section.fields
                ],
            }
            for section in self.sections
        ]

    # This is necessary to bind the field to the root serializer (because they are nested)
    def bind(self, field_name, parent):
        super().bind(field_name, parent)

        for section in self.sections:
            section.bind(field_name, parent)


class MilestoneSectionField(serializers.ReadOnlyField):
    def __init__(self, slug="", label="", fields=[], **kwargs):
        super().__init__(**kwargs)

        self.slug = slug
        self.label = _(label)
        self.fields = fields

    # This is necessary to bind the field to the root serializer (because they are nested)
    def bind(self, field_name, parent):
        super().bind(field_name, parent)

        for field in self.fields:
            field.bind(field_name, parent)


class MethodField(serializers.SerializerMethodField):
    def __init__(self, slug="", label="", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.slug = slug
        self.label = _(label)
        self.method_name = f"get_{slug.replace('-', '_')}"


class CamacWorkflowEntryField(serializers.ReadOnlyField):
    def __init__(self, slug="", name="", label="", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.slug = slug
        self.name = name
        self.label = _(label)

    def get_attribute(self, instance):
        workflow_entry = WorkflowEntry.objects.filter(
            instance_id=instance.pk,
            workflow_item__name=self.name,
        ).first()

        if workflow_entry:
            return workflow_entry.workflow_date
        return None  # pragma: no cover
