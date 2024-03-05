from caluma.caluma_form.models import Answer, Document
from caluma.caluma_workflow.models import WorkItem
from django.db.models import Q
from rest_framework import serializers


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
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.slug = slug
        self.label = label
        self.task = task
        self.field = field
        self.status = status
        self.filter = filter
        self.include_child_cases = include_child_cases

    def get_attribute(self, instance):
        cases = instance._child_cases if self.include_child_cases else [instance.case]

        work_items = WorkItem.objects.filter(
            task=self.task,
            case__in=cases,
        )

        work_items = (
            work_items.filter(status=self.status) if self.status else work_items
        )

        if self.filter:
            work_items = work_items.filter(self.filter(instance))

        return work_items.values_list(self.field, flat=True)


class AnswerField(serializers.ReadOnlyField):
    def __init__(
        self,
        slug="",
        label="",
        document="",
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.slug = slug
        self.label = label
        self.document = document

    def get_attribute(self, instance):
        documents = Document.objects.filter(
            Q(form__slug=self.document)
            & (Q(case=instance.case) | Q(work_item__in=instance._all_work_items))
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
        self.label = label
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
        self.label = label
        self.method_name = f"get_{slug.replace('-', '_')}"
