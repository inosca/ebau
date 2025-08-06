import hashlib
import json
from abc import ABCMeta, abstractmethod

from caluma.caluma_form.models import Answer, AnswerDocument, DynamicOption
from django.conf import settings
from django.db import models
from django.db.models import (
    Case,
    CharField,
    Exists,
    F,
    Manager,
    OuterRef,
    Value,
    When,
)
from django.db.models.expressions import Func
from django.db.models.functions import (
    Cast,
    Concat,
    NullIf,
    Replace,
    Trim,
    TruncDate,
)
from django.utils.functional import cached_property
from django.utils.translation import get_language

from camac.instance.export.filters import (
    StringAggSubquery,
    caluma_answer,
)
from camac.instance.models import Instance, InstanceStateT
from camac.permissions.api import PermissionManager
from camac.responsible.models import ResponsibleService
from camac.user.models import Role, Service


class AbstractModelMeta(ABCMeta, type(models.Model)):
    pass


class InstanceProxy(models.Model, metaclass=AbstractModelMeta):
    @classmethod
    @abstractmethod
    def fields(self) -> list[str]: ...

    def fields_to_dict(self):
        return {field: getattr(self, field, None) for field in self.fields}

    def hash(self):
        data = self.fields_to_dict()
        json_dump = json.dumps(data, sort_keys=True)
        encoded = json_dump.encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    class Meta:
        abstract = True


class InstanceManagerAG(Manager["InstanceProxyAG"]):
    """Custom manager for instance proxies."""

    def annotate_gis_data(self):
        return caluma_answer("gis-map")

    def annotate_dossier_number(self):
        return F("case__meta__dossier-number")

    def annotate_responsible_user(self):
        service_afb = Service.objects.filter(slug="afb").values("pk")[:1]
        return (
            ResponsibleService.objects.filter(
                instance_id=OuterRef("pk"), service_id=service_afb
            )
            .annotate(
                name=Trim(
                    Concat(
                        Trim(F("responsible_user__name")),
                        Value(" "),
                        Trim(F("responsible_user__surname")),
                    )
                )
            )
            .values("name")[:1]
        )

    def annotate_intent(self):
        return caluma_answer("beschreibung-bauvorhaben")

    def annotate_url(self):
        return Concat(
            Value(f"{settings.INTERNAL_BASE_URL}/cases/"),
            F("instance_id"),
            output_field=models.CharField(),
        )

    def annotate_municipality(self):
        return (
            DynamicOption.objects.filter(
                question_id="gemeinde", document_id=OuterRef("case__document_id")
            )
            .order_by("-created_at")
            .values(f"label__{get_language()}")[:1]
        )

    def annotate_plot_number(self):
        return StringAggSubquery(
            Answer.objects.filter(
                question_id="parzellennummer",
                document__family=OuterRef("case__document_id"),
                value__isnull=False,
            )
            .annotate(
                # Return NULL if the answer is empty so this function returns
                # the same on empty answers as on no answer at all.
                string_value=NullIf(
                    Trim(
                        Replace(
                            Cast("value", output_field=CharField()),
                            Value('"'),
                            Value(""),
                        )
                    ),
                    Value(""),
                ),
            )
            .values("string_value"),
            column_name="string_value",
            delimiter=", ",
        )

    def annotate_status(self):
        return InstanceStateT.objects.filter(
            instance_state_id=OuterRef("instance_state_id"), language=get_language()
        ).values("name")[:1]

    def annotate_applicant(self):
        return StringAggSubquery(
            AnswerDocument.objects.filter(
                answer__question_id="personalien-gesuchstellerin",
                answer__document_id=OuterRef("case__document_id"),
            )
            .annotate(
                is_juristic=Exists(
                    Answer.objects.filter(
                        question_id="juristische-person-gesuchstellerin",
                        document_id=OuterRef("document_id"),
                        value="juristische-person-gesuchstellerin-ja",
                    )
                ),
                name=Case(
                    When(
                        is_juristic=True,
                        then=caluma_answer(
                            "name-juristische-person-gesuchstellerin", "document_id"
                        ),
                    ),
                    default=Trim(
                        Concat(
                            caluma_answer("vorname-gesuchstellerin", "document_id"),
                            Value(" "),
                            caluma_answer("name-gesuchstellerin", "document_id"),
                        )
                    ),
                ),
            )
            .values("name")[:1],
            column_name="name",
            delimiter=", ",
        )

    def annotate_submit_date(self):
        return Cast(
            TruncDate(
                Func(
                    Replace(
                        Cast("case__meta__submit-date", output_field=CharField()),
                        Value('"'),
                        Value(""),
                    ),
                    Cast(Value("YYYY-mm-dd"), output_field=models.CharField()),
                    function="TO_DATE",
                    output_field=models.DateTimeField(),
                )
            ),
            output_field=models.CharField(),
        )

    def annotate_type(self):
        return F(f"case__family__document__form__name__{get_language()}")

    def get_queryset(self):
        """Return the annotated base queryset for the AfB."""

        afb = Service.objects.get(slug="afb")
        role = Role.objects.get(name="trusted-service-lead")

        manager = PermissionManager.from_params(service=afb, role=role)

        queryset = manager.filter_queryset(
            super().get_queryset().exclude(instance_state__name="new"), None
        )

        return (
            queryset.annotate(
                gis_data=self.annotate_gis_data(),
                dossier_number=self.annotate_dossier_number(),
                responsible_user=self.annotate_responsible_user(),
                intent=self.annotate_intent(),
                url=self.annotate_url(),
                municipality=self.annotate_municipality(),
                plot_number=self.annotate_plot_number(),
                status=self.annotate_status(),
                applicant=self.annotate_applicant(),
                submit_date=self.annotate_submit_date(),
                type=self.annotate_type(),
            )
            .select_related("case", "case__document", "case__document__form")
            .only(
                "case__family",
                "case__meta",
                "case__document__family",
                "case__document__form",
                "case__document__form__name",
                "instance_state",
            )
        )


class InstanceProxyAG(InstanceProxy, Instance):
    fields = [
        "instance_id",
        "coordinate_x",
        "coordinate_y",
        "dossier_number",
        "responsible_user",
        "intent",
        "url",
        "municipality",
        "plot_number",
        "status",
        "applicant",
        "submit_date",
        "type",
    ]

    objects = InstanceManagerAG()

    @cached_property
    def coordinates(self):
        gis_data = self.gis_data.replace("\\", '"')
        json_data = json.loads(gis_data)
        coordinates = json_data.get("markers")
        if not coordinates or not isinstance(coordinates, list):  # pragma: no cover
            return None

        return coordinates

    @property
    def coordinate_x(self):
        if not self.coordinates:  # pragma: no cover
            return None

        return self.coordinates[0].get("x")

    @property
    def coordinate_y(self):
        if not self.coordinates:  # pragma: no cover
            return None

        return self.coordinates[0].get("y")

    class Meta:
        proxy = True


class GISExport(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True, db_index=True)
    hash = models.CharField()

    instance = models.OneToOneField(
        to="instance.Instance",
        on_delete=models.CASCADE,
        related_name="+",
        primary_key=True,
    )

    class Meta:
        abstract = True


class AGGISExport(GISExport):
    coordinate_x = models.FloatField(blank=True, null=True)
    coordinate_y = models.FloatField(blank=True, null=True)
    dossier_number = models.CharField(blank=True, null=True)
    responsible_user = models.CharField(blank=True, null=True)
    intent = models.CharField(blank=True, null=True)
    url = models.CharField()
    municipality = models.CharField(blank=True, null=True)
    plot_number = models.CharField(blank=True, null=True)
    status = models.CharField()
    applicant = models.CharField(blank=True, null=True)
    submit_date = models.DateField(blank=True, null=True)
    type = models.CharField()
