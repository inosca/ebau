import hashlib
import json
from abc import ABCMeta, abstractmethod

from caluma.caluma_form.models import Answer, AnswerDocument, DynamicOption, Option
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.contrib.postgres.expressions import ArraySubquery
from django.db import models
from django.db.models import (
    Case,
    CharField,
    Exists,
    F,
    Manager,
    OuterRef,
    Q,
    Subquery,
    Value,
    When,
)
from django.db.models.expressions import Func
from django.db.models.functions import (
    Cast,
    Concat,
    JSONObject,
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
from camac.user.models import Role, Service, ServiceT


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
        return Case(
            When(instance_state__name="subm", then=Value("Pruefung.formell")),
            When(
                instance_state__name="material-exam", then=Value("Pruefung.materiell")
            ),
            When(instance_state__name="correction", then=Value("in_Korrektur")),
            When(instance_state__name="reject", then=Value("zur_Rueckweisung")),
            When(instance_state__name="rejected", then=Value("zurueckgewiesen")),
            When(instance_state__name="withdrawal", then=Value("zum_Rueckzug")),
            When(instance_state__name="withdrawn", then=Value("zurueckgezogen")),
            When(
                instance_state__name="init-distribution",
                then=Value("Zirkulation_initialisieren"),
            ),
            When(instance_state__name="distribution", then=Value("in_Zirkulation")),
            When(instance_state__name="decision", then=Value("Entscheid")),
            When(instance_state__name="decided", then=Value("entschieden")),
            When(
                instance_state__name="construction-monitoring",
                then=Value("Baubegleitung"),
            ),
            When(instance_state__name="finished", then=Value("abgeschlossen")),
            default=Value(None),
            output_field=models.CharField(),
        )

    def annotate_ebau_link(self):
        return Concat(
            Value(f"{settings.INTERNAL_BASE_URL}/cases/"),
            F("instance_id"),
            output_field=models.CharField(),
        )

    def annotate_gesuchssteller_vertretung(self):
        return JSONObject(
            natuerliche_person=JSONObject(
                name=caluma_answer(
                    "vertretung-nachname",
                    "case__document_id",
                ),
                vorname=caluma_answer(
                    "vertretung-vorname",
                    "case__document_id",
                ),
            ),
            juristische_person=JSONObject(
                name=caluma_answer(
                    "vertretung-juristische-person-name",
                    "case__document_id",
                ),
            ),
            adresse=JSONObject(
                strassenname=caluma_answer(
                    "vertretung-strasse",
                    "case__document_id",
                ),
                hausnummer=caluma_answer(
                    "vertretung-nummer",
                    "case__document_id",
                ),
                plz=caluma_answer(
                    "vertretung-plz",
                    "case__document_id",
                ),
                ortschaft=caluma_answer(
                    "vertretung-ort",
                    "case__document_id",
                ),
            ),
        )

    def annotate_projektverfasser(self):
        return self._annotate_personen_adresse("projektverfasserin")

    def annotate_rechnungsempfaenger(self):
        return self._annotate_personen_adresse("rechnungsempfaengerin")

    def annotate_grundeigentuemer(self):
        return self._annotate_personen_adresse("grundeigentuemerin")

    def _annotate_multiple_choice_labels(self, question):
        selected_option_slugs = (
            Answer.objects.filter(
                question_id=question,
                document_id=OuterRef(OuterRef("case__document_id")),
            )
            .annotate(
                option_slug=Func(
                    F("value"),
                    function="jsonb_array_elements_text",
                    output_field=CharField(),
                ),
            )
            .values("option_slug")
        )

        return ArraySubquery(
            Option.objects.filter(pk__in=Subquery(selected_option_slugs))
            .order_by("pk")
            .values(f"label__{get_language()}")
        )

    def annotate_bauprojekt(self):
        nutzungszwecke = StringAggSubquery(
            Option.objects.filter(
                pk__in=Subquery(
                    Answer.objects.filter(
                        question_id="nutzungszwecke",
                        document_id=OuterRef(OuterRef("case__document_id")),
                    )
                    .annotate(
                        option_slug=Func(
                            F("value"),
                            function="jsonb_array_elements_text",
                            output_field=CharField(),
                        ),
                    )
                    .values("option_slug")
                )
            ).values(f"label__{get_language()}"),
            column_name=f"label__{get_language()}",
            delimiter=", ",
        )

        return JSONObject(
            beschreibung=caluma_answer("kurzbeschreibung-bauprojekt"),
            bauwerk_art=self._annotate_multiple_choice_labels("art-der-bauwerke"),
            nutzungszweck=nutzungszwecke,
        )

    def annotate_entscheid(self):
        entscheid = Answer.objects.filter(
            question_id="entscheid-entscheid",
            document__work_item__task_id="decision",
            document__work_item__status=WorkItem.STATUS_COMPLETED,
            document__work_item__case__family=OuterRef("case__family"),
        ).values("value")[:1]

        datum = Answer.objects.filter(
            question_id="decision-date",
            document__work_item__task_id="decision",
            document__work_item__status=WorkItem.STATUS_COMPLETED,
            document__work_item__case__family=OuterRef("case__family"),
        ).values("date")[:1]

        return JSONObject(
            entscheid=Subquery(entscheid),
            datum=Subquery(datum),
        )

    def annotate_publikation(self):
        startdatum = Answer.objects.filter(
            question_id="publikation-start",
            document__work_item__task_id="fill-publication",
            document__work_item__status=WorkItem.STATUS_COMPLETED,
            document__work_item__case__family=OuterRef("case__family"),
        ).values("date")[:1]

        enddatum = Answer.objects.filter(
            question_id="publikation-ende",
            document__work_item__task_id="fill-publication",
            document__work_item__status=WorkItem.STATUS_COMPLETED,
            document__work_item__case__family=OuterRef("case__family"),
        ).values("date")[:1]

        return JSONObject(
            startdatum=Subquery(startdatum),
            enddatum=Subquery(enddatum),
        )

    def annotate_zirkulation(self):
        service_name = ServiceT.objects.filter(
            service_id=OuterRef("pk"),
            language=get_language(),
        ).values("name")[:1]

        inquiries = (
            WorkItem.objects.filter(
                task_id="inquiry",
                case__family=OuterRef("case__family"),
                addressed_groups__0__isnull=False,
            )
            .exclude(status=WorkItem.STATUS_SUSPENDED)
            .annotate(
                service_id=Cast(
                    F("addressed_groups__0"),
                    output_field=models.IntegerField(),
                )
            )
            .annotate(
                data=Subquery(
                    Service.objects.filter(
                        pk=OuterRef("service_id"),
                    )
                    .annotate(
                        data=JSONObject(
                            fachstelle=Case(
                                When(
                                    service_group__slug="municipality",
                                    then=Value("Gemeinde"),
                                ),
                                When(
                                    service_group__slug="service-extra-cantonal",
                                    then=Value("ausserkantonale_Fachstelle"),
                                ),
                                When(
                                    Q(slug="afu") | Q(service_parent__slug="afu"),
                                    then=Value("AFU"),
                                ),
                                When(
                                    Q(slug="arp") | Q(slug__startswith="arp-"),
                                    then=Value("ARP"),
                                ),
                                When(pk=110, then=Value("AMB")),
                                When(
                                    Q(slug="awa-arbeitsinspektorat") | Q(pk=133),
                                    then=Value("AWA"),
                                ),
                                When(slug="awjf", then=Value("AWJF")),
                                When(slug="denkmalpflege", then=Value("ADA")),
                                When(slug="gesundheitsamt", then=Value("GESA")),
                                When(slug="sgv", then=Value("SGV")),
                                When(slug="alw", then=Value("ALW")),
                                When(slug="avt", then=Value("AVT")),
                                default=Value("ausserkantonale_Fachstelle"),
                                output_field=models.CharField(),
                            ),
                            name=Subquery(service_name),
                            abteilung=Subquery(service_name),
                        )
                    )
                    .values("data")[:1]
                )
            )
            .values("data")
        )

        return ArraySubquery(inquiries)

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
                    fachstelle=Case(
                        When(
                            service__service_group__slug="municipality",
                            then=Value("Gemeinde"),
                        ),
                        When(
                            service__service_group__slug="service-extra-cantonal",
                            then=Value("ausserkantonale_Fachstelle"),
                        ),
                        When(
                            Q(service__slug="afu")
                            | Q(service__service_parent__slug="afu"),
                            then=Value("AFU"),
                        ),
                        When(
                            Q(service__slug="arp")
                            | Q(service__slug__startswith="arp-"),
                            then=Value("ARP"),
                        ),
                        When(service_id=110, then=Value("AMB")),
                        When(
                            Q(service__slug="awa-arbeitsinspektorat")
                            | Q(service_id=133),
                            then=Value("AWA"),
                        ),
                        When(service__slug="awjf", then=Value("AWJF")),
                        When(service__slug="denkmalpflege", then=Value("ADA")),
                        When(service__slug="gesundheitsamt", then=Value("GESA")),
                        When(service__slug="sgv", then=Value("SGV")),
                        When(service__slug="alw", then=Value("ALW")),
                        When(service__slug="avt", then=Value("AVT")),
                        default=Value("ausserkantonale_Fachstelle"),
                        output_field=models.CharField(),
                    ),
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
            .values("data")[:1]
        )

    def annotate_lokalisation(self):
        # TODO: Implement Caluma source mapping.
        return Value(None, output_field=models.JSONField())

    def annotate_geometrie_linie(self):
        # TODO: Implement Caluma source mapping.
        return Value(None, output_field=models.JSONField())

    def annotate_geometrie_flaeche(self):
        # TODO: Implement Caluma source mapping.
        return Value(None, output_field=models.JSONField())

    def annotate_ausserhalb_bauzone(self):
        return Case(
            When(Q(case__meta__contains={"is-bab": True}), then=Value(True)),
            default=Value(False),
            output_field=models.BooleanField(),
        )

    def _annotate_personen_adresse(
        self,
        table_question,
        name_question="nachname",
        vorname_question="vorname",
        juristische_person_question="juristische-person-name",
    ):
        person_data = {
            "natuerliche_person": JSONObject(
                name="name",
                vorname="vorname",
            ),
            "adresse": JSONObject(
                strassenname="strassenname",
                hausnummer="hausnummer",
                plz="plz",
                ortschaft="ortschaft",
            ),
        }

        if juristische_person_question:
            person_data["juristische_person"] = JSONObject(
                name=caluma_answer(
                    juristische_person_question,
                    "document_id",
                ),
            )

        return Subquery(
            AnswerDocument.objects.filter(
                answer__question_id=table_question,
                answer__document_id=OuterRef("case__document_id"),
            )
            .annotate(
                name=caluma_answer(name_question, "document_id"),
                vorname=caluma_answer(vorname_question, "document_id"),
                strassenname=caluma_answer("strasse", "document_id"),
                hausnummer=caluma_answer("strasse-nummer", "document_id"),
                plz=caluma_answer("plz", "document_id"),
                ortschaft=caluma_answer("ort", "document_id"),
            )
            .order_by("-sort")
            .annotate(data=JSONObject(**person_data))
            .values("data")[:1],
            output_field=models.JSONField(),
        )

    def annotate_gesuchsteller(self):
        return self._annotate_personen_adresse(
            "bauherrin",
            juristische_person_question="juristische-person-name",
        )

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
                gesuchssteller=self.annotate_gesuchsteller(),
                gesuchssteller_vertretung=self.annotate_gesuchssteller_vertretung(),
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
        "gesuchssteller",
        "gesuchssteller_vertretung",
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


class SOGISExport(GISExport):
    identifikator = models.CharField()
    bfsnr = models.IntegerField(blank=True, null=True)
    verfahrensart = models.CharField()
    status = models.CharField()
    gesuchssteller = models.JSONField(blank=True, null=True)
    gesuchssteller_vertretung = models.JSONField(blank=True, null=True)
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
