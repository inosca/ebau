import requests
from django.conf import settings
from django.utils import timezone
from pyproj import CRS, Transformer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_json_api import views

from camac.instance.models import FormField
from camac.user.permissions import permission_aware

from . import filters, models, serializers


class PublicationEntryView(views.ModelViewSet):
    swagger_schema = None
    filterset_class = filters.PublicationEntryFilterSet
    serializer_class = serializers.PublicationEntrySerializer
    queryset = models.PublicationEntry.objects.all()
    prefetch_for_includes = {"instance": ["instance"]}

    @permission_aware
    def get_queryset(self):
        return models.PublicationEntry.objects.filter(
            publication_date__gte=timezone.now()
            - settings.APPLICATION.get("PUBLICATION_DURATION"),
            publication_date__lt=timezone.now(),
            is_published=True,
        )

    def get_queryset_for_municipality(self):
        return models.PublicationEntry.objects.filter(
            instance__group=self.request.group
        )

    def get_queryset_for_service(self):
        return models.PublicationEntry.objects.none()

    def get_queryset_for_canton(self):
        return models.PublicationEntry.objects.none()

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
        bauherrschaften_override = formFieldQuery.filter(
            name="bauherrschaft-override"
        ).first()
        bauherrschaften = bauherrschaften_override or bauherrschaften
        if bauherrschaften:
            payload["bauherrschaften"] = self._clean_persons(bauherrschaften.value)

        projektverfasser = formFieldQuery.filter(name="projektverfasser-planer").first()
        projektverfasser_override = formFieldQuery.filter(
            name="projektverfasser-planer-override"
        ).first()
        projektverfasser = projektverfasser_override or projektverfasser
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

        grundstuecknummern = []
        for parcel in formFieldQuery.get(name="parzellen").value:
            grundstuecknummern.append({"type": "KTN", "nummer": parcel["number"]})
        payload["grundstuecknummern"] = grundstuecknummern

        koordinaten = []
        transformer = Transformer.from_crs(
            "EPSG:4326",
            CRS.from_proj4(
                "+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs"
            ),
        )

        for coordSet in formFieldQuery.get(name="punkte").value:
            if not isinstance(coordSet, list):
                coordSet = [coordSet]
            for coord in coordSet:
                lat, lng = transformer.transform(coord["lat"], coord["lng"])
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


class PublicationEntryUserPermissionView(views.ModelViewSet):
    swagger_schema = None
    filterset_class = filters.PublicationEntryUserPermissionFilterSet
    serializer_class = serializers.PublicationEntryUserPermissionSerializer
    queryset = models.PublicationEntryUserPermission.objects.all()
    prefetch_for_includes = {"user": ["user"]}

    @permission_aware
    def get_queryset(self):
        return models.PublicationEntryUserPermission.objects.filter(
            user=self.request.user,
            publication_entry__publication_date__gte=timezone.now()
            - settings.APPLICATION.get("PUBLICATION_DURATION"),
            publication_entry__publication_date__lt=timezone.now(),
        )

    def get_queryset_for_municipality(self):
        return models.PublicationEntryUserPermission.objects.filter(
            publication_entry__instance__group=self.request.group
        )

    def get_queryset_for_service(self):
        return models.PublicationEntryUserPermission.objects.none()

    @permission_aware
    def has_create_permission(self):
        return True

    def has_create_permission_for_municipality(self):
        return False

    def has_create_permission_for_service(self):
        return False

    @permission_aware
    def has_update_permission(self):
        return False

    def has_update_permission_for_municipality(self):
        return True

    def has_destroy_permission(self):
        return False
