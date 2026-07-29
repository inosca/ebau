import hashlib
import json
from abc import ABCMeta, abstractmethod
from logging import getLogger

from caluma.caluma_form.models import Answer, AnswerDocument, DynamicOption, Option
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.contrib.postgres.expressions import ArraySubquery
from django.db import models, transaction
from django.db.models import (
    Case,
    CharField,
    Exists,
    F,
    Func,
    Manager,
    OuterRef,
    Q,
    Subquery,
    Value,
    When,
)
from django.db.models.functions import (
    MD5,
    Cast,
    Concat,
    JSONObject,
    NullIf,
    Replace,
    Trim,
    TruncDate,
)
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.utils.translation import get_language

from camac.instance.export.filters import (
    StringAggSubquery,
    caluma_answer,
)
from camac.instance.models import Instance, InstanceStateT
from camac.permissions.api import PermissionManager
from camac.permissions.models import InstanceACL
from camac.responsible.models import ResponsibleService
from camac.user.models import Role, Service, ServiceT

log = getLogger(__name__)


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

        # Do not export draft dossiers. Therefore no Status_Geschaeft mapping
        # for "neu" is needed at this point.
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


class InstanceManagerSO(Manager["InstanceProxySO"]):
    """Custom manager for SO instance proxies."""

    def annotate_identifikator(self):
        return F("case__meta__dossier-number")

    def annotate_bfsnr(self):
        return caluma_answer("gemeindenummer-bfs")

    def annotate_verfahrensart(self):
        return F(f"case__family__document__form__name__{get_language()}")

    def annotate_status(self):
        # The instance state maps to a Status_Geschaeft enum in formatters._map_status
        return F("instance_state__name")

    def annotate_ebau_link(self):
        return Concat(
            Value(f"{settings.INTERNAL_BASE_URL}/cases/"),
            F("instance_id"),
            output_field=models.CharField(),
        )

    def annotate_gesuchsteller_vertretung(self):
        # TODO The fields Natuerliche_Person and Adresse
        # are madatory by the ILI Model definition. Since
        # the form for vertretung has all fields optional,
        # this mapping cant work.
        return Subquery(
            AnswerDocument.objects.filter(
                answer__question_id="bauherrin",
                answer__document_id=OuterRef("case__document_id"),
            )
            .annotate(
                vertretung=caluma_answer("vertretung", "document_id"),
                ist_juristische_person=caluma_answer(
                    "vertretung-juristische-person", "document_id"
                ),
            )
            .order_by("-sort")
            .annotate(
                data=Case(
                    When(
                        vertretung="vertretung-ja",
                        then=JSONObject(
                            natuerliche_person=JSONObject(
                                name=caluma_answer(
                                    "vertretung-nachname", "document_id"
                                ),
                                vorname=caluma_answer(
                                    "vertretung-vorname", "document_id"
                                ),
                            ),
                            juristische_person=Case(
                                When(
                                    ist_juristische_person=(
                                        "vertretung-juristische-person-ja"
                                    ),
                                    then=JSONObject(
                                        name=caluma_answer(
                                            "vertretung-juristische-person-name",
                                            "document_id",
                                        ),
                                    ),
                                ),
                                output_field=models.JSONField(),
                            ),
                            adresse=JSONObject(
                                strassenname=caluma_answer(
                                    "vertretung-strasse", "document_id"
                                ),
                                hausnummer=caluma_answer(
                                    "vertretung-nummer", "document_id"
                                ),
                                plz=caluma_answer("vertretung-plz", "document_id"),
                                ortschaft=caluma_answer(
                                    "vertretung-ort", "document_id"
                                ),
                            ),
                        ),
                    ),
                    output_field=models.JSONField(),
                )
            )
            .values("data")[:1],
            output_field=models.JSONField(),
        )

    def annotate_projektverfasser(self):
        return self._annotate_personen_adresse(
            "projektverfasserin", "projektverfasserin-abweichend"
        )

    def annotate_rechnungsempfaenger(self):
        return self._annotate_personen_adresse(
            "rechnungsempfaengerin", "rechnungsempfaengerin-abweichend"
        )

    def annotate_grundeigentuemer(self):
        return self._annotate_personen_adresse(
            "grundeigentuemerin", "grundeigentuemerin-abweichend"
        )

    def _get_option_labels(
        self, option_slug_func: Func, question: str, outer_ref: str | None = None
    ):
        outer_ref = outer_ref or "case__document_id"
        selected_option_slugs = (
            Answer.objects.filter(
                question_id=question,
                # This subquery is nested inside the option-slug subquery, so the
                # document reference reaches two OuterRefs out to the case.
                document_id=OuterRef(OuterRef(outer_ref)),
            )
            .annotate(
                option_slug=option_slug_func,
            )
            .values("option_slug")
        )

        return (
            Option.objects.filter(pk__in=Subquery(selected_option_slugs))
            .order_by("pk")
            .values(f"label__{get_language()}")
        )

    def _get_multiple_choice_option_labels(self, question, outer_ref=None):
        return self._get_option_labels(
            Func(
                F("value"),
                function="jsonb_array_elements_text",
                output_field=CharField(),
            ),
            question,
            outer_ref,
        )

    def _get_single_choice_option_label(self, question, outer_ref=None):
        return self._get_option_labels(
            Func(
                F("value"),
                template="%(expressions)s #>> '{}'",
                output_field=CharField(),
            ),
            question,
            outer_ref,
        )[:1]

    def annotate_bauprojekt(self):
        # TODO This wont work for Form Erdwärmesonde as they dont
        # have art-der-bauwerke. So we don't export it for now for
        # these dossiers. Same for is-paper.
        return Case(
            When(
                Exists(
                    Answer.objects.filter(
                        question_id="art-der-bauwerke",
                        document_id=OuterRef("case__document_id"),
                    )
                ),
                then=JSONObject(
                    beschreibung=caluma_answer("umschreibung-bauprojekt"),
                    bauwerk_art=ArraySubquery(
                        self._get_multiple_choice_option_labels("art-der-bauwerke")
                    ),
                    nutzungszweck=StringAggSubquery(
                        self._get_multiple_choice_option_labels("nutzungszwecke"),
                        column_name=f"label__{get_language()}",
                        delimiter=", ",
                    ),
                    bauwerke=ArraySubquery(
                        AnswerDocument.objects.filter(
                            answer__question_id="gebaeude",
                            answer__document_id=OuterRef("case__document_id"),
                        )
                        .order_by("-sort")
                        .annotate(
                            data=JSONObject(
                                bezeichnung=caluma_answer(
                                    "gebaeude-bezeichnung", "document_id"
                                ),
                                bauwerk_typ=self._get_single_choice_option_label(
                                    "typ-des-bauwerks", "document_id"
                                ),
                                egid=caluma_answer("egid", "document_id"),
                                arbeiten_art=ArraySubquery(
                                    self._get_multiple_choice_option_labels(
                                        "art-der-arbeiten", "document_id"
                                    ),
                                    column_name=f"label__{get_language()}",
                                    delimiter=", ",
                                ),
                                gebaeudekategorie=self._get_single_choice_option_label(
                                    "gebaeudekategorie", "document_id"
                                ),
                            )
                        )
                        .values("data")
                    ),
                ),
            )
        )

    def _has_completed_work_item(self, task):
        return Exists(
            WorkItem.objects.filter(
                task_id=task,
                status=WorkItem.STATUS_COMPLETED,
                case__family=OuterRef("case__family"),
            )
        )

    def _completed_work_item_answer(self, task, question, field):
        return Subquery(
            Answer.objects.filter(
                question_id=question,
                document__work_item__task_id=task,
                document__work_item__status=WorkItem.STATUS_COMPLETED,
                document__work_item__case__family=OuterRef("case__family"),
            ).values(field)[:1]
        )

    def annotate_entscheid(self):
        return Case(
            When(
                self._has_completed_work_item("decision"),
                then=JSONObject(
                    entscheid=self._completed_work_item_answer(
                        "decision", "entscheid-entscheid", "value"
                    ),
                    datum=self._completed_work_item_answer(
                        "decision", "entscheid-datum", "date"
                    ),
                ),
            )
        )

    def annotate_publikation(self):
        return Case(
            When(
                self._has_completed_work_item("fill-publication"),
                then=JSONObject(
                    startdatum=self._completed_work_item_answer(
                        "fill-publication", "publikation-start", "date"
                    ),
                    enddatum=self._completed_work_item_answer(
                        "fill-publication", "publikation-ende", "date"
                    ),
                ),
            )
        )

    def annotate_zirkulation(self):
        service_name = ServiceT.objects.filter(
            service_id=OuterRef("pk"),
            language=get_language(),
        ).values("name")[:1]

        inquiry_services = (
            Service.objects.filter(
                pk__in=InstanceACL.objects.filter(
                    access_level_id="distribution-service",
                    instance_id=OuterRef(OuterRef("pk")),
                ).values("service__pk")
            )
            .annotate(
                data=JSONObject(
                    slug=F("slug"),
                    parent_slug=F("service_parent__slug"),
                    group_slug=F("service_group__slug"),
                    name=Value(None),
                    abteilung=Subquery(service_name),
                )
            )
            .order_by("pk")
            .values("data")
        )

        return ArraySubquery(inquiry_services)

    def annotate_zustaendige_person(self):
        service_name = ServiceT.objects.filter(
            service_id=OuterRef("service_id"),
            language=get_language(),
        ).values("name")[:1]

        return Subquery(
            ResponsibleService.objects.filter(
                instance_id=OuterRef("pk"),
            )
            .annotate(
                data=JSONObject(
                    slug=F("service__slug"),
                    parent_slug=F("service__service_parent__slug"),
                    group_slug=F("service__service_group__slug"),
                    name=Trim(
                        Concat(
                            Trim(F("responsible_user__name")),
                            Value(" "),
                            Trim(F("responsible_user__surname")),
                        )
                    ),
                    abteilung=Subquery(service_name),
                )
            )
            .order_by("pk")
            .values("data")[:1]
        )

    def annotate_lokalisation(self):
        # TODO According to ILI PLZ and ORT are required but
        # in the form they are not. for now we only export if they
        # are present but this means missing data if the rest was filled
        # out.
        return Case(
            When(
                Exists(
                    Answer.objects.filter(
                        question_id="plz",
                        document_id=OuterRef("case__document_id"),
                    )
                )
                & Exists(
                    Answer.objects.filter(
                        question_id="ort",
                        document_id=OuterRef("case__document_id"),
                    )
                ),
                then=JSONObject(
                    strassenname=caluma_answer("strasse-flurname"),
                    hausnummer=caluma_answer("strasse-nummer"),
                    plz=caluma_answer("plz"),
                    ortschaft=caluma_answer("ort"),
                ),
            )
        )

    def annotate_geometrie_linie(self):
        # Not yet implemented in form
        return Value(None, output_field=models.JSONField())

    def annotate_geometrie_flaeche(self):
        # Not yet implemented in form
        return Value(None, output_field=models.JSONField())

    def annotate_ausserhalb_bauzone(self):
        return Case(
            When(Q(case__meta__contains={"is-bab": True}), then=Value(True)),
            default=Value(False),
            output_field=models.BooleanField(),
        )

    def _annotate_personen_adresse(self, table_question, abweichend_question=None):
        person = Subquery(
            AnswerDocument.objects.filter(
                answer__question_id=table_question,
                answer__document_id=OuterRef("case__document_id"),
            )
            .annotate(
                ist_juristische_person=caluma_answer(
                    "juristische-person", "document_id"
                ),
            )
            .order_by("-sort")
            .annotate(
                data=JSONObject(
                    juristische_person=Case(
                        When(
                            ist_juristische_person="juristische-person-ja",
                            then=JSONObject(
                                name=caluma_answer(
                                    "juristische-person-name", "document_id"
                                ),
                            ),
                        ),
                        output_field=models.JSONField(),
                    ),
                    natuerliche_person=JSONObject(
                        name=caluma_answer("nachname", "document_id"),
                        vorname=caluma_answer("vorname", "document_id"),
                    ),
                    adresse=JSONObject(
                        strassenname=caluma_answer("strasse", "document_id"),
                        hausnummer=caluma_answer("strasse-nummer", "document_id"),
                        plz=caluma_answer("plz", "document_id"),
                        ortschaft=caluma_answer("ort", "document_id"),
                    ),
                )
            )
            .values("data")[:1],
            output_field=models.JSONField(),
        )

        if abweichend_question is None:
            return person

        return Case(
            When(
                Exists(
                    Answer.objects.filter(
                        question_id=abweichend_question,
                        document_id=OuterRef("case__document_id"),
                        value=f"{abweichend_question}-ja",
                    )
                ),
                then=person,
            ),
            output_field=models.JSONField(),
        )

    def annotate_gesuchsteller(self):
        return self._annotate_personen_adresse("bauherrin")

    def annotate_geometrie_punkt(self):
        return Subquery(
            AnswerDocument.objects.filter(
                answer__question_id="parzellen",
                answer__document_id=OuterRef("case__document_id"),
            )
            .annotate(
                ost=caluma_answer("lagekoordinaten-ost", "document_id"),
                nord=caluma_answer("lagekoordinaten-nord", "document_id"),
            )
            .order_by("-sort")
            .annotate(data=JSONObject(ost="ost", nord="nord"))
            .values("data")[:1],
            output_field=models.JSONField(),
        )

    def annotate_grundstuecke(self):
        return ArraySubquery(
            AnswerDocument.objects.filter(
                answer__question_id="parzellen",
                answer__document_id=OuterRef("case__document_id"),
            )
            .annotate(
                nummer=caluma_answer("parzellennummer", "document_id"),
                egrid=caluma_answer("e-grid", "document_id"),
            )
            .order_by("-sort")
            .annotate(data=JSONObject(nummer="nummer", egrid="egrid"))
            .values("data")
        )

    def get_queryset(self):
        """Return the annotated base queryset for the SO GIS export."""

        # Export all submitted/in-process SO dossiers, independent of ACLs.
        # Do not export draft dossiers. Therefore no Status_Geschaeft mapping
        # for "neu" is needed at this point.
        queryset = super().get_queryset().exclude(instance_state__name="new")

        return (
            queryset.annotate(
                identifikator=self.annotate_identifikator(),
                bfsnr=self.annotate_bfsnr(),
                verfahrensart=self.annotate_verfahrensart(),
                status=self.annotate_status(),
                gesuchsteller=self.annotate_gesuchsteller(),
                gesuchsteller_vertretung=self.annotate_gesuchsteller_vertretung(),
                projektverfasser=self.annotate_projektverfasser(),
                rechnungsempfaenger=self.annotate_rechnungsempfaenger(),
                grundeigentuemer=self.annotate_grundeigentuemer(),
                ausserhalb_bauzone=self.annotate_ausserhalb_bauzone(),
                bauprojekt=self.annotate_bauprojekt(),
                grundstuecke=self.annotate_grundstuecke(),
                entscheid=self.annotate_entscheid(),
                publikation=self.annotate_publikation(),
                zirkulation=self.annotate_zirkulation(),
                zustaendige_person=self.annotate_zustaendige_person(),
                ebau_link=self.annotate_ebau_link(),
                lokalisation=self.annotate_lokalisation(),
                geometrie_punkt=self.annotate_geometrie_punkt(),
                geometrie_linie=self.annotate_geometrie_linie(),
                geometrie_flaeche=self.annotate_geometrie_flaeche(),
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


class InstanceProxySO(InstanceProxy, Instance):
    fields_for_update = [
        "identifikator",
        "bfsnr",
        "verfahrensart",
        "status",
        "gesuchsteller",
        "gesuchsteller_vertretung",
        "projektverfasser",
        "rechnungsempfaenger",
        "grundeigentuemer",
        "ausserhalb_bauzone",
        "bauprojekt",
        "grundstuecke",
        "entscheid",
        "publikation",
        "zirkulation",
        "zustaendige_person",
        "ebau_link",
        "lokalisation",
        "geometrie_punkt",
        "geometrie_linie",
        "geometrie_flaeche",
    ]
    fields = ["instance_id", *fields_for_update]

    objects = InstanceManagerSO()

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


class SOGISExportQuerySet(models.QuerySet):
    def pending(self):
        """Filter to the exports that still have to be delivered.

        `exported_at` is only written once the response body has been
        streamed, so anything never delivered or changed since last exported
        is exported again on the next run.
        """
        return self.filter(
            Q(exported_at__isnull=True) | Q(modified_at__gt=F("exported_at"))
        )


class SOGISExportManager(Manager.from_queryset(SOGISExportQuerySet)):
    def mark_exported(self, pks: list[int]) -> int:
        """Mark the given exports as delivered."""
        return self.filter(pk__in=pks).update(exported_at=now())

    @transaction.atomic
    def sync(self) -> None:
        """Create a SOGISExport model for all new Instances and update existing models for changed Instances."""

        # Hash all fields as JSONObject for comparing changed values
        hashed = InstanceProxySO.objects.annotate(
            last_exported_hash=self.filter(instance_id=OuterRef("pk")).values("hash")[
                :1
            ],
            hash=MD5(
                Cast(
                    JSONObject(**{name: F(name) for name in InstanceProxySO.fields}),
                    output_field=CharField(),
                )
            ),
        )

        new = hashed.filter(last_exported_hash__isnull=True).iterator(chunk_size=1000)

        # For new Instances, last_exported_hash will be null.
        created = self.bulk_create(
            [
                SOGISExport(**instance.fields_to_dict(), hash=instance.hash)
                for instance in new
            ],
            batch_size=500,
            # Two export runs at once both see the same instance as new and
            # race to insert it. Skipping the loser's duplicate keeps that a
            # non-event instead of an IntegrityError, and the row it wanted to
            # write is identical anyway.
            ignore_conflicts=True,
        )

        # Compare the hash in Python: `.exclude(hash=F("last_exported_hash"))` would inline the whole
        # MD5(JSONObject(...)) into the WHERE. So we first fetch only pk + the two hashes (each subquery
        # runs once, inside the hash instead of twice for a full select) and diff in Python, then select
        # the full field columns only for the rows we actually update.
        existing = (
            hashed.filter(last_exported_hash__isnull=False)
            .values("pk", "hash", "last_exported_hash")
            .iterator(chunk_size=2000)
        )
        ids_to_update = [
            row["pk"] for row in existing if row["hash"] != row["last_exported_hash"]
        ]

        updated_at = now()
        updated = [
            SOGISExport(
                **instance.fields_to_dict(),
                hash=instance.hash,
                modified_at=updated_at,
            )
            for instance in hashed.filter(pk__in=ids_to_update).iterator(
                chunk_size=1000
            )
        ]

        self.bulk_update(
            updated,
            [
                *InstanceProxySO.fields_for_update,
                "hash",
                "modified_at",
            ],
            batch_size=500,
        )

        log.info(f"Updated export entries for {len(updated)} instance(s).")
        log.info(f"Created export entries for {len(created)} instance(s).")


class SOGISExport(GISExport):
    identifikator = models.CharField()
    bfsnr = models.IntegerField(blank=True, null=True)
    verfahrensart = models.CharField()
    status = models.CharField()
    gesuchsteller = models.JSONField(blank=True, null=True)
    gesuchsteller_vertretung = models.JSONField(blank=True, null=True)
    projektverfasser = models.JSONField(blank=True, null=True)
    rechnungsempfaenger = models.JSONField(blank=True, null=True)
    grundeigentuemer = models.JSONField(blank=True, null=True)
    ausserhalb_bauzone = models.BooleanField(blank=True, null=True)
    bauprojekt = models.JSONField(blank=True, null=True)
    grundstuecke = models.JSONField(blank=True, null=True)
    entscheid = models.JSONField(blank=True, null=True)
    publikation = models.JSONField(blank=True, null=True)
    zirkulation = models.JSONField(blank=True, null=True)
    zustaendige_person = models.JSONField(blank=True, null=True)
    ebau_link = models.CharField()
    lokalisation = models.JSONField(blank=True, null=True)
    geometrie_punkt = models.JSONField(blank=True, null=True)
    geometrie_linie = models.JSONField(blank=True, null=True)
    geometrie_flaeche = models.JSONField(blank=True, null=True)
    exported_at = models.DateTimeField(blank=True, null=True, db_index=True)

    objects = SOGISExportManager()
