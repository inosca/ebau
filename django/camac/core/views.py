from pathlib import Path
from uuid import uuid4

import requests
from django.conf import settings
from django.db.models import F
from django.http import HttpResponse
from django.utils import timezone
from django.utils.encoding import escape_uri_path, smart_bytes
from django.utils.module_loading import import_string
from pyproj import CRS, Transformer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_json_api import django_filters, filters as json_api_filters
from rest_framework_json_api.views import ModelViewSet, ReadOnlyModelViewSet

from camac.caluma.api import CalumaApi
from camac.instance.mixins import InstanceQuerysetMixin
from camac.instance.models import FormField, Instance
from camac.user.permissions import permission_aware

from . import filters, models, serializers


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
    swagger_schema = None
    filterset_class = filters.PublicationEntryFilterSet
    serializer_class = serializers.PublicationEntrySerializer
    queryset = models.PublicationEntry.objects.all()
    prefetch_for_includes = {"instance": ["instance"]}
    filter_backends = (
        json_api_filters.OrderingFilter,
        django_filters.DjangoFilterBackend,
    )
    ordering_fields = ["publication_date", "instance__location__name"]
    ordering = ["publication_date"]

    @permission_aware
    def get_queryset(self):
        return models.PublicationEntry.objects.filter(
            publication_date__lte=timezone.now(),
            publication_end_date__gte=timezone.now(),
            is_published=True,
        )

    def get_queryset_for_municipality(self):
        return models.PublicationEntry.objects.filter(
            instance__group=self.request.group
        )

    def get_queryset_for_service(self):
        return models.PublicationEntry.objects.filter(
            instance__circulations__activations__service=self.request.group.service
        )

    def get_queryset_for_canton(self):
        return models.PublicationEntry.objects.none()

    def get_queryset_for_reader(self):
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

    def has_destroy_permission(self):
        return False

    def _clean_persons(self, persons, type=""):
        for person in persons:
            # We only use the title of grundeigentuemer because the external Amtsblatt API
            # only uses a title on grundeigentuemer
            if type == "grundeigentuemer":
                anrede_mapping = {
                    "Herr": "Grundeigentümer",
                    "Frau": "Grundeigentümerin",
                    "Firma": "Grundeigentümer",
                }
                person["anrede"] = anrede_mapping[person["anrede"]]
            else:
                del person["anrede"]

            person["adresse"] = person["strasse"]
            del person["strasse"]

            if "name" in person:
                person["nachname"] = person["name"]
                del person["name"]

            person.pop("email", None)
            person.pop("tel", None)

        return persons

    @action(methods=["post"], detail=True)  # noqa: C901
    def publish(self, request, pk=None):
        payload = {}
        publication = self.get_object()
        formFieldQuery = FormField.objects.filter(instance=publication.instance)

        payload["bfs_nr"] = int(publication.instance.location.communal_federal_number)

        payload["publikation_datum"] = publication.publication_date.strftime("%d.%m.%Y")

        bauzone = formFieldQuery.filter(name="lage").first()
        if bauzone:
            bauzone = bauzone.value
            payload["bauzone"] = bauzone if bauzone != "beides" else "ausserhalb"

        bauherrschaften = formFieldQuery.filter(name="bauherrschaft").first()
        bauherrschaften_v2 = formFieldQuery.filter(name="bauherrschaft-v2").first()
        bauherrschaften_override = formFieldQuery.filter(
            name="bauherrschaft-override"
        ).first()
        bauherrschaften = (
            bauherrschaften_override or bauherrschaften or bauherrschaften_v2
        )
        if bauherrschaften:
            payload["bauherrschaften"] = self._clean_persons(bauherrschaften.value)

        projektverfasser = formFieldQuery.filter(name="projektverfasser-planer").first()
        projektverfasser_v2 = formFieldQuery.filter(
            name="projektverfasser-planer-v2"
        ).first()
        projektverfasser_override = formFieldQuery.filter(
            name="projektverfasser-planer-override"
        ).first()
        projektverfasser = (
            projektverfasser_override or projektverfasser or projektverfasser_v2
        )
        if projektverfasser:
            payload["projektverfasser"] = self._clean_persons(projektverfasser.value)

        grundeigentuemer = formFieldQuery.filter(name="grundeigentumerschaft").first()
        grundeigentuemer_override = formFieldQuery.filter(
            name="grundeigentumerschaft-override"
        ).first()
        grundeigentuemer = grundeigentuemer_override or grundeigentuemer
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
                "spezialbezeichnung": spezialbezeichnung.value
                if spezialbezeichnung
                else "",
                "ort": ort.value if ort else "",
            }
        ]

        grundstuecknummern = []
        for parcel in formFieldQuery.get(name="parzellen").value:
            grundstuecknummern.append({"type": "KTN", "nummer": parcel["number"]})
        payload["grundstuecknummern"] = grundstuecknummern

        standort_koordinaten = formFieldQuery.filter(name="standort-koordinaten")
        if standort_koordinaten.exists():
            coordinates = standort_koordinaten.first().value.splitlines()
            coordinates_override = []
            for coordinate in coordinates:
                coordinate = coordinate.split()
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
                if not coord["skip_transform"]:
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


class SendfileHttpResponse(HttpResponse):
    """
    Special HttpResponse for x-sendfile with nginx.

    Wraps the django.http.HttpResponse and augments it with the necessary
    headers for x-sendfile with nginx.
    Accepts either `file_path` to a static file (probably from a `FileField`)
    or `file_obj` which represents a temporary download (to be stored with a random
    filename).

    :param content_type: Same as in the parent class
    :param filename: Content-Disposition header filename
    :param location: Base path which will be mapped with the nginx location
    :param base_path: Path to where nginx looks for files for given location
    :param file_path: Path to file inside `base_path`
    :param file_obj: File-like object for temporary downloads
    """

    def __init__(
        self,
        content_type: str,
        filename: str,
        base_path: str = None,
        file_path: str = None,
        file_obj: bytes = None,
    ):
        super().__init__(content_type=content_type)

        filename = Path(filename)

        if (base_path or file_path) and file_obj:
            raise ValueError(
                "Takes either `base_path` and `file_path` or a `file_obj` but not both."
            )
        if bool(base_path) != bool(file_path):
            raise ValueError("Both `base_path` and `file_path` are needed.")

        if base_path and file_path:
            base_path = Path(base_path)
            file_path = Path(file_path)
            abs_path = base_path / file_path.relative_to("/")

        if file_obj:
            base_path = Path(settings.TEMPFILE_DOWNLOAD_PATH)
            file_path = (
                Path(settings.TEMPFILE_DOWNLOAD_URL)
                / f"{filename.stem}-{str(uuid4())[:7]}{filename.suffix}"
            )

            abs_path = base_path / file_path.relative_to("/")

            if not abs_path.parent.exists():  # pragma: no cover
                abs_path.parent.mkdir(parents=True)

            abs_path.open("wb").write(file_obj.read())

        self["Content-Disposition"] = 'attachment; filename="%s"' % escape_uri_path(
            str(filename)
        )
        self["X-Accel-Redirect"] = "%s" % escape_uri_path(str(file_path))
        self["X-Sendfile"] = smart_bytes(str(abs_path))


class AuthorityView(ReadOnlyModelViewSet):
    """Only used in Kt. UR for 'Leitbehörde'."""

    swagger_schema = None
    serializer_class = serializers.AuthoritySerializer
    queryset = models.Authority.objects.all()


class WorkflowEntryView(ReadOnlyModelViewSet, InstanceQuerysetMixin):
    """Only used in Kt. UR."""

    swagger_schema = None
    serializer_class = serializers.WorkflowEntrySerializer
    queryset = models.WorkflowEntry.objects.all()
    filterset_class = filters.WorkflowEntryFilterSet
