import requests
from django.conf import settings
from pyproj import CRS, Transformer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from camac.instance.models import FormField
from camac.user.permissions import permission_aware

from . import filters, models, serializers


class PublicationEntryView(viewsets.ModelViewSet):
    swagger_schema = None
    filterset_class = filters.PublicationEntryFilterSet
    serializer_class = serializers.PublicationEntrySerializer
    queryset = models.PublicationEntry.objects.all()

    @permission_aware
    def get_queryset(self):
        return models.PublicationEntry.objects.none()

    def get_queryset_for_canton(self):
        return models.PublicationEntry.objects.none()

    def get_queryset_for_service(self):
        return models.PublicationEntry.objects.none()

    def get_queryset_for_municipality(self):
        return models.PublicationEntry.objects.filter(
            instance__group=self.request.group
        )

    @permission_aware
    def has_create_permission(self):
        return False

    def has_create_permission_for_municipality(self):
        return True

    def has_create_permission_for_service(self):
        return False

    def has_create_permission_for_canton(self):
        return False

    @permission_aware
    def has_update_permission(self):
        return False

    def has_update_permission_for_municipality(self):
        return True

    def has_update_permission_for_service(self):
        return False

    def has_update_permission_for_canton(self):
        return False

    def has_destroy_permission(self):
        return False

    def _clean_persons(self, persons, type=""):
        for person in persons:
            if type == "grundeingenuemer":
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

            person.pop("email", None)
            person.pop("tel", None)

        return persons

    @action(methods=["post"], detail=True)  # noqa: C901
    def publish(self, request, pk=None):
        try:
            payload = {}
            publication = self.get_object()
            formFieldQuery = FormField.objects.filter(instance=publication.instance)

            payload["bfs_nr"] = int(
                publication.instance.location.communal_federal_number
            )

            payload["publikation_datum"] = publication.publication_date.strftime(
                "%d.%m.%Y"
            )

            bauzone = formFieldQuery.filter(name="lage").first()
            if bauzone:
                bauzone = bauzone.value
                payload["bauzone"] = bauzone if bauzone != "beides" else "ausserhalb"

            bauherrschaften = formFieldQuery.filter(name="bauherrschaft").first()
            if bauherrschaften:
                payload["bauherrschaften"] = self._clean_persons(bauherrschaften.value)

            projektverfasser = formFieldQuery.filter(
                name="projektverfasser-planer"
            ).first()
            if projektverfasser:
                payload["projektverfasser"] = self._clean_persons(
                    projektverfasser.value
                )

            grundeigentuemer = formFieldQuery.filter(
                name="grundeigentumerschaft"
            ).first()
            if grundeigentuemer:
                payload["grundeigentuemer"] = self._clean_persons(
                    grundeigentuemer.value, "grundeingenuemer"
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
            for coord in formFieldQuery.get(name="punkte").value:
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
                settings.PUBLICAIION_API_URL,
                json=payload,
                auth=(settings.PUBLICATION_API_USER, settings.PUBLICATION_API_PASSWORD),
            )

            response.raise_for_status()
        # This is to catch any exception that might result from the Amtsblatt api
        except requests.exceptions.RequestException as e:  # pragma: no cover
            return Response(str(e), 400)
        else:
            return Response([], 204)
