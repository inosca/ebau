import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Dict, List, Optional, Tuple, Type, TypeVar, Union

import dateparser
from codetiming import Timer
from django.conf import settings
from django.utils.timezone import make_aware
from jsonpath_ng.ext import parse

from camac.dossier_import.config.kt_ag_sap_migration.dossier_import.dossier_classes import (
    Authorization,
    Building,
    CantonComment,
    CantonStatusHistoryEntry,
    Comment,
    Deadline,
    Decision,
    DocumentStatus,
    DossierTypes,
    Fee,
    KtAargauDossier,
    KtAgSuspension,
    ProceduralStatusEntry,
    Residence,
    ValueHolder,
    Workflow,
    WorkflowDoc,
    WorkflowRecipient,
)
from camac.dossier_import.config.kt_ag_sap_migration.sap.sap_access import SAPAccess
from camac.dossier_import.dossier_classes import (
    Coordinates,
    Person,
    PlotData,
)
from camac.dossier_import.loaders import DossierLoader
from camac.dossier_import.models import DossierImport

log = logging.getLogger(__name__)

UNMAPPED = "__UNMAPPED__"

T = TypeVar("T")


@dataclass
class Transform:
    """Recursive data structure that describes the transformation from plain JSON to domain objects."""

    data_path: str
    result_type: Type
    mappings: Dict[str, Union[str, "Transform"]]
    converter: Optional[Dict[str, Callable]] = field(default_factory=dict)


def noop(x):
    return x


def true_if_one(x):
    return x == "1"


def bool_from_X(x):
    return x == "X"


def true_if_one_or_X(x):
    return true_if_one(x) or bool_from_X(x)


def sap_date_else_none(x: Optional[str]) -> Optional[str]:
    if not is_real_sap_date(x):
        return None
    return x


def datetime_from_long_number(x: Union[str, float, int]):
    """Convert a float to datetime with timezone CET.

    The float is expected to be a timestamp in the format:
    20240214090249.07 or
    20250617150613
    to a datetime object.
    """

    if not x:
        return None

    # ignore digits after comma and convert to string
    timestamp_str = str(int(x))

    try:
        d = dateparser.parse(timestamp_str, date_formats=["%Y%m%d%H%M%S"])
        if not d:  # pragma: no cover
            raise ValueError(f"Could not parse date {x} (rounded: {timestamp_str})")
        return make_aware(d)
    except ValueError:  # pragma: no cover
        return None


def datetime_from_yyyymmdd(value: Optional[str]) -> Optional[datetime]:
    if not is_real_sap_date(value):  # pragma: no cover
        return None

    try:
        return make_aware(datetime.strptime(value, "%Y%m%d"))
    except ValueError:  # pragma: no cover
        return None


def date_from_yyyymmdd(value: Optional[str]) -> Optional[datetime]:
    if not is_real_sap_date(value):  # pragma: no cover
        return None

    try:
        datetime_value = make_aware(datetime.strptime(value, "%Y%m%d"))
        return datetime_value.date() if datetime_value else None
    except ValueError:  # pragma: no cover
        return None


def is_real_sap_date(x: Optional[str]) -> Optional[str]:
    return x and x != "00000000"


def str_or_none(x: any) -> Optional[str]:
    return str(x) if x else None


def int_or_none(x: any) -> Optional[str]:
    return int(x) if x else None


def float_or_none(x: any) -> Optional[str]:
    return float(x) if x else None


def docid_or_none(x: str) -> Optional[str]:
    return x if x and x != "0000000000000000000000000" else None


# Documentation: https://github.com/h2non/jsonpath-ng

PERSON_MAPPING_MAPPINGS = {
    "first_name": "VNAM",
    "last_name": "NAME",
    "company": "FIRMA",
    "street": "STRASSE",
    "street_number": "STRASNR",
    "zip": "PLZ",
    "town": "ORT",
    "phone": "TELMOBI,TELFEST",
    "email": "EMAIL",
    "is_juristic_person": "FIRMA",
    # KGUID (Kontakt GUID), GVGUID (gesetzl. Vertreter GUID)",
}

PERSON_CONVERTERS = {"zip": int_or_none, "is_juristic_person": bool}
MAPPING = Transform(
    data_path="$",
    result_type=KtAargauDossier,
    mappings={
        "id": "GESUCH_ID",
        "dossier_file_path": "json_path",
        "proposal": "BTITEL",
        "description": "BSGUID_TXT",
        "cantonal_id": "BVUAFBNR",
        "cantonal_status": "KANTONS_STATUS",
        "municipal_id": "GEMEINDE_BG",
        "municipal_status": "GEMEINDE_STATUS",
        "creation_date": "CRDAT",
        "submit_date": "EINDAT",
        "responsible_municipality": "CITY_ID",
        "other_municipalities": Transform(
            "STANDORTE[?(@.CITY != '{CITY}')]", ValueHolder, {"value": "CITY_ID"}
        ),
        "city": "CITY",
        "zip": "STANDORTE[?(@.CITY == '{CITY}')].POSTAL_CODE",
        "street": "STANDORTE[?(@.CITY == '{CITY}')].STRASSE",
        "street_number": "STANDORTE[?(@.CITY == '{CITY}')].STRASNR",
        "submission_reason": "ERFGRND",
        "application_type": "VERFTYP",
        "dossier_types": Transform(
            "$",
            DossierTypes,
            {
                "baugesuch": "BAUANL_KNZ",
                "reklamegesuch": "REKLAM_KNZ",
                "abbruchgesuch": "ABRUCH_KNZ",
                "umnutzung": "UMNUTZ_KNZ",
                "anfrage": "ANFRAG_KNZ",
                "vorentscheid": "VORENT_KNZ",
                "rodung": "RODUNG_KNZ",
                "uvp": "UMWELT_KNZ",
                "pgv": "PLANGN_KNZ",
            },
            {
                "baugesuch": bool_from_X,
                "reklamegesuch": bool_from_X,
                "abbruchgesuch": bool_from_X,
                "umnutzung": bool_from_X,
                "anfrage": bool_from_X,
                "vorentscheid": bool_from_X,
                "rodung": bool_from_X,
                "uvp": bool_from_X,
                "pgv": bool_from_X,
            },
        ),
        "profiling": "PROFIL_KNZ",
        "profiling_date": "PROFIL_DAT",
        "profile_approval_date": "PROFIL_KTR",
        "profiling_reasoning": "PRGUID_TXT",
        # Zweckbestimmung
        "residential_use": "WHNTZ_KNZ",
        "residence": Transform(
            "WOHNUTZ[*]",
            Residence,
            {
                "number_of_residential_units": "ANZ_WHG",
                "number_of_rooms": "ANZ_ZIM",
                "of_which_second_homes": "ANZ_ZWHG",
            },
            {
                "number_of_residential_units": int_or_none,
                "number_of_rooms": float_or_none,
                "of_which_second_homes": int_or_none,
            },
        ),
        "commercial_and_industrial_use": "GINTZ_KNZ",
        "commercial_and_industrial_type_of_use": "GINTZ_ART",
        "commercial_and_industrial_sector": "GIBRANCHE",
        "agricultural_use": "LWNTZ_KNZ",
        "owned_land_total_ha": "LWNTZ_EL",
        "leased_land_total_ha": "LWNTZ_PL",
        "existing_livestock": "LWNTZ_TBB",
        "new_livestock": "LWNTZ_TBN",
        "other_buildings": "ABNTZ_KNZ",
        "other_buildings_designation": "ABNTZ_BEZ",
        "other_buildings_type_of_use": "ABNTZ_ART",
        # Gebäudehülle
        "building_envelope_roof_covering_material": "DBEL_MAT",
        "building_envelope_roof_covering_color": "DBEL_COL",
        "building_envelope_exterior_wall_material": "AWND_BART",
        "building_envelope_exterior_wall_color": "AWND_COL",
        # Gebäudeheizung und Energie
        "building_heating_none": "GHNO_KNZ",
        "building_heating_existing": "GHIS_KNZ",
        "building_heating_new": "GHNW_KNZ",
        "building_heating_new_kw": "GHNW_KW",
        "building_heating_replacement": "GHES_KNZ",
        "building_heating_replacement_kw": "GHES_KW",
        "building_heating_unknown": "GHUK_KNZ",
        "building_heating_unknown_explanation": "GHGUID_TXT",
        "building_heating_type_oil": "BA_OEL_KNZ",
        "building_heating_type_oil_new": "BA_OEN_KNZ",
        "building_heating_type_gas": "BA_GAS",
        "building_heating_type_wood": "BA_HLZ",
        "building_heating_type_electric": "BA_ELK",
        "building_heating_type_district": "BA_FRN",
        "building_heating_type_heatpump": "BA_WAP",
        "building_heating_type_heatpump_ground_water": "BA_WAB",
        "building_heating_type_heatpump_air": "BA_LUF",
        "building_heating_type_other": "BA_OTH",
        "building_heating_type_other_text": "BA_OTB",
        # Parzellen
        "plot_data": Transform(
            "PARZELLEN[*]",
            PlotData,
            {"number": "PARZNR", "municipality": "CITY_ID", "egrid": UNMAPPED},
        ),
        "coordinates": Transform(
            "STANDORTE[?(@.CITY == '{CITY}')]",
            Coordinates,
            {
                "n": "KOORDB",
                "e": "KOORDL",
            },
            {
                "n": float,
                "e": float,
            },
        ),
        "building": Transform(
            "STANDORTE[*]",
            Building,
            {
                "egid": "EGID",
                "insurance_number": "ASSEKNR",
            },
        ),
        "applicant": Transform(
            # BH - Bauherrschaft
            "KONTAKTE[?(@.PTROL == 'BH')]",
            Person,
            PERSON_MAPPING_MAPPINGS,
            PERSON_CONVERTERS,
        ),
        "landowner": Transform(
            # GE - Grundeigentümer
            "KONTAKTE[?(@.PTROL == 'GE')]",
            Person,
            PERSON_MAPPING_MAPPINGS,
            PERSON_CONVERTERS,
        ),
        "project_author": Transform(
            # PV - Projektverfasser
            "KONTAKTE[?(@.PTROL == 'PV')]",
            Person,
            PERSON_MAPPING_MAPPINGS,
            PERSON_CONVERTERS,
        ),
        "legal_representative": Transform(
            # GV - Gesetzl. Vertreter
            "KONTAKTE[?(@.PTROL == 'GV')]",
            Person,
            PERSON_MAPPING_MAPPINGS,
            PERSON_CONVERTERS,
        ),
        "invoice_recipient": Transform(
            # RE - Rechnungsadresse
            "KONTAKTE[?(@.PTROL == 'RE')]",
            Person,
            PERSON_MAPPING_MAPPINGS,
            PERSON_CONVERTERS,
        ),
        # Parkplätze
        "parking_affected": "PARK_KNZ",
        "existing_parking_spaces": "ANZ_OPARK",
        "existing_mandatory_spaces": "ANZ_OPARK_P",
        "existing_non_mandatory_spaces": "ANZ_OPARK_NP",
        "new_parking_spaces": "ANZ_NPARK",
        "new_mandatory_spaces": "ANZ_NPARK_P",
        "new_non_mandatory_spaces": "ANZ_NPARK_NP",
        # Bauzonen
        "zoning_area": "BAU_ZON",
        "usage_zone": "NTZ_ZON",
        "overlapping_zone": "UBL_ZON",
        "special_use_plan": "SND_PLN",
        # Dichteziffern
        "ratio_utilization_zone_regulation": "ASN_ZIF_ZOD",
        "ratio_utilization_building_project": "ASN_ZIF_BPJ",
        "ratio_volume_zone_regulation": "BMS_ZIF_ZOD",
        "ratio_volume_building_project": "BMS_ZIF_BPJ",
        "ratio_green_area_zone_regulation": "GSF_ZIF_ZOD",
        "ratio_green_area_building_project": "GFL_ZIF_BPJ",
        "ratio_floor_area_zone_regulation": "GFL_ZIF_ZOD",
        "ratio_floor_area_building_project": "GSF_ZIF_BPJ",
        "ratio_coverage_zone_regulation": "UEB_ZIF_ZOD",
        "ratio_coverage_building_project": "UEB_ZIF_BPJ",
        # Bauzonen - weitere Angaben
        "zone_water_protection_area_au": "GWS_AU_KNZ",
        "zone_water_protection_area_bc": "GWS_UB_KNZ",
        "zone_spring_capture_area": "GWS_QB_KNZ",
        "zone_flood_hazard": "HWG_KNZ",
        "zone_seismic_compliance": "EKE_ERF",
        "zone_sensitivity_level": "EMP_STF",
        # Kanalisation & Entwässerung
        "sewage_connection_property": "KA_LGS_KNZ",
        "sewage_connection_property_presence": "KA_LGN_KNZ",
        "sewage_connection_construction": "KA_BAU_KNZ",
        "sewage_connection_construction_presence": "KA_BAN_KNZ",
        "stormwater_infiltration": "DS_VSK_KNZ",
        "stormwater_infiltration_new": "DS_VSN_KNZ",
        "stormwater_public_water": "DS_OGW_KNZ",
        "stormwater_public_water_new": "DS_OGN_KNZ",
        "stormwater_sewage": "DS_KNL_KNZ",
        "stormwater_sewage_new": "DS_KNN_KNZ",
        "stormwater_self_use": "DS_EIG_KNZ",
        # Umweltrechtliche Angaben
        "environmental_geothermal_probes_planned": "ERDSND_KNZ",
        "environmental_special_drilling_or_pump_tests": "SDBOHR_KNZ",
        "environmental_solar_installation_planned": "SOLAR_KNZ",
        "environmental_contaminated_site_affected": "ALTLAST_KNZ",
        "environmental_groundwater_intervention_required": "GWABSNK_KNZ",
        "environmental_soil_intervention_planned": "BODEIN_KNZ",
        "environmental_noise_protection_required": "LSMERF_KNZ",
        "environmental_material_extraction_planned": "MATABB_KNZ",
        "environmental_sewer_construction_or_change": "KANAL_KNZ",
        "environmental_energy_certificate_required": "ENERGIE_KNZ",
        # Angaben zur Sicherheit
        "safety_fire_protection_canton_required": "BS_KANT_KNZ",
        "safety_fire_protection_heating_required": "BSFKANT_KNZ",
        "safety_fire_protection_communal_required": "BS_KOMM_KNZ",
        "safety_employees_affected": "BETRIEB_KNZ",
        "safety_incident_zone_or_infrastructure": "STOER_KNZ",
        "safety_flood_prone_area": "HWGEFHR_KNZ",
        "safety_shelter_obligation": "SRBAUPF_KNZ",
        # Kantonsstrasse, Wald
        "street_highway_affected": "KANTSTR_KNZ",
        "street_min_distance_undershot": "BAULINE_KNZ",
        "street_min_distance_reasoning": "BLGUID_TXT",
        "street_new_or_intensified_access": "ERSCHLS_KNZ",
        "street_advertising_planned": "REKLAME_KNZ",
        "forest_min_distance_undershot": "MAWALD_KNZ",
        "forest_min_distance_reasoning": "MAGUID_TXT",
        "forest_project_in_forest": "BVWALD_KNZ",
        # Bauen ausserhalb der Bauzone
        "outside_building_zone_agricultural_use": "LWBETR_KNZ",
        "outside_building_zone_legal_nonconforming_use": "BSTAND_KNZ",
        "outside_building_zone_other_project": "BVBZON_KNZ",
        "outside_building_zone_terrain_modification": "TVBZON_KNZ",
        # Weitere Angaben, Gewässer, ...
        "special_public_water_body_affected": "OEFFGW_KNZ",
        "special_water_body_name": "OEFFGW_NAM",
        "special_water_distance_undershot": "OEFFGW_ABS",
        "special_water_distance_reasoning": "GWGUID_TXT",
        "special_water_intervention_planned": "OEFFGW_EIN",
        "special_monument_or_visibility_affected": "DENKMAL_KNZ",
        "special_airspace_obstacle_planned": "LFHIND_KNZ",
        # Baukosten
        "cost_building_without_land": "BKOLND",
        "cost_environmental_works": "BKUMGB",
        "cost_total": "BKTOTAL",
        # Weitere Angaben - Bemerkungen
        "notes_comments": "BKGUID_TXT",
        # Verfahrensstand
        "procedural_status": Transform(
            "VERFSTAND[*]",
            ProceduralStatusEntry,
            {
                "action": "ACTION",
                "step": "STEP",
                "timestamp": "TSTAMPL",
                "username": "WHOTXT",
                "comment": "KOMMENTAR",
            },
            {
                "timestamp": datetime_from_long_number,
            },
        ),
        "comments": Transform(
            "KOMMENTARE[*]",
            Comment,
            {
                "userid": "SACHB",
                "username": "SACHB_FIRSTNAME + ' ' + $.SACHB_LASTNAME",
                "text": "KOMMENTAR",
                "timestamp": "CREATED_AT",
            },
            {
                "timestamp": datetime_from_long_number,
            },
        ),
        "workflows": Transform(
            "DWFLOW[*]",
            Workflow,
            {
                "workflow_type": "DWTYP",
                "id": "DWGUID",
                "date": "DWBEG",
                "active": "ACTIVE",
                "status": "DWSTAT",
            },
            {
                "date": datetime_from_yyyymmdd,
                "active": bool_from_X,
            },
        ),
        "workflow_docs": Transform(
            "DWFLOW_DOC[*]",
            WorkflowDoc,
            {
                "workflow_id": "DWGUID",
                "dms_id": "DMS_ID",
                "dms_version": "DMS_VERS",
                "doc_type": "DOCTYPE",
                "date": "DDATE + $.DTIME",
                "remark": "BEMERKUNG",
                "recipient_id": "EMPFGUID",
            },
            {"date": datetime_from_long_number},
        ),
        "workflow_recipients": Transform(
            "DWFLOW_REC[*]",
            WorkflowRecipient,
            {
                "id": "EMPFGUID",
                "workflow_id": "DWGUID",
                "user_id": "EMPFID",
                "user_name": "EMPFNAM",
                "user_email": "EMPFADR",
                "reason": "REASON",
                "active": "ACTIVE",
                "remark": "BEMERKUNG",
                "manually_added": "MAN_KNZ",
                "date": "DDATE+$.DTIME",
                "status": "RCSTAT",
                "request": "ANTRAG",
            },
            {
                "active": bool_from_X,
                "manually_added": bool_from_X,
                "date": datetime_from_long_number,
            },
        ),
        "decisions": Transform(
            "ENTSCHEID[*]",
            Decision,
            {
                "type": "ART_ID,ART_TEXT",
                "decision_date": "VERFUGUNGSDAT",
                "legal_binding_date": "RECHTSKRAFTDAT",
                "legal_remedy_taken_date": "RECHTMITTELDAT",
                "remark": "BEMERKUNG",
            },
            {
                "decision_date": datetime_from_yyyymmdd,
                "legal_binding_date": datetime_from_yyyymmdd,
                "legal_remedy_taken_date": datetime_from_yyyymmdd,
            },
        ),
        "deadlines": Transform(
            "DATES[*]",
            Deadline,
            {
                "type": "TRMTYP",
                "date_from": "DATVON",
                "date_to": "DATBIS",
                "notice": "NOTICE",
                "reason": "GRUND_TXT",
                "completed": "ABGS",
            },
            {
                "date_from": datetime_from_yyyymmdd,
                "date_to": datetime_from_yyyymmdd,
                "completed": bool_from_X,
            },
        ),
        "authorizations": Transform(
            "BERECHT[*]",
            Authorization,
            {
                "userid": "PARTNER",
                "permission": "BROL",
            },
        ),
        "canton_entry_date": "KANTON_EINGANG",
        "canton_internal_deadline": "KANTON_BEARBEITUNGSFRIST",
        "canton_group": "KANTON_GRUPPE",
        "canton_group_name": "KANTON_GRUPPE2",
        "canton_assignee": "KANTON_SACHBEARBEITER",
        "canton_provisional_closure_date": "KANTON_VORL_ABSCHLUSS",
        "canton_closure_code": "KANTON_ABSCHLUSSCODE",
        "canton_processing_duration_days": "KANTON_DAUER",
        "canton_lwag_number": "KANTON_LWAG_NR",
        "canton_status_history": Transform(
            "KANTON_STATUSVERLAUF[*]",
            CantonStatusHistoryEntry,
            {
                "source": "SOURCE",
                "timestamp": "TSTAMPL",
                "who_text": "WHOTXT",
                "comment": "KOMMENTAR",
                "document_id": "DOC_ID",
                "document_version": "DOC_VERSION",
                "action_text": "ACTION_TXT",
                "step_text": "STEP_TXT",
            },
            converter={
                "document_id": docid_or_none,
            },
        ),
        "canton_comments": Transform(
            "KANTON_KOMMENTARE[*]",
            CantonComment,
            {
                "timestamp": "TIMESTAMP",
                "user_id": "USER_ID",
                "text": "TEXT",
            },
        ),
        "canton_application_codes": Transform(
            "KANTON_GESUCHSCODES[*]",
            ValueHolder,
            {"value": "BAUG_ID + ' / ' + $.DESCRIPTION"},
        ),
        "canton_usage_zones": Transform(
            "KANTON_NUTZUNGSZONEN[*]",
            ValueHolder,
            {"value": "DESCRIPTION"},
        ),
        "canton_protection_zones": Transform(
            "KANTON_SCHUTZZONEN[*]",
            ValueHolder,
            {"value": "DESCRIPTION"},
        ),
        "canton_roads": Transform(
            "KANTON_STRASSEN[*]",
            ValueHolder,
            {"value": "DESCRIPTION + ' (' + $.ROAD_NUMBER + ')'"},
        ),
        "canton_railways": Transform(
            "KANTON_BAHNEN[*]",
            ValueHolder,
            {"value": "DESCRIPTION"},
        ),
        "canton_waters": Transform(
            "KANTON_GEWAESSER[*]",
            ValueHolder,
            {"value": "RIVER_ID + ' - ' + $.RIVER_NAME"},
        ),
        "canton_cantonal_road_affected": "KANTON_KANTSTR_KNZ",
        "canton_water_affected": "KANTON_OEFFGW_KNZ",
        "canton_forest_distance": "KANTON_MAWALD_KNZ",
        "canton_special_case_dev": "KANTON_SNDF_ENTW_KNZ",
        "canton_groundwater_lowering_planned": "KANTON_GWABSNK_KNZ",
        "canton_awa": "KANTON_AWA_KNZ",
        "canton_construction_project_in_forest": "KANTON_BVWALD_KNZ",
        "canton_flood_hazard": "KANTON_HWG_KNZ",
        "canton_monument_protection": "KANTON_DENKMAL_KNZ",
        "canton_hiking_trails": "KANTON_WANDERWEGE_KNZ",
        "canton_townscape_protection": "KANTON_ORTSBILD",
        "canton_major_accident_ordinance_affected": "KANTON_STOER_KNZ",
        "canton_archaeology": "KANTON_ARCH_KNZ",
        "canton_traffic": "KANTON_VERKEHR_KNZ",
        "canton_noise_protection": "KANTON_LSMERF_KNZ",
        "canton_material_extraction": "KANTON_MATABB_KNZ",
        "canton_agv": "KANTON_AGV_KNZ",
        "canton_cycle_paths": "KANTON_RADWEGE_KNZ",
        "canton_subsequent_application": "KANTON_NACHTR_GESUCH_KNZ",
        "canton_sewerage": "KANTON_KANALISATION",
        "canton_area_consumption": "KANTON_FLACHENVERBRAUCH",
        "canton_koko_date": "KANTON_KOKO_DATUM",
        "canton_koko_status": "KANTON_KOKO_STATUS",
        "canton_municipal_decision": "KANTON_BESCHLUSS_GEMEINDE",
        "canton_decision_type": "KANTON_BESCHLUSS_ART",
        "canton_delay_caused_by": "KANTON_VERZOGERUNG",
        "canton_justification": "KANTON_BEGRUNDUNG",
        "canton_fees": Transform(
            "KANTON_GEBUEHREN[*]",
            Fee,
            {
                "cost_type": "COST_TYPE",
                "description": "DESCRIPTION",
                "calculation_scheme": "CALCULATION_SCHEME",
                "calc_scheme_position": "CALC_SCHEME_POSITION",
                "request_task_id": "REQUEST_TASK_ID",
                "unit_price": "UNIT_PRICE",
                "amount": "AMOUNT",
                "msehi": "MSEHI",
                "take": "TAKE",
                "show_in_gv": "SHOW_IN_GV",
                "comment_fs": "COMMENT_FS",
                "comment_afb": "COMMENT_AFB",
            },
            converter={
                "take": bool_from_X,
                "show_in_gv": bool_from_X,
            },
        ),
        "canton_suspensions": Transform(
            "KANTON_SISTIERUNGEN[*]",
            KtAgSuspension,
            {
                "start_date": "DATVON",
                "resume_date": "RESUME_DATE",
                "reason": "REASON",
                "note": "NOTE",
                "prev_status": "PREV_STATUS",
                "creation_date": "CREATED_ON",
            },
            converter={
                "start_date": sap_date_else_none,
                "end_date": sap_date_else_none,
                "creation_date": sap_date_else_none,
                "resume_date": sap_date_else_none,
            },
        ),
        "document_statuses": Transform(
            "DOK_STATUS[*]",
            DocumentStatus,
            {
                "dms_id": "DMS_ID",
                "dms_version": "DMS_VERS",
                "status": "STATUS_TEXT",
            },
        ),
    },
    converter={
        "submit_date": sap_date_else_none,
        "profiling": true_if_one,
        "profiling_date": sap_date_else_none,
        "profile_approval_date": sap_date_else_none,
        "residential_use": bool_from_X,
        "commercial_and_industrial_use": bool_from_X,
        "agricultural_use": bool_from_X,
        "other_buildings": bool_from_X,
        "owned_land_total_ha": str_or_none,
        "leased_land_total_ha": str_or_none,
        "existing_livestock": str_or_none,
        "new_livestock": str_or_none,
        "parking_affected": bool_from_X,
        # Gebäudeheizung und Energie
        "building_heating_none": bool_from_X,
        "building_heating_existing": bool_from_X,
        "building_heating_new": bool_from_X,
        "building_heating_replacement": bool_from_X,
        "building_heating_unknown": bool_from_X,
        "building_heating_type_oil": bool_from_X,
        "building_heating_type_oil_new": true_if_one,
        "building_heating_type_gas": bool_from_X,
        "building_heating_type_wood": bool_from_X,
        "building_heating_type_electric": bool_from_X,
        "building_heating_type_district": bool_from_X,
        "building_heating_type_heatpump": bool_from_X,
        "building_heating_type_heatpump_ground_water": bool_from_X,
        "building_heating_type_heatpump_air": bool_from_X,
        "building_heating_type_other": bool_from_X,
        # Bauzonen - weitere Angaben
        "zone_water_protection_area_au": bool_from_X,
        "zone_water_protection_area_bc": bool_from_X,
        "zone_spring_capture_area": bool_from_X,
        "zone_flood_hazard": true_if_one_or_X,
        # Kanalisation und Entwässerung
        "sewage_connection_property": bool_from_X,
        "sewage_connection_construction": bool_from_X,
        "stormwater_infiltration": bool_from_X,
        "stormwater_infiltration_new": true_if_one,
        "stormwater_public_water": bool_from_X,
        "stormwater_public_water_new": true_if_one,
        "stormwater_sewage": bool_from_X,
        "stormwater_sewage_new": true_if_one,
        "stormwater_self_use": bool_from_X,
        # Umweltrechtliche Angaben
        "environmental_geothermal_probes_planned": bool_from_X,
        "environmental_special_drilling_or_pump_tests": bool_from_X,
        "environmental_solar_installation_planned": bool_from_X,
        "environmental_contaminated_site_affected": bool_from_X,
        "environmental_groundwater_intervention_required": bool_from_X,
        "environmental_soil_intervention_planned": bool_from_X,
        "environmental_noise_protection_required": bool_from_X,
        "environmental_material_extraction_planned": bool_from_X,
        "environmental_sewer_construction_or_change": bool_from_X,
        "environmental_energy_certificate_required": bool_from_X,
        # Angaben zur Sicherheit
        "safety_fire_protection_canton_required": bool_from_X,
        "safety_fire_protection_heating_required": bool_from_X,
        "safety_fire_protection_communal_required": bool_from_X,
        "safety_employees_affected": bool_from_X,
        "safety_incident_zone_or_infrastructure": bool_from_X,
        "safety_flood_prone_area": bool_from_X,
        "safety_shelter_obligation": bool_from_X,
        # Kantonsstrasse, Wald
        "street_highway_affected": bool_from_X,
        "street_min_distance_undershot": bool_from_X,
        "street_new_or_intensified_access": bool_from_X,
        "street_advertising_planned": bool_from_X,
        "forest_min_distance_undershot": bool_from_X,
        "forest_project_in_forest": bool_from_X,
        # Bauen ausserhalb der Bauzone
        "outside_building_zone_agricultural_use": bool_from_X,
        "outside_building_zone_legal_nonconforming_use": bool_from_X,
        "outside_building_zone_other_project": bool_from_X,
        "outside_building_zone_terrain_modification": bool_from_X,
        # Weitere Angaben, Gewässer, ...
        "special_public_water_body_affected": bool_from_X,
        "special_water_distance_undershot": bool_from_X,
        "special_water_intervention_planned": bool_from_X,
        "special_monument_or_visibility_affected": bool_from_X,
        "special_airspace_obstacle_planned": bool_from_X,
        # Baukosten
        "cost_building_without_land": float,
        "cost_environmental_works": float,
        "cost_total": float,
        "canton_entry_date": sap_date_else_none,
        "canton_internal_deadline": sap_date_else_none,
        "canton_provisional_closure_date": sap_date_else_none,
        "canton_processing_duration_days": int_or_none,
        "canton_cantonal_road_affected": bool_from_X,
        "canton_water_affected": bool_from_X,
        "canton_forest_distance": bool_from_X,
        "canton_special_case_dev": bool_from_X,
        "canton_groundwater_lowering_planned": bool_from_X,
        "canton_awa": bool_from_X,
        "canton_construction_project_in_forest": bool_from_X,
        "canton_flood_hazard": bool_from_X,
        "canton_monument_protection": bool_from_X,
        "canton_hiking_trails": bool_from_X,
        "canton_townscape_protection": bool_from_X,
        "canton_major_accident_ordinance_affected": bool_from_X,
        "canton_archaeology": bool_from_X,
        "canton_traffic": bool_from_X,
        "canton_noise_protection": bool_from_X,
        "canton_material_extraction": bool_from_X,
        "canton_agv": bool_from_X,
        "canton_cycle_paths": bool_from_X,
        "canton_subsequent_application": bool_from_X,
        "canton_koko_date": sap_date_else_none,
        "canton_municipal_decision": sap_date_else_none,
    },
)


class KtAargauDossierLoader(DossierLoader):
    filter_dossier_ids: List[str] | None = None

    def __init__(self):
        self._sap_access = SAPAccess(**settings.DOSSIER_IMPORT["SAP_ACCESS"])

    def list_dossier_count_per_municipality(self) -> List[Tuple[str, str, str]]:
        """
        Return a list of municipalities with the number of dossiers to be migrated, each.

        Returns:
            List[Tuple[Optional[str], str]]: List of (municipality, dossier_count) pairs.
        """

        return self._sap_access.list_dossier_count_per_municipality()

    def get_dossier_ids(self, segment) -> List[str]:
        return self._sap_access.get_dossier_ids(segment)

    @classmethod
    def set_dossier_filter(cls, dossier_ids: List[str] | None):
        cls.filter_dossier_ids = dossier_ids

    @classmethod
    def get_dossier_filter(cls) -> List[str] | None:
        return cls.filter_dossier_ids

    @Timer("load_dossiers", logger=None)
    def load_dossiers(self, param: DossierImport):
        yield from (
            self.map_data(data)
            for data in self._sap_access.query_dossiers(
                dossier_or_segment=param.source_file.name
                if param.source_file
                else None,
                only_dossier_ids=self.get_dossier_filter(),
            )
        )

    @classmethod
    @Timer("map_data", logger=None)
    def map_data(cls, data):
        return cls._map(MAPPING.mappings, MAPPING.result_type, data, MAPPING.converter)

    @classmethod
    def _map(
        cls,
        mappings: Dict[str, Union[str, Transform]],
        target_class: T,
        data: Dict,
        converters: Optional[Dict[str, Callable]] = None,
    ) -> T:
        if converters is None:  # pragma: no cover
            converters = {}
        mapped_values = {
            # extract the jsonpath value and apply any converter or keep the original one
            field: cls._get_converted_value_for_field(field, data, converters, mapping)
            for field, mapping in mappings.items()
        }

        return target_class(**mapped_values)

    @classmethod
    def _get_converted_value_for_field(cls, field, data, converters, mapping):
        value = cls._extract_value(mapping, data)
        return cls._convert(field, value, converters)

    @classmethod
    def _convert(cls, field, value, converters):
        converter = converters.get(field, noop)
        try:
            return converter(value)
        except Exception:  # pragma: no cover
            converter_name = (
                converter.__name__
                if hasattr(converter, "__name__")
                else type(converter)
            )
            log.warning(
                f"Cannot convert '{field}' with value '{value}' using converter '{converter_name}'"
            )
            return value

    @classmethod
    def _extract_value(cls, mapping: Union[str, Transform], data: Dict):
        if type(mapping) is str:
            # build the jsonpath expression for each field, substitude placeholders with toplevel dict values and search
            # for the value of the jsonpath expression in the dict
            json_path = f"$.{mapping}".format_map(defaultdict(lambda: None, data))
            matches = (
                m.value
                for m in parse(json_path).find(data)
                if m.value not in [None, ""]
            )
            return next(matches, None)

        mapping: Transform
        if not cls._use_subdata(mapping):  # pragma: no cover
            return cls._map(
                mapping.mappings, mapping.result_type, data, mapping.converter
            )

        subdata_path = f"$.{mapping.data_path}".format_map(
            defaultdict(lambda: None, data)
        )
        subdata_list = parse(subdata_path).find(data)
        return [
            cls._map(mapping.mappings, mapping.result_type, d.value, mapping.converter)
            for d in subdata_list
        ]

    @classmethod
    def _use_subdata(cls, mapping):
        return mapping.data_path and mapping.data_path != "$"
