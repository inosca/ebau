from typing import Literal

import requests
from django.conf import settings
from django.utils.translation import get_language, gettext as _

from camac.gis.clients.base import GISBaseClient
from camac.user.models import Service
from camac.utils import build_url, get_dict_item


class OerebGisClient(GISBaseClient):
    """GIS client for the ÖREB service.

    This client is canton agnostic and should work with every Swiss canton using
    the official federal ÖREB service. The only thing that may vary is the host
    URL and the configuration that lives in our `GisDataSource` models.

    The schema that is expected can be found here (specifically in section 3.2):
    https://www.cadastre-manual.admin.ch/de/oereb-webservice-aufruf-eines-auszugs

    The corresponding JSON schema can be found here:
    https://schemas.geo.admin.ch/V_D/OeREB/2.0/extract.json
    """

    required_params = ["egrid"]

    def process_data_source(self, config: dict, _intermediate_data: dict) -> dict:
        """Process ÖREB data source.

        Example config:
        ```json
        {
            "realestate_properties": [
                {
                    "property": "Number",
                    "question": "parzellen.parzellennummer"
                },
                {
                    "property": "MunicipalityCode",
                    "question": "parzellen.gemeinde",
                    "cast": "municipality_bfs_to_dynamic_option"
                }
            ],
            "restriction_on_landownership_collections": [
                {
                    "theme": "ch.Nutzungsplanung",
                    "question": "zonenplan"
                },
                {
                    "theme": [
                        "ch.SG.KantonaleSondernutzungsplaene",
                        "ch.SG.KomSondernutzungsplaene"
                    ],
                    "question": "sondernutzungsplan"
                }
            ],
            "concerned_themes": [
                {
                    "theme": [
                        "ch.BelasteteStandorte",
                        "ch.BelasteteStandorteMilitaer",
                        "ch.BelasteteStandorteZivileFlugplaetze",
                        "ch.BelasteteStandorteOeffentlicherVerkehr"
                    ],
                    "question": "kbs"
                }
            ]
        }
        ```
        """

        raw_data = self._get_extract(self.params["egrid"])
        data = {}

        for item in config.get("realestate_properties", []):
            self._handle_realestate_property(raw_data, data, **item)
        for item in config.get("restriction_on_landownership_collections", []):
            self._handle_restriction_collection(raw_data, data, **item)
        for item in config.get("concerned_themes", []):
            self._handle_concerned_theme(raw_data, data, **item)

        return data

    def _handle_realestate_property(
        self,
        raw_data: dict,
        data: dict,
        question: str,
        property: str,
        cast: Literal["municipality_bfs_to_dynamic_option"] | None = None,
    ):
        """Assign a `RealEstate` property to a question.

        Reads `RealEstate.<property>` and optionally casts the raw value to the
        format Caluma expects via `cast`.
        """

        value = raw_data["RealEstate"][property]

        match cast:
            case "municipality_bfs_to_dynamic_option":
                pk = (
                    Service.objects.filter(external_identifier=value)
                    .values_list("pk", flat=True)
                    .first()
                )
                value = {"key": str(pk)} if pk is not None else None
            case None:
                pass
            case _:  # pragma: no cover
                raise NotImplementedError()

        self.set_question_value(data, question, value)

    def _handle_restriction_collection(
        self,
        raw_data: dict,
        data: dict,
        question: str,
        theme: list[str] | str,
    ):
        """Assign matched restriction texts to a question.

        Collects every `LegendText.Text` in
        `RealEstate.RestrictionOnLandownership` whose `Code` matches `theme`.
        """

        theme = [theme] if isinstance(theme, str) else theme

        restrictions = get_dict_item(raw_data, "RealEstate.RestrictionOnLandownership")
        values = [
            # `LegendText` is a `MultilingualText` array, but the OEREB service
            # filters it to the single entry matching the `LANG` query parameter
            # (or a default language if it's is omitted), so we can always use
            # the first item.
            get_dict_item(entry, "LegendText.0.Text", list_lookups=True)
            for entry in restrictions
            if get_dict_item(entry, "Theme.Code") in theme
        ]

        self.set_question_value(data, question, values)

    def _handle_concerned_theme(
        self,
        raw_data: dict,
        data: dict,
        question: str,
        theme: list[str] | str,
        yes: str = "ja",
        no: str = "nein",
    ):
        """Assign `yes`/`no` based on theme presence to a question.

        Checks whether any entry in `ConcernedTheme` has a `Code` matching
        `theme`.
        """

        theme = [theme] if isinstance(theme, str) else theme

        entries = raw_data["ConcernedTheme"]
        is_concerned = any(entry["Code"] in theme for entry in entries)
        value = yes if is_concerned else no

        self.set_question_value(data, question, value)

    def _get_extract(self, egrid: str) -> dict:
        """Fetch the OEREB JSON extract for `egrid` and return its payload."""

        response = requests.get(
            build_url(settings.OEREB_URL, "/extract/json/"),
            params={"EGRID": egrid, "LANG": get_language()},
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise RuntimeError(
                _("Error %(code)s while fetching data from the OEREB API")
                % {"code": response.status_code}
            ) from exc

        if response.status_code == 204:
            raise RuntimeError(
                _(
                    "No OEREB data for EGRID %(egrid)s. Plot may be outside of the canton."
                )
                % {"egrid": egrid}
            )

        return get_dict_item(response.json(), "GetExtractByIdResponse.extract")

    class Meta:
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "additionalProperties": False,
            "$defs": {
                "question": {
                    "type": "string",
                    "pattern": r"^[-a-zA-Z0-9_]+(\.[-a-zA-Z0-9_]+)?$",
                },
                "themeCodes": {
                    "oneOf": [
                        {"type": "string"},
                        {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 1,
                        },
                    ],
                },
            },
            "properties": {
                "realestate_properties": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["property", "question"],
                        "properties": {
                            "property": {"type": "string"},
                            "question": {"$ref": "#/$defs/question"},
                            "cast": {
                                "type": "string",
                                "enum": ["municipality_bfs_to_dynamic_option"],
                            },
                        },
                    },
                },
                "restriction_on_landownership_collections": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["theme", "question"],
                        "properties": {
                            "theme": {"$ref": "#/$defs/themeCodes"},
                            "question": {"$ref": "#/$defs/question"},
                        },
                    },
                },
                "concerned_themes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["theme", "question"],
                        "properties": {
                            "theme": {"$ref": "#/$defs/themeCodes"},
                            "question": {"$ref": "#/$defs/question"},
                            "yes": {"type": "string"},
                            "no": {"type": "string"},
                        },
                    },
                },
            },
        }
