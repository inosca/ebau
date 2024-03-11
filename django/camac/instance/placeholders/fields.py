import base64
from abc import ABC, abstractmethod
from io import BytesIO

import qrcode
from alexandria.core import models as alexandria_models
from caluma.caluma_form.models import Answer, AnswerDocument, Document, Question
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db.models import Exists, OuterRef, Q, Sum
from django.utils.translation import get_language, gettext, gettext_noop as _
from rest_framework import serializers

from camac.alexandria.extensions.visibilities import (
    CustomVisibility as CustomAlexandriaVisibility,
)
from camac.billing.models import BillingV2Entry
from camac.caluma.utils import find_answer, work_item_by_addressed_service_condition
from camac.user.models import Service, User
from camac.utils import build_url, clean_join, get_dict_item

from .utils import (
    clean_and_add_full_name,
    get_person_address_1,
    get_person_address_2,
    get_person_name,
    human_readable_date,
    row_to_person,
)


class AliasedMixin(object):
    def __init__(
        self, aliases=[], nested_aliases={}, description=None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.aliases = aliases
        self._nested_aliases = nested_aliases
        self.description = description

    @property
    def nested_aliases(self):
        return self._nested_aliases


class AliasedIntegerField(AliasedMixin, serializers.IntegerField):
    pass


class AliasedMethodField(AliasedMixin, serializers.SerializerMethodField):
    pass


class DeprecatedField(AliasedMixin, serializers.ReadOnlyField):
    def __init__(self, value=None, **kwargs):
        super().__init__(**kwargs)

        self.value = value

    def get_attribute(self, instance):
        return self.value


class ServiceField(ABC, AliasedMixin, serializers.ReadOnlyField):
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

    @abstractmethod
    def get_service(instance):  # pragma: no cover
        ...

    def to_representation(self, value):
        value = super().to_representation(value)

        if value and self.remove_name_prefix:
            # Municipalities and districts in BE all have a prefix which is
            # sometimes unwanted in certain placeholder.
            for prefix in [
                gettext("Authority"),
                gettext("Municipality"),
                gettext("District"),
            ]:
                value = value.replace(prefix, "").strip()

        if value and self.add_municipality_prefix:
            value = clean_join(gettext("Municipality"), value)

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


class UserField(ABC, AliasedMixin, serializers.ReadOnlyField):
    @abstractmethod
    def get_user(instance):  # pragma: no cover
        ...

    def get_attribute(self, instance):
        user = self.get_user(instance)

        if not user:  # pragma: no cover
            return ""

        if self.source == "full_name":
            return clean_join(user.name, user.surname)

        return getattr(user, self.source)


class ResponsibleUserField(UserField):
    def get_user(self, instance):
        responsible_service = instance.responsible_services.filter(
            service=self.context["request"].group.service
        ).first()

        return responsible_service.responsible_user if responsible_service else None


class CurrentUserField(UserField):
    def get_user(self, instance):
        return self.context["request"].user


class BillingEntriesField(AliasedMixin, serializers.ReadOnlyField):
    def __init__(self, own=False, total=False, **kwargs):
        super().__init__(**kwargs)

        self.own = own
        self.total = total

    @property
    def nested_aliases(self):
        if self.total:
            return {}

        nested_aliases = {
            "POSITION": [_("POSITION")],
            "BETRAG": [_("AMOUNT")],
        }

        if settings.APPLICATION_NAME == "kt_so":
            nested_aliases.update(
                {
                    "RECHTSGRUNDLAGE": [_("LEGAL_BASIS")],
                    "KOSTENSTELLE": [_("COST_CENTER")],
                }
            )

        return nested_aliases

    def format_rate(self, value):
        return f"{value:,.2f}".replace(",", "’")

    def to_representation(self, value):
        if self.total:
            return self.format_rate(
                value.aggregate(Sum("final_rate")).get("final_rate__sum")
                if value
                else 0
            )

        data = []

        for entry in value:
            row = {
                "POSITION": entry.text,
                "BETRAG": self.format_rate(entry.final_rate),
            }

            if settings.APPLICATION_NAME == "kt_so":
                row.update(
                    {
                        "RECHTSGRUNDLAGE": entry.legal_basis,
                        "KOSTENSTELLE": entry.cost_center,
                    }
                )

            data.append(row)

        return data

    def get_attribute(self, instance):
        own_filters = (
            {"group__service": self.context["request"].group.service}
            if self.own
            else {}
        )

        return BillingV2Entry.objects.filter(instance=instance, **own_filters).order_by(
            "organization", "pk"
        )


class PublicationField(AliasedMixin, serializers.ReadOnlyField):
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


class MasterDataField(AliasedMixin, serializers.ReadOnlyField):
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
        if not get_dict_item(
            settings.MASTER_DATA, f"CONFIG.{self.source}", default=None
        ):  # pragma: no cover
            return None

        return getattr(instance._master_data, self.source)


class JointField(AliasedMixin, serializers.ReadOnlyField):
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


class InquiriesField(AliasedMixin, serializers.ReadOnlyField):
    def __init__(
        self,
        only_own=False,
        props=[
            ("service", "NAME"),
            ("deadline", "FRIST"),
            ("creation_date", "ERSTELLT"),
            ("completion_date", "BEANTWORTET"),
        ],
        join_by=None,
        service_group=None,
        status=None,
        **kwargs,
    ):
        all_nested_aliases = {
            "ANTWORT": [_("ANSWER")],
            "BEANTWORTET": [_("ANSWERED")],
            "ERSTELLT": [_("CREATED")],
            "FACHSTELLE": [_("SERVICE")],
            "FRIST": [_("DEADLINE")],
            "NAME": [_("NAME")],
            "NEBENBESTIMMUNGEN": [_("ANCILLARY_CLAUSES")],
            "STELLUNGNAHME": [_("OPINION")],
            "TEXT": [_("TEXT")],
            "VON": [_("BY")],
        }

        nested_aliases = (
            {key: all_nested_aliases[key] for _, key in props}
            if all([isinstance(prop, tuple) for prop in props])
            else {}
        )

        super().__init__(nested_aliases=nested_aliases, **kwargs)

        self.only_own = only_own
        self.props = props
        self.join_by = join_by
        self.service_group = service_group
        self.status = status

    def get_service(self, inquiry, type):
        return Service.objects.get(pk=int(getattr(inquiry, type)[0])).get_name()

    def get_prop_key(self, prop):
        return prop[1] if isinstance(prop, tuple) else prop

    def get_prop_value(self, inquiry, prop):
        prop_mapping = {
            "opinion": lambda i: find_answer(
                i.child_case.document,
                settings.DISTRIBUTION["QUESTIONS"]["STATEMENT"],
            ),
            "ancillary_clauses": lambda i: find_answer(
                i.child_case.document,
                settings.DISTRIBUTION["QUESTIONS"]["ANCILLARY_CLAUSES"],
            ),
            "answer": lambda i: find_answer(
                i.child_case.document,
                settings.DISTRIBUTION["QUESTIONS"]["STATUS"],
            ),
            "service": lambda i: self.get_service(i, "addressed_groups"),
            "service_with_prefix": lambda i: f"- {self.get_service(i,'addressed_groups')}",
            "deadline": lambda i: i.deadline.strftime("%d.%m.%Y"),
            "creation_date": lambda i: i.created_at.strftime("%d.%m.%Y"),
            "completion_date": lambda i: (
                i.closed_at.strftime("%d.%m.%Y")
                if i.status == WorkItem.STATUS_COMPLETED
                else None
            ),
        }

        if isinstance(prop, tuple):
            prop = prop[0]

        try:
            return prop_mapping.get(prop)(inquiry)
        except AttributeError:
            # child_case and deadline may be None on draft inquiries
            return ""

    def to_representation(self, value):
        mapped = [
            {
                self.get_prop_key(prop): self.get_prop_value(inquiry, prop)
                for prop in self.props
            }
            for inquiry in value
        ]

        if self.join_by:
            return clean_join(
                *[i.get(self.props[0]) for i in mapped], separator=self.join_by
            )

        return mapped

    def get_attribute(self, instance):
        service = self.context["request"].group.service

        if not service:  # pragma: no cover
            return None

        queryset = WorkItem.objects.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
            case__family__instance=instance,
            status__in=(
                [self.status]
                if self.status
                else [
                    WorkItem.STATUS_READY,
                    WorkItem.STATUS_COMPLETED,
                    WorkItem.STATUS_SUSPENDED,
                    WorkItem.STATUS_SKIPPED,
                ]
            ),
        ).filter(
            work_item_by_addressed_service_condition(
                Q(service_parent__isnull=True) | Q(service_parent_id=service.pk)
            )
        )

        if self.only_own:
            queryset = queryset.exclude(status=WorkItem.STATUS_SUSPENDED).filter(
                addressed_groups__contains=[str(service.pk)]
            )
        elif self.service_group:
            service_groups = self.service_group

            if not isinstance(service_groups, list):
                service_groups = [service_groups]

            queryset = queryset.filter(
                work_item_by_addressed_service_condition(
                    Q(service_group__name__in=service_groups)
                )
            )

        return queryset.order_by("created_at")


class LegalSubmissionField(AliasedMixin, serializers.ReadOnlyField):
    def __init__(self, type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.type = type

    @property
    def nested_aliases(self):
        if settings.APPLICATION_NAME == "kt_so":
            return {
                "DATUM_POSTSTEMPEL": [_("DATE_POSTMARK")],
                "EINSPRECHENDE": [_("OPPOSING")],
            }

        nested_aliases = {
            "DATUM_DOKUMENT": [_("DATE_DOCUMENT")],
            "DATUM_EINGANG": [_("DATE_RECEIPT")],
            "RECHTSBEGEHRENDE": [_("LEGAL_CLAIMANTS")],
            "TITEL": [_("TITLE")],
        }

        if self.type == "legal-submission-type-objection":
            nested_aliases["RUEGEPUNKTE"] = [_("REPRIMANDS")]
        else:
            nested_aliases["ANLIEGEN"] = [_("REQUEST"), _("CONCERN")]

        return nested_aliases

    def to_representation(self, value):
        data = []

        for document in value:
            legal_claimants = []

            for claimant in find_answer(
                document,
                settings.PLACEHOLDERS["LEGAL_SUBMISSIONS"][
                    "LEGAL_CLAIMANTS_TABLE_QUESTION"
                ],
            ):
                legal_claimants.append(get_person_name(row_to_person(claimant)))

            if settings.APPLICATION_NAME == "kt_bern":
                legal_submission = {
                    "DATUM_EINGANG": find_answer(
                        document, "legal-submission-receipt-date"
                    ),
                    "DATUM_DOKUMENT": find_answer(
                        document, "legal-submission-document-date"
                    ),
                    "TITEL": find_answer(document, "legal-submission-title"),
                    "RECHTSBEGEHRENDE": clean_join(*legal_claimants, separator=", "),
                }
            elif settings.APPLICATION_NAME == "kt_so":
                legal_submission = {
                    "DATUM_POSTSTEMPEL": find_answer(document, "einsprache-datum"),
                    "EINSPRECHENDE": clean_join(*legal_claimants, separator=", "),
                }

            if self.type == "legal-submission-type-objection":
                legal_submission["RUEGEPUNKTE"] = find_answer(
                    document, "legal-submission-reprimands"
                )
            elif self.type == "legal-submission-type-load-compensation-request":
                legal_submission["ANLIEGEN"] = find_answer(
                    document, "legal-submission-request-load-compensation-request"
                )
            elif self.type == "legal-submission-type-legal-custody":
                legal_submission["ANLIEGEN"] = find_answer(
                    document, "legal-submission-request-legal-custody"
                )

            data.append(legal_submission)

        return data

    def get_attribute(self, instance):
        queryset = Document.objects.filter(
            form_id=settings.PLACEHOLDERS["LEGAL_SUBMISSIONS"]["FORM"],
            family__work_item__case__instance=instance,
        )

        if self.type:
            queryset = queryset.filter(
                Exists(
                    Answer.objects.filter(
                        question_id="legal-submission-type",
                        value__contains=self.type,
                        document_id=OuterRef("pk"),
                    )
                )
            )

        return queryset.prefetch_related("answers").order_by("-answerdocument__sort")


class LegalClaimantsField(AliasedMixin, serializers.ReadOnlyField):
    def __init__(self, type=None, *args, **kwargs):
        super().__init__(
            nested_aliases={"ADDRESS": [_("ADDRESS")], "NAME": [_("NAME")]},
            *args,
            **kwargs,
        )

        self.type = type

    def to_representation(self, value):
        data = []

        for claimant in value:
            serialized = clean_and_add_full_name(row_to_person(claimant))

            data.append(
                {
                    "ADDRESS": serialized["full_address"],
                    "NAME": serialized["full_name"],
                }
            )

        return data

    def get_attribute(self, instance):
        legal_submissions = Document.objects.filter(
            form_id=settings.PLACEHOLDERS["LEGAL_SUBMISSIONS"]["FORM"],
            family__work_item__case__instance=instance,
        )

        if self.type:
            legal_submissions = legal_submissions.filter(
                Exists(
                    Answer.objects.filter(
                        question_id="legal-submission-type",
                        value__contains=self.type,
                        document_id=OuterRef("pk"),
                    )
                )
            )

        return Document.objects.filter(
            pk__in=AnswerDocument.objects.filter(
                answer__document__in=legal_submissions,
                answer__question_id=settings.PLACEHOLDERS["LEGAL_SUBMISSIONS"][
                    "LEGAL_CLAIMANTS_TABLE_QUESTION"
                ],
            ).values("document")
        ).order_by("created_at")


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


class InformationOfNeighborsField(AliasedMixin, serializers.ReadOnlyField):
    def __init__(
        self,
        type,
        **kwargs,
    ):
        nested_aliases = (
            {
                "ADDRESS_1": [_("ADDRESS_1")],
                "ADDRESS_2": [_("ADDRESS_2")],
                "NAME": [_("NAME")],
            }
            if type == "neighbors"
            else {}
        )

        super().__init__(
            nested_aliases=nested_aliases,
            **kwargs,
        )

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


class DecisionField(AliasedMixin, serializers.ReadOnlyField):
    def __init__(self, compare_to=None, use_identifier=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.compare_to = compare_to
        self.use_identifier = use_identifier

    def get_attribute(self, instance):
        work_item = (
            WorkItem.objects.filter(task_id="decision", case__family__instance=instance)
            .exclude(status=WorkItem.STATUS_CANCELED)
            .order_by("-created_at")
            .first()
        )

        return (
            work_item.document.answers.filter(question_id=self.source).first()
            if work_item
            else None
        )

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


class AlexandriaDocumentField(AliasedMixin, serializers.ReadOnlyField):
    nested_aliases = {
        "NAME": [_("NAME")],
        "DESCRIPTION": [_("DESCRIPTION")],
        "CREATED_AT": [_("CREATED_AT")],
        "CREATED_BY": [_("CREATED_BY")],
        "MODIFIED_AT": [_("MODIFIED_AT")],
        "MODIFIED_BY": [_("MODIFIED_BY")],
        "CATEGORY": [_("CATEGORY")],
        "MARKS": [_("MARKS")],
        "TAGS": [_("TAGS")],
    }

    def __init__(
        self,
        mark=None,
        category=None,
        include_child_categories=False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.mark = mark
        self.category = category
        self.include_child_categories = include_child_categories

    def get_attribute(self, instance):
        queryset = alexandria_models.Document.objects.filter(
            instance_document__instance=instance
        )

        if self.mark:
            queryset = queryset.filter(marks__pk__contains=self.mark)

        if self.category:
            filter = Q(category_id=self.category)

            if self.include_child_categories:
                filter |= Q(category__parent_id=self.category)

            queryset = queryset.filter(filter)

        return CustomAlexandriaVisibility().filter_queryset_for_document(
            queryset, self.context["request"]
        )

    def to_representation(self, documents):
        data = []

        for document in documents:
            system_generated = "system-generated" in document.metainfo
            created_by = ""
            modified_by = ""
            if not system_generated:
                if created_by_user := User.objects.filter(
                    pk=document.created_by_user
                ).first():
                    created_by = created_by_user.get_full_name()
                if modified_by_user := User.objects.filter(
                    pk=document.modified_by_user
                ).first():
                    modified_by = modified_by_user.get_full_name()

            data.append(
                {
                    "NAME": document.title.de,
                    "DESCRIPTION": document.description.de,
                    "CREATED_AT": document.created_at.strftime("%d.%m.%Y %H:%M"),
                    "CREATED_BY": created_by,
                    "MODIFIED_AT": document.modified_at.strftime("%d.%m.%Y %H:%M"),
                    "MODIFIED_BY": modified_by,
                    "CATEGORY": document.category.slug,
                    "MARKS": list(document.marks.values_list("slug", flat=True)),
                    "TAGS": list(document.tags.values_list("name", flat=True)),
                }
            )

        return data


class AlexandriaSimpleDocumentField(AlexandriaDocumentField):
    nested_aliases = {}

    def to_representation(self, documents):
        return ",\n".join(
            [
                gettext(
                    "%(title)s (submitted as %(original_title)s) on %(date)s at %(time)s"
                )
                % {
                    "title": document.title[get_language()],
                    "original_title": document.files.filter(variant="original")
                    .order_by("-created_at")
                    .first()
                    .name,
                    "date": document.created_at.strftime("%d.%m.%Y"),
                    "time": document.created_at.strftime("%H:%M"),
                }
                for document in documents
            ]
        )
