import requests
from django.conf import settings
from django.db.models import Exists, F, OuterRef, Q
from django.utils.module_loading import import_string
from pyproj import CRS, Transformer
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_json_api import django_filters, filters as json_api_filters
from rest_framework_json_api.views import ModelViewSet, ReadOnlyModelViewSet

from camac.caluma.api import CalumaApi
from camac.caluma.models import Inquiry
from camac.core.utils import canton_aware
from camac.instance.mixins import InstanceQuerysetMixin
from camac.instance.models import FormField, Instance
from camac.user.permissions import (
    DefaultPermission,
    PublicationPermission,
    permission_aware,
)

from . import filters, models, serializers


class EnforcePaginationMixin:
    def paginate_queryset(self, queryset):
        """Paginate the queryset.

        Enforce pagination on this viewset. If clients don't pass page
        information (page[number] and optional page[size]), a validation error
        will be thrown.

        You can define a custom maximum page size by defining `max_page_size`
        on your viewset class. If you don't, a default of 100 is used.

        You can define a default page size by defining `default_page_size`
        on your viewset class. If you don't, a default of 20 is used.
        """

        if "page[number]" not in self.request.query_params:
            raise ValidationError("Pagination is required")

        default_page_size = getattr(self, "default_page_size", 20)
        page_size = int(self.request.query_params.get("page[size]", default_page_size))

        max_page_size = getattr(self, "max_page_size", 100)

        if page_size == 0 or page_size > max_page_size:
            raise ValidationError(
                f"Pagination outside permissible range. Max page size: {max_page_size}"
            )

        return super().paginate_queryset(queryset)


class MultilangMixin:
    def _is_multilang_model(self, model):
        return issubclass(model, models.MultilingualModel)

    def _get_included_serializer(self, serializer, path):
        parts = path.split(".")

        for i, part in enumerate(parts, 1):
            included = getattr(serializer, "included_serializers", {}).get(part)

            # if it's a string, import the class
            if isinstance(included, str):
                included = import_string(included)

            # if it's a nested include follow the path
            if i < len(parts):
                return self._get_included_serializer(included, ".".join(parts[i:]))

            return included

    def _get_multilang_prefetch_for_include(self, serializer, include):
        included_serializer = self._get_included_serializer(serializer, include)

        # included model is not multilang, continue
        if not self._is_multilang_model(included_serializer.Meta.model):
            return None

        lookup = "__".join(include.split("."))
        return [f"{lookup}__trans"]

    def get_prefetch_related(self, include):
        prefetch_for_include = super().get_prefetch_related(include)

        if not settings.APPLICATION.get("IS_MULTILINGUAL"):
            return prefetch_for_include

        # the direct translation models must always be prefetched
        if include == "__all__":
            if self._is_multilang_model(self.queryset.model):
                return (prefetch_for_include if prefetch_for_include else []) + [
                    "trans"
                ]

            return prefetch_for_include

        multilang_prefetch_for_include = self._get_multilang_prefetch_for_include(
            self.serializer_class, include
        )

        prefetch = set()
        if prefetch_for_include:
            prefetch.update(prefetch_for_include)
        if multilang_prefetch_for_include:
            prefetch.update(multilang_prefetch_for_include)

        return list(prefetch) if len(prefetch) else None

    def get_queryset(self):
        queryset = super().get_queryset()

        if settings.APPLICATION.get("IS_MULTILINGUAL") and self._is_multilang_model(
            queryset.model
        ):
            return queryset.prefetch_related("trans")

        return queryset


class PublicationEntryView(ModelViewSet):
    filterset_class = filters.PublicationEntryFilterSet
    serializer_class = serializers.PublicationEntrySerializer
    queryset = models.PublicationEntry.objects.all()
    prefetch_for_includes = {"instance": ["instance"]}
    filter_backends = (
        json_api_filters.OrderingFilter,
        django_filters.DjangoFilterBackend,
    )
    ordering = ["instance__location__name", "publication_date", "instance__identifier"]

    @permission_aware
    def get_queryset(self):
        return models.PublicationEntry.objects.none()

    def get_queryset_for_municipality(self):
        return models.PublicationEntry.objects.filter(
            instance__group__service_id=self.request.group.service_id
        )

    def get_queryset_for_service(self):
        if settings.DISTRIBUTION:
            return models.PublicationEntry.objects.filter(
                Exists(
                    Inquiry.objects.for_instance(OuterRef("instance"))
                    .addressed_to(self.request.group.service_id)
                    .only_active()
                )
            )

        return models.PublicationEntry.objects.filter(
            instance__circulations__activations__service=self.request.group.service
        )

    def get_queryset_for_canton(self):
        return models.PublicationEntry.objects.none()

    def get_queryset_for_reader(self):
        if settings.DISTRIBUTION:
            return models.PublicationEntry.objects.filter(
                Q(instance__group__service_id=self.request.group.service_id)
                | Exists(
                    Inquiry.objects.for_instance(OuterRef("instance"))
                    .addressed_to(self.request.group.service_id)
                    .only_active()
                )
            )

        return models.PublicationEntry.objects.filter(
            instance__circulations__activations__service=self.request.group.service
        )

    @permission_aware
    def has_create_permission(self):
        return False

    def has_create_permission_for_municipality(self):
        return True

    @permission_aware
    def has_update_permission(self):
        return False

    def has_update_permission_for_municipality(self):
        return True

    @permission_aware
    def has_destroy_permission(self):
        return False

    def has_destroy_permission_for_municipality(self):
        return True

    def _clean_persons(self, persons, type=""):
        persons_data = []
        for person in persons:
            person_data = {
                "firma": person.get("firma", ""),
                "vorname": person.get("vorname", ""),
                "nachname": person.get("name", ""),
                "adresse": person.get("strasse", ""),
                "plz": person.get("plz", ""),
                "ort": person.get("ort", ""),
            }

            # We only use the title of grundeigentuemer because the external Amtsblatt API
            # only uses a title on grundeigentuemer
            if type == "grundeigentuemer":
                anrede_mapping = {
                    "Herr": "Grundeigentümer",
                    "Frau": "Grundeigentümerin",
                    "Firma": "Grundeigentümer",
                }

                person_data["anrede"] = (
                    anrede_mapping[person["anrede"]]
                    if "anrede" in person
                    else "Diverse"
                )
            persons_data.append(person_data)

        return persons_data

    @action(methods=["post"], detail=True)
    def publish(self, request, pk=None):  # noqa: C901
        payload = {}
        publication = self.get_object()
        formFieldQuery = FormField.objects.filter(instance=publication.instance)

        payload["bfs_nr"] = int(publication.instance.location.communal_federal_number)

        payload["publikation_datum"] = publication.publication_date.strftime("%d.%m.%Y")

        bauzone = formFieldQuery.filter(name="lage").first()
        if bauzone:
            bauzone = bauzone.value
            payload["bauzone"] = bauzone if bauzone != "beides" else "ausserhalb"

        bauherrschaften_field = formFieldQuery.filter(
            name__in=["bauherrschaft", "bauherrschaft-v2", "bauherrschaft-v3"]
        ).first()
        bauherrschaften_override = formFieldQuery.filter(
            name="bauherrschaft-override"
        ).first()
        bauherrschaften = bauherrschaften_override or bauherrschaften_field
        if bauherrschaften:
            payload["bauherrschaften"] = self._clean_persons(bauherrschaften.value)

        projektverfasser_field = formFieldQuery.filter(
            name__in=[
                "projektverfasser-planer",
                "projektverfasser-planer-v2",
                "projektverfasser-planer-v3",
            ]
        ).first()
        projektverfasser_override = formFieldQuery.filter(
            name="projektverfasser-planer-override"
        ).first()
        projektverfasser = projektverfasser_override or projektverfasser_field
        if projektverfasser:
            payload["projektverfasser"] = self._clean_persons(projektverfasser.value)

        grundeigentuemer_field = formFieldQuery.filter(
            name__in=["grundeigentumerschaft", "grundeigentumerschaft-v2"]
        ).first()
        grundeigentuemer_override = formFieldQuery.filter(
            name="grundeigentumerschaft-override"
        ).first()
        grundeigentuemer = grundeigentuemer_override or grundeigentuemer_field
        if grundeigentuemer:
            payload["grundeigentuemer"] = self._clean_persons(
                grundeigentuemer.value, "grundeigentuemer"
            )

        bezeichnung = formFieldQuery.get(name="bezeichnung").value
        bezeichnung_override = formFieldQuery.filter(
            name="bezeichnung-override"
        ).first()
        if bezeichnung_override:
            bezeichnung = bezeichnung_override.value
        payload["bauobjekte"] = [{"bezeichnung": bezeichnung}]

        adresse = formFieldQuery.filter(name="ortsbezeichnung-des-vorhabens").first()
        spezialbezeichnung = formFieldQuery.filter(
            name="standort-spezialbezeichnung"
        ).first()
        ort = formFieldQuery.filter(name="standort-ort").first()
        payload["standorte"] = [
            {
                "adresse": adresse.value if adresse else "",
                "spezialbezeichnung": (
                    spezialbezeichnung.value if spezialbezeichnung else ""
                ),
                "ort": ort.value if ort else "",
            }
        ]

        grundstuecknummern = []
        for parcel in formFieldQuery.get(name="parzellen").value:
            grundstuecknummern.append({"type": "KTN", "nummer": parcel["number"]})
        payload["grundstuecknummern"] = grundstuecknummern

        standort_koordinaten = formFieldQuery.filter(name="standort-koordinaten")
        coordinates_override = []
        if standort_koordinaten.exists():
            coordinates = standort_koordinaten.first().value.strip().splitlines()
            for coordinate in coordinates:
                coordinate = [c.strip() for c in coordinate.split(";")]
                coordinates_override.append(
                    [
                        {
                            "lat": coordinate[0],
                            "lng": coordinate[1],
                            "skip_transform": True,
                        }
                    ]
                )

        koordinaten = []
        transformer = Transformer.from_crs(
            "EPSG:4326",
            CRS.from_proj4(
                "+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs"
            ),
        )

        for coordSet in coordinates_override or formFieldQuery.get(name="punkte").value:
            if not isinstance(coordSet, list):
                coordSet = [coordSet]
            for coord in coordSet:
                lat = coord["lat"]
                lng = coord["lng"]
                if "skip_transform" not in coord or not coord["skip_transform"]:
                    lat, lng = transformer.transform(lat, lng)
                lat = f"{int(lat)}"
                lng = f"{int(lng)}"
                koordinaten.append(
                    {
                        # This formats the coordinates to "2 700 000", because the api only supports this format
                        "koordinate_1": " ".join((lat[:1], lat[1:4], lat[4:])),
                        "koordinate_2": " ".join((lng[:1], lng[1:4], lng[4:])),
                        "hinweis": "",
                    }
                )

        payload["koordinaten"] = koordinaten

        bemerkung = formFieldQuery.filter(name="publikation-bemerkung").first()
        if bemerkung:
            payload["bemerkungen"] = [{"type": "", "text": bemerkung.value}]

        response = requests.post(
            settings.PUBLICATION_API_URL,
            json=payload,
            auth=(settings.PUBLICATION_API_USER, settings.PUBLICATION_API_PASSWORD),
        )

        # Return 400 when a error occured at the Amtsblatt API
        if not response.ok:  # pragma: no cover
            return Response(response.text, 400)

        return Response([], 204)

    @action(methods=["get"], detail=False)
    def no_publication(self, request):
        CalumaApi().close_publication(
            Instance.objects.get(pk=request.query_params["instance"]),
            request.caluma_info.context.user,
        )

        return Response([], 204)

    @action(methods=["post"], detail=True)
    def viewed(self, request, pk=None):
        models.PublicationEntry.objects.filter(pk=pk).update(
            publication_views=F("publication_views") + 1
        )
        return Response([], 204)


class AuthorityView(ReadOnlyModelViewSet):
    """Only used in Kt. UR for 'Leitbehörde'."""

    serializer_class = serializers.AuthoritySerializer
    queryset = models.Authority.objects.all()


class WorkflowEntryView(InstanceQuerysetMixin, ReadOnlyModelViewSet):
    """Only used in Kt. UR."""

    serializer_class = serializers.WorkflowEntrySerializer
    queryset = models.WorkflowEntry.objects.all()
    filterset_class = filters.WorkflowEntryFilterSet

    # Queryset for internal role permissions are handled
    # by InstanceQuerysetMixin
    def get_queryset_for_applicant(self):
        return self.queryset.none()

    def get_queryset_for_public(self):
        return self.queryset.none()


class ResourceView(ReadOnlyModelViewSet):
    serializer_class = serializers.ResourceSerializer
    queryset = models.Resource.objects.filter(hidden=False).order_by("sort")

    prefetch_for_includes = {"__all__": ["trans"]}

    def _get_queryset(self):
        return super().get_queryset().filter(role_acls__role=self.request.group.role)

    @canton_aware
    def get_queryset(self):
        return self._get_queryset()

    def get_queryset_ag(self):
        # In Kt. AG, "light" municipalities should not see the global GWR resource
        # and the statistics export.
        # If we have more use cases for dynamic resource visibility, extract this
        # into something more generic.
        service = self.request.group.service
        if service and service.service_group.name == "municipality-light":
            return self._get_queryset().exclude(
                Q(template__contains="gwr-global")
                | Q(template__contains="statistics-export")
            )
        return self._get_queryset()


class InstanceResourceView(ReadOnlyModelViewSet):
    serializer_class = serializers.InstanceResourceSerializer
    filterset_class = filters.InstanceResourceFilterSet
    queryset = (
        models.InstanceResource.objects.filter(hidden=False).distinct().order_by("sort")
    )

    select_for_includes = {"__all__": ["ir_taskform", "resource", "form_group"]}
    prefetch_for_includes = {"__all__": ["trans"]}


class StaticContentView(ModelViewSet):
    permission_classes = [DefaultPermission | PublicationPermission]
    filterset_class = filters.StaticContentFilterSet
    queryset = models.StaticContent.objects.all()
    serializer_class = serializers.StaticContentSerializer

    @permission_aware
    def has_create_permission(self):
        return False

    def has_create_permission_for_support(self):
        return True

    @permission_aware
    def has_update_permission(self):
        return False

    def has_update_permission_for_support(self):
        return True

    @permission_aware
    def has_destroy_permission(self):
        return False

    def has_destroy_permission_for_support(self):
        return True


class ServiceContentViewSet(ReadOnlyModelViewSet):
    filterset_class = filters.ServiceContentFilterSet
    queryset = models.ServiceContent.objects.all()
    serializer_class = serializers.ServiceContentSerializer
    permission_classes = [DefaultPermission | PublicationPermission]
