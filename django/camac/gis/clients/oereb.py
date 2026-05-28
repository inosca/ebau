from concurrent.futures import ThreadPoolExecutor
from itertools import chain
from typing import Any, Literal

import requests
from django.conf import settings
from django.utils.translation import get_language, gettext as _, override

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
    max_concurrent_extracts = 16

    def process_data_source(
        self,
        config: dict[str, Any],
        _intermediate_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Process ÖREB data source.

        Supports a single EGRID or a comma-separated list. For each config item
        we first extract the raw value from every EGRID's extract, then
        aggregate across EGRIDs and write the final value to `data`:

        - Table questions (slug `table.column`): each EGRID contributes one row.
        - Concerned themes: If any EGRID is concerned, the result is `yes`; only
          if every EGRID is unconcerned is the result `no`.
        - Restriction collections (list-valued): ordered, deduplicated union.
        - Other flat questions: concatenated and deduplicated, or first
          non-empty wins when `use_first: true` is set on the config item.

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
                    "question": "gemeinde",
                    "cast": "municipality_bfs_to_dynamic_option",
                    "use_first": true
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
        egrids = self.params["egrid"].split(",")
        language = get_language()

        # We can allow a high amount of workers as `_get_extract` is very
        # CPU-light. We're only really I/O waiting on the response from the
        # OEREB server.
        with ThreadPoolExecutor(max_workers=self.max_concurrent_extracts) as executor:
            extracts = list(
                executor.map(
                    lambda egrid: self._get_extract(egrid, language),
                    egrids,
                )
            )

        data = {}

        for item in config.get("realestate_properties", []):
            self._write(
                data,
                item,
                [self._extract_realestate_property(raw, **item) for raw in extracts],
            )

        for item in config.get("restriction_on_landownership_collections", []):
            self._write(
                data,
                item,
                [self._extract_restriction_collection(raw, **item) for raw in extracts],
            )

        for item in config.get("concerned_themes", []):
            self._write(
                data,
                item,
                [self._extract_concerned_theme(raw, **item) for raw in extracts],
            )

        return data

    def _write(
        self,
        data: dict[str, Any],
        item: dict[str, Any],
        values: list[Any],
    ) -> None:
        """Write extracted per-EGRID values into the final data object.

        Table questions get one row per EGRID, all other questions questions are
        aggregated via `_aggregate` before being written.
        """

        question = item["question"]

        if "." in question:
            self._write_table_column(data, question, values)
        else:
            value = self._aggregate(values, item)
            self.set_question_value(data, question, value)

    def _write_table_column(
        self,
        data: dict[str, Any],
        question: str,
        values: list[Any],
    ) -> None:
        """Write a per-EGRID list of values as column values in a table."""

        table, column = question.split(".")
        rows = data.get(table, [])

        for i, value in enumerate(values):
            if i >= len(rows):
                rows.append({})

            rows[i][column] = value

        data[table] = rows

    def _aggregate(self, values: list[Any], item: dict[str, Any]) -> Any:
        """Combine per-EGRID values for a single flat question.

        - If `use_first` is given, we ignore all values after the first (e.g.
          for writing the municipality)
        - If values are booleans, we return the configured yes/no option
          strings. If **any** of the values is `True` it will be "yes".
        - Nested lists are flattened
        """
        first = values[0]

        if item.get("use_first"):
            return first

        if isinstance(first, bool):
            return item.get("yes", "ja") if any(values) else item.get("no", "nein")

        if isinstance(first, list):
            return list(chain(*values))

        return values

    def _extract_realestate_property(
        self,
        raw_data: dict[str, Any],
        property: str,
        cast: Literal["municipality_bfs_to_dynamic_option"] | None = None,
        **kwargs,
    ) -> Any:
        """Extract a `RealEstate` property.

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
                return {"key": str(pk)} if pk is not None else None
            case None:
                return value
            case _:  # pragma: no cover
                raise NotImplementedError()

    def _extract_restriction_collection(
        self,
        raw_data: dict[str, Any],
        theme: list[str] | str,
        **kwargs,
    ) -> list[str]:
        """Extract matched restriction texts.

        Collects every `LegendText.Text` in
        `RealEstate.RestrictionOnLandownership` whose `Code` matches `theme`.
        """

        theme = [theme] if isinstance(theme, str) else theme

        restrictions = get_dict_item(raw_data, "RealEstate.RestrictionOnLandownership")
        return [
            # `LegendText` is a `MultilingualText` array, but the OEREB service
            # filters it to the single entry matching the `LANG` query parameter
            # (or a default language if it's is omitted), so we can always use
            # the first item.
            get_dict_item(entry, "LegendText.0.Text", list_lookups=True)
            for entry in restrictions
            if get_dict_item(entry, "Theme.Code") in theme
        ]

    def _extract_concerned_theme(
        self,
        raw_data: dict[str, Any],
        theme: list[str] | str,
        **kwargs,
    ) -> bool:
        """Extract whether the EGRID is concerned by `theme`.

        Checks whether any entry in `ConcernedTheme` has a `Code` matching
        `theme`.
        """

        theme = [theme] if isinstance(theme, str) else theme

        entries = raw_data["ConcernedTheme"]
        return any(entry["Code"] in theme for entry in entries)

    def _get_extract(
        self,
        egrid: str,
        language: Literal["de", "fr", "it", "rm"],
    ) -> dict[str, Any]:
        """Fetch the OEREB JSON extract for `egrid` and return its payload."""

        # We need to explicitly override the language to make sure we use the
        # passed language for error translations. This is necessary because
        # threads don't inherit the active language.
        with override(language):
            response = requests.get(
                build_url(settings.OEREB_URL, "/extract/json/"),
                params={"EGRID": egrid, "LANG": language},
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
                            "use_first": {"type": "boolean"},
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
                            "use_first": {"type": "boolean"},
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
