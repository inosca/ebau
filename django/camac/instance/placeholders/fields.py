import base64
from io import BytesIO

import qrcode
from caluma.caluma_form.models import Answer, Question
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db.models import Sum
from django.utils.translation import get_language, gettext as _
from rest_framework import serializers

from camac.core.models import Activation, BillingV2Entry
from camac.user.models import Service
from camac.utils import build_url

from .utils import (
    clean_join,
    get_person_address_1,
    get_person_address_2,
    get_person_name,
    human_readable_date,
)


class DeprecatedField(serializers.ReadOnlyField):
    def __init__(self, value=None, **kwargs):
        super().__init__(**kwargs)

        self.value = value

    def get_attribute(self, instance):
        return self.value


class ServiceField(serializers.ReadOnlyField):
    def __init__(
        self,
        source_args=[],
        remove_name_prefix=False,
        add_municipality_prefix=False,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.source_args = source_args
        self.remove_name_prefix = remove_name_prefix
        self.add_municipality_prefix = add_municipality_prefix

    def to_representation(self, value):
        value = super().to_representation(value)

        if value and self.remove_name_prefix:
            # Municipalities and districts in BE all have a prefix which is
            # sometimes unwanted in certain placeholder.
            value = (
                value.replace("Leitbehörde", "")
                .replace("Regierungsstatthalteramt", "")
                .replace("Autorité directrice", "")
                .replace("Préfecuture", "")
            ).strip()

        if value and self.add_municipality_prefix:
            value = clean_join(_("Municipality"), value)

        return value

    def get_attribute(self, instance):
        service = self.get_service(instance)
        value = getattr(service, self.source) if service else None
        return value(*self.source_args) if callable(value) else value


class MunicipalityField(ServiceField):
    def get_service(self, instance):
        caluma_municipality = instance._master_data.municipality

        return (
            Service.objects.get(pk=caluma_municipality.get("slug"))
            if caluma_municipality
            else None
        )


class CurrentServiceField(ServiceField):
    def get_service(self, instance):
        return self.context["request"].group.service


class ResponsibleServiceField(ServiceField):
    def get_service(self, instance):
        return instance.responsible_service(filter_type="municipality")


class ResponsibleUserField(serializers.ReadOnlyField):
    def get_user(self, instance):
        responsible_service = instance.responsible_services.filter(
            service=self.context["request"].group.service
        ).first()

        return responsible_service.responsible_user if responsible_service else None

    def get_attribute(self, instance):
        user = self.get_user(instance)

        if not user:  # pragma: no cover
            return ""

        if self.source == "full_name":
            return clean_join(user.surname, user.name)

        return getattr(user, self.source)


class BillingEntriesField(serializers.ReadOnlyField):
    def __init__(self, own=False, total=False, **kwargs):
        super().__init__(**kwargs)

        self.own = own
        self.total = total

    def format_rate(self, value):
        return f"{value:,.2f}".replace(",", "’")

    def to_representation(self, value):
        if self.total:
            return self.format_rate(
                value.aggregate(Sum("final_rate")).get("final_rate__sum")
                if value
                else 0
            )

        return [
            {"POSITION": entry.text, "BETRAG": self.format_rate(entry.final_rate)}
            for entry in value
        ]

    def get_attribute(self, instance):
        own_filters = (
            {"group__service": self.context["request"].group.service}
            if self.own
            else {}
        )

        return BillingV2Entry.objects.filter(instance=instance, **own_filters)


class PublicationField(serializers.ReadOnlyField):
    def __init__(self, value_key="value", parser=lambda value: value, **kwargs):
        super().__init__(**kwargs)

        self.value_key = value_key
        self.parser = parser

    def to_representation(self, value):
        return self.parser(super().to_representation(value))

    def get_attribute(self, instance):
        work_item = (
            instance.case.work_items.filter(
                task_id="fill-publication",
                status=WorkItem.STATUS_COMPLETED,
                addressed_groups=[str(self.context["request"].group.service_id)],
                **{"meta__is-published": True},
            )
            .order_by("-created_at")
            .first()
        )
        answer = (
            work_item.document.answers.filter(question_id=self.source).first()
            if work_item
            else None
        )

        return getattr(answer, self.value_key, "") if answer else ""


class MasterDataField(serializers.ReadOnlyField):
    def __init__(self, join_by=None, sum_by=None, parser=lambda value: value, **kwargs):
        super().__init__(**kwargs)

        self.join_by = join_by
        self.sum_by = sum_by
        self.parser = parser

    def to_representation(self, value):
        if self.join_by and isinstance(value, list):
            return clean_join(*[self.parser(v) for v in value], separator=self.join_by)
        if self.sum_by and isinstance(value, list):

            def parse(v):
                try:
                    return int(v.get(self.sum_by))
                except (TypeError, ValueError):  # pragma: no cover
                    return None

            parsed_values = list(filter(None, [parse(v) for v in value]))

            return sum(parsed_values) if len(parsed_values) else ""

        return self.parser(super().to_representation(value))

    def get_attribute(self, instance):
        return getattr(instance._master_data, self.source)


class JointField(serializers.ReadOnlyField):
    def __init__(self, fields=[], separator=" ", **kwargs):
        super().__init__(**kwargs)

        self.fields = fields
        self.separator = separator

        for field in self.fields:
            field.bind(field_name="", parent=self)

    def get_attribute(self, instance):
        return clean_join(
            *[
                field.to_representation(field.get_attribute(instance))
                for field in self.fields
            ],
            separator=self.separator,
        )


class ActivationsField(serializers.ReadOnlyField):
    def __init__(
        self,
        only_own=False,
        filters={},
        props=[
            ("service", "NAME"),
            ("deadline", "FRIST"),
            ("creation_date", "ERSTELLT"),
        ],
        join_by=None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.only_own = only_own
        self.filters = filters
        self.props = props
        self.join_by = join_by

    def get_notice(self, activation, notice_type):
        notice_types = {"STELLUNGNAHME": 1, "NEBENBESTIMMUNGEN": 20000}

        return (
            activation.notices.filter(notice_type_id=notice_types.get(notice_type))
            .values_list("content", flat=True)
            .first()
            or ""
        )

    def get_prop_key(self, prop):
        return prop[1] if isinstance(prop, tuple) else prop

    def get_prop_value(self, activation, prop):
        prop_mapping = {
            "opinion": lambda activation: self.get_notice(activation, "STELLUNGNAHME"),
            "collateral": lambda activation: self.get_notice(
                activation, "NEBENBESTIMMUNGEN"
            ),
            "answer": lambda activation: activation.circulation_answer.get_name(),
            "service": lambda activation: activation.service.get_name(),
            "service_with_prefix": lambda activation: f"- {activation.service.get_name()}",
            "deadline": lambda activation: activation.deadline_date.strftime(
                "%d.%m.%Y"
            ),
            "creation_date": lambda activation: activation.start_date.strftime(
                "%d.%m.%Y"
            ),
        }

        if isinstance(prop, tuple):
            prop = prop[0]

        return prop_mapping.get(prop)(activation)

    def to_representation(self, value):
        mapped = [
            {
                self.get_prop_key(prop): self.get_prop_value(activation, prop)
                for prop in self.props
            }
            for activation in value
        ]

        if self.join_by:
            return clean_join(
                *[i.get(self.props[0]) for i in mapped], separator=self.join_by
            )

        return mapped

    def get_attribute(self, instance):
        if self.only_own:
            self.filters.update({"service": self.context["request"].group.service})

        return Activation.objects.filter(
            circulation__instance=instance, **self.filters
        ).order_by("start_date")


class MasterDataPersonField(MasterDataField):
    def __init__(
        self,
        only_first=False,
        fields=["juristic_name", "name"],
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.only_first = only_first
        self.fields = (
            ["juristic_name", "name", "address_1", "address_2"]
            if fields == "__all__"
            else fields
        )

    def parse_row(self, row):
        parts = []

        if "juristic_name" in self.fields:
            parts.append(
                get_person_name(row, include_name=False, include_juristic_name=True)
            )

        if "name" in self.fields:
            parts.append(
                get_person_name(row, include_name=True, include_juristic_name=False)
            )

        if "address_1" in self.fields:
            parts.append(get_person_address_1(row))

        if "address_2" in self.fields:
            parts.append(get_person_address_2(row))

        return clean_join(*parts, separator=", ")

    def to_representation(self, value):
        if not value or not len(value):  # pragma: no cover
            return ""

        return clean_join(*[self.parse_row(row) for row in value], separator=", ")

    def get_attribute(self, instance):
        value = super().get_attribute(instance)

        return value[:1] if self.only_first and value else value


class InformationOfNeighborsField(serializers.ReadOnlyField):
    def __init__(
        self,
        type,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.type = type

    def get_work_item(self, instance):
        return (
            instance.case.work_items.filter(
                task_id="information-of-neighbors",
                status=WorkItem.STATUS_COMPLETED,
                addressed_groups=[str(self.context["request"].group.service_id)],
                **{"meta__is-published": True},
            )
            .order_by("-created_at")
            .first()
        )

    def get_attribute(self, instance):
        work_item = self.get_work_item(instance)

        if work_item and self.type in ["link", "qr_code"]:
            return build_url(
                settings.PUBLIC_BASE_URL,
                f"/public-instances/{instance.pk}/form?key={str(work_item.document.pk)[:7]}",
            )

        elif work_item and self.type == "neighbors":
            table = work_item.document.answers.filter(
                question_id="information-of-neighbors-neighbors"
            ).first()

            def get_value(row, question):
                answer = row.answers.filter(question_id=question).first()
                return answer.value if answer else None

            return [
                {
                    "last_name": get_value(row, "name-gesuchstellerin"),
                    "first_name": get_value(row, "vorname-gesuchstellerin"),
                    "street": get_value(row, "strasse-gesuchstellerin"),
                    "street_number": get_value(row, "nummer-gesuchstellerin"),
                    "zip": get_value(row, "plz-gesuchstellerin"),
                    "town": get_value(row, "ort-gesuchstellerin"),
                    "is_juristic_person": (
                        get_value(
                            row,
                            "juristische-person-gesuchstellerin",
                        )
                        == "juristische-person-gesuchstellerin-ja"
                    ),
                    "juristic_name": get_value(
                        row, "name-juristische-person-gesuchstellerin"
                    ),
                }
                for row in (table.documents.all() if table else [])
            ]

        return None

    def to_representation(self, value):
        if value and self.type == "qr_code":
            data = BytesIO()
            img = qrcode.make(value)
            img.save(data, "PNG")
            data_b64 = base64.b64encode(data.getvalue())
            return f"data:image/png;base64,{data_b64.decode('utf-8')}"

        elif self.type == "neighbors":
            return [
                {
                    "NAME": get_person_name(person),
                    "ADDRESS_1": get_person_address_1(person),
                    "ADDRESS_2": get_person_address_2(person),
                }
                for person in value
            ]

        return value


class DecisionField(serializers.ReadOnlyField):
    def __init__(self, compare_to=None, use_identifier=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.compare_to = compare_to
        self.use_identifier = use_identifier

    def get_attribute(self, instance):
        try:
            return Answer.objects.get(
                question_id=self.source,
                document__work_item__task_id="decision",
                document__work_item__status=WorkItem.STATUS_COMPLETED,
                document__work_item__case__family__instance=instance,
            )
        except Answer.DoesNotExist:
            return None

    def to_representation(self, answer):
        if self.compare_to:
            return answer.value in (
                self.compare_to
                if isinstance(self.compare_to, list)
                else [self.compare_to]
            )

        if answer.question.type == Question.TYPE_DATE:
            return human_readable_date(answer.date)
        elif answer.question.type == Question.TYPE_CHOICE:
            option = answer.selected_options[0]

            if self.use_identifier:
                return option.meta["identifier"]

            return option.label[get_language()]

        return answer.value  # pragma: no cover
