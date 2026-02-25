from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Union

from camac.dossier_import.dossier_classes import Dossier, Person


@dataclass
class Building:
    egid: Optional[str]
    insurance_number: Optional[str]


@dataclass
class Residence:
    number_of_residential_units: Optional[int]
    number_of_rooms: Optional[float]
    of_which_second_homes: Optional[int]


@dataclass
class ValueHolder:
    value: Optional[str]


@dataclass
class ProceduralStatusEntry:
    action: Optional[str] = None
    step: Optional[str] = None
    timestamp: Optional[datetime] = None
    username: Optional[str] = None
    comment: Optional[str] = None


@dataclass
class Comment:
    userid: Optional[str] = None
    username: Optional[str] = None
    text: Optional[str] = None
    timestamp: Optional[datetime] = None


@dataclass
class WorkflowDoc:
    workflow_id: Optional[str] = None
    dms_id: Optional[str] = None
    dms_version: Optional[str] = None
    doc_type: Optional[str] = None
    date: Optional[datetime] = None
    remark: Optional[str] = None
    recipient_id: Optional[str] = None


@dataclass
class WorkflowRecipient:
    id: Optional[str] = None
    workflow_id: Optional[str] = None
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    reason: Optional[str] = None
    active: Optional[bool] = None
    remark: Optional[str] = None
    manually_added: Optional[bool] = None
    date: Optional[datetime] = None
    status: Optional[str] = None
    request: Optional[str] = None
    docs: Optional[List[WorkflowDoc]] = None


@dataclass
class Workflow:
    id: Optional[str] = None
    workflow_type: Optional[str] = None
    date: Optional[datetime] = None
    active: Optional[bool] = None
    status: Optional[str] = None
    recipients: Optional[List[WorkflowRecipient]] = None
    docs: Optional[List[WorkflowDoc]] = None


@dataclass
class Decision:
    type: Optional[str] = None
    decision_date: Optional[datetime] = None
    legal_binding_date: Optional[datetime] = None
    legal_remedy_taken_date: Optional[datetime] = None
    remark: Optional[str] = None


@dataclass
class Deadline:
    type: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    notice: Optional[str] = None
    reason: Optional[str] = None
    completed: Optional[bool] = False


@dataclass
class Authorization:
    userid: Optional[str] = None
    permission: Optional[str] = None


@dataclass
class DossierTypes:
    pgv: Optional[bool] = False
    uvp: Optional[bool] = False
    baugesuch: Optional[bool] = False
    anfrage: Optional[bool] = False
    reklamegesuch: Optional[bool] = False
    vorentscheid: Optional[bool] = False
    rodung: Optional[bool] = False
    abbruchgesuch: Optional[bool] = False
    umnutzung: Optional[bool] = False


# eBau extended nested classes
@dataclass
class CantonStatusHistoryEntry:
    source: Optional[str] = None
    timestamp: Optional[int] = None
    who_text: Optional[str] = None
    comment: Optional[str] = None
    document_id: Optional[str] = None
    document_version: Optional[str] = None
    action_text: Optional[str] = None
    step_text: Optional[str] = None


@dataclass
class CantonComment:
    timestamp: Optional[int] = None
    user_id: Optional[str] = None
    text: Optional[str] = None


@dataclass
class Fee:
    cost_type: Optional[str] = None
    description: Optional[str] = None
    calculation_scheme: Optional[str] = None
    calc_scheme_position: Optional[str] = None
    request_task_id: Optional[str] = None
    unit_price: Optional[str] = None
    amount: Optional[str] = None
    msehi: Optional[str] = None
    take: Optional[bool] = False
    show_in_gv: Optional[bool] = False
    comment_fs: Optional[str] = None
    comment_afb: Optional[str] = None


@dataclass
class KtAgSuspension:
    start_date: Optional[datetime] = None
    resume_date: Optional[datetime] = None
    reason: Optional[str] = None
    note: Optional[str] = None
    prev_status: Optional[str] = None
    creation_date: Optional[datetime] = None


@dataclass
class DocumentStatus:
    dms_id: Optional[str] = None
    dms_version: Optional[str] = None
    status: Optional[str] = None


@dataclass
class KtAargauDossier(Dossier):
    dossier_file_path: Optional[str] = None
    dossier_number: Optional[str] = None  # the DIBA dossier number
    caluma_form_id: Optional[str] = None  # the DIBA form id
    instance_state: Optional[str] = None  # the DIBA instance state
    description: Optional[str] = None
    is_paper: Optional[bool] = None
    municipal_id: Optional[str] = None
    municipal_status: Optional[str] = None
    cantonal_status: Optional[str] = None
    procedural_status: Optional[Union[List[ProceduralStatusEntry], str]] = None
    comments: Optional[Union[List[Comment], str]] = None
    workflows: Optional[Union[List[Workflow], str]] = None
    workflow_docs: Optional[Union[List[WorkflowDoc], str]] = None
    workflow_recipients: Optional[Union[List[WorkflowRecipient], str]] = None
    decisions: Optional[Union[List[Decision], str]] = None
    deadlines: Optional[Union[List[Deadline], str]] = None
    authorizations: Optional[Union[List[Authorization], str]] = None

    creation_date: Optional[str] = None
    building: Optional[Union[List[Building], str]] = None
    responsible_municipality: Optional[str] = None
    is_municipality_light: Optional[bool] = False
    other_municipalities: Optional[Union[List[ValueHolder], str]] = None
    dossier_types: Optional[Union[DossierTypes, str]] = None
    submission_reason: Optional[str] = None
    profiling: Optional[bool] = False
    profiling_date: Optional[Union[datetime, str]] = None
    profiling_reasoning: Optional[str] = None

    # contacts
    invoice_recipient: Optional[Union[List[Person], str]] = None
    legal_representative: Optional[Union[List[Person], str]] = None

    # Zweckbestimmung
    residential_use: Optional[bool] = False
    commercial_and_industrial_use: Optional[bool] = False
    agricultural_use: Optional[bool] = False
    other_buildings: Optional[bool] = False
    residence: Optional[Union[List[Residence], str]] = None
    commercial_and_industrial_type_of_use: Optional[str] = None
    commercial_and_industrial_sector: Optional[str] = None
    owned_land_total_ha: Optional[str] = None
    leased_land_total_ha: Optional[str] = None
    existing_livestock: Optional[str] = None
    new_livestock: Optional[str] = None
    other_buildings_designation: Optional[str] = None
    other_buildings_type_of_use: Optional[str] = None
    parking_affected: Optional[bool] = False
    existing_parking_spaces: Optional[str] = None
    existing_mandatory_spaces: Optional[str] = None
    existing_non_mandatory_spaces: Optional[str] = None
    new_parking_spaces: Optional[str] = None
    new_mandatory_spaces: Optional[str] = None
    new_non_mandatory_spaces: Optional[str] = None

    # Gebäudehülle
    building_envelope_exterior_wall_material: Optional[str] = None
    building_envelope_exterior_wall_color: Optional[str] = None
    building_envelope_roof_covering_material: Optional[str] = None
    building_envelope_roof_covering_color: Optional[str] = None

    # Gebäudeheizung und Energie
    building_heating_none: Optional[bool] = False
    building_heating_existing: Optional[bool] = False
    building_heating_new: Optional[bool] = False
    building_heating_new_kw: Optional[str] = None
    building_heating_replacement: Optional[bool] = False
    building_heating_replacement_kw: Optional[str] = None
    building_heating_unknown: Optional[bool] = False
    building_heating_unknown_explanation: Optional[str] = None
    building_heating_type_oil: Optional[bool] = False
    building_heating_type_oil_new: Optional[bool] = False
    building_heating_type_gas: Optional[bool] = False
    building_heating_type_wood: Optional[bool] = False
    building_heating_type_electric: Optional[bool] = False
    building_heating_type_district: Optional[bool] = False
    building_heating_type_heatpump: Optional[bool] = False
    building_heating_type_heatpump_ground_water: Optional[bool] = False
    building_heating_type_heatpump_air: Optional[bool] = False
    building_heating_type_other: Optional[bool] = False
    building_heating_type_other_text: Optional[str] = None

    # Bauzonen
    zoning_area: Optional[str] = None
    usage_zone: Optional[str] = None
    overlapping_zone: Optional[str] = None
    special_use_plan: Optional[str] = None

    # Dichteziffern
    ratio_utilization_zone_regulation: Optional[str] = None
    ratio_utilization_building_project: Optional[str] = None
    ratio_volume_zone_regulation: Optional[str] = None
    ratio_volume_building_project: Optional[str] = None
    ratio_green_area_zone_regulation: Optional[str] = None
    ratio_green_area_building_project: Optional[str] = None
    ratio_floor_area_zone_regulation: Optional[str] = None
    ratio_floor_area_building_project: Optional[str] = None
    ratio_coverage_zone_regulation: Optional[str] = None
    ratio_coverage_building_project: Optional[str] = None
    # Kanalisation & Entwässerung
    sewage_connection_property: Optional[bool] = False
    sewage_connection_property_presence: Optional[str] = None
    sewage_connection_construction: Optional[bool] = False
    sewage_connection_construction_presence: Optional[str] = None
    stormwater_infiltration: Optional[bool] = False
    stormwater_infiltration_new: Optional[bool] = False
    stormwater_public_water: Optional[bool] = False
    stormwater_public_water_new: Optional[bool] = False
    stormwater_sewage: Optional[bool] = False
    stormwater_sewage_new: Optional[bool] = False
    stormwater_self_use: Optional[bool] = False

    # Bauzonen - weitere Angaben
    zone_water_protection_area_au: Optional[bool] = False
    zone_water_protection_area_bc: Optional[bool] = False
    zone_spring_capture_area: Optional[bool] = False
    zone_flood_hazard: Optional[bool] = False
    zone_seismic_compliance: Optional[str] = None
    zone_sensitivity_level: Optional[str] = None

    # Umweltrechtliche Angaben
    environmental_geothermal_probes_planned: Optional[bool] = False
    environmental_special_drilling_or_pump_tests: Optional[bool] = False
    environmental_solar_installation_planned: Optional[bool] = False
    environmental_contaminated_site_affected: Optional[bool] = False
    environmental_groundwater_intervention_required: Optional[bool] = False
    environmental_soil_intervention_planned: Optional[bool] = False
    environmental_noise_protection_required: Optional[bool] = False
    environmental_material_extraction_planned: Optional[bool] = False
    environmental_sewer_construction_or_change: Optional[bool] = False
    environmental_energy_certificate_required: Optional[bool] = False

    # Angaben zur Sicherheit
    safety_fire_protection_canton_required: Optional[bool] = False
    safety_fire_protection_heating_required: Optional[bool] = False
    safety_fire_protection_communal_required: Optional[bool] = False
    safety_employees_affected: Optional[bool] = False
    safety_incident_zone_or_infrastructure: Optional[bool] = False
    safety_flood_prone_area: Optional[bool] = False
    safety_shelter_obligation: Optional[bool] = False

    # Kantonsstrasse, Wald
    street_highway_affected: Optional[bool] = False
    street_min_distance_undershot: Optional[bool] = False
    street_min_distance_reasoning: Optional[str] = None
    street_new_or_intensified_access: Optional[bool] = False
    street_advertising_planned: Optional[bool] = False
    forest_min_distance_undershot: Optional[bool] = False
    forest_min_distance_reasoning: Optional[str] = None
    forest_project_in_forest: Optional[bool] = False

    # Bauen ausserhalb der Bauzone
    outside_building_zone_agricultural_use: Optional[bool] = False
    outside_building_zone_legal_nonconforming_use: Optional[bool] = False
    outside_building_zone_other_project: Optional[bool] = False
    outside_building_zone_terrain_modification: Optional[bool] = False

    # Weitere Angaben, Gewässer, ...
    special_public_water_body_affected: Optional[bool] = False
    special_water_body_name: Optional[str] = None
    special_water_distance_undershot: Optional[bool] = False
    special_water_distance_reasoning: Optional[str] = None
    special_water_intervention_planned: Optional[bool] = False
    special_monument_or_visibility_affected: Optional[bool] = False
    special_airspace_obstacle_planned: Optional[bool] = False

    # Baukosten
    cost_building_without_land: Optional[float] = None
    cost_environmental_works: Optional[float] = None
    cost_total: Optional[float] = None

    # Weitere Angaben - Bemerkungen
    notes_comments: Optional[str] = None

    # eBau extended
    canton_entry_date: Optional[str] = None
    canton_internal_deadline: Optional[str] = None
    canton_group: Optional[str] = None
    canton_group_name: Optional[str] = None
    canton_assignee: Optional[str] = None
    canton_provisional_closure_date: Optional[str] = None
    canton_closure_code: Optional[str] = None
    canton_processing_duration_days: Optional[int] = None
    canton_lwag_number: Optional[str] = None

    canton_status_history: Optional[List[CantonStatusHistoryEntry]] = None
    canton_comments: Optional[List[CantonComment]] = None

    canton_application_codes: Optional[List[ValueHolder]] = None

    canton_usage_zones: Optional[List[ValueHolder]] = None

    canton_protection_zones: Optional[List[ValueHolder]] = None

    canton_cantonal_road_affected: Optional[bool] = None
    canton_roads: Optional[List[ValueHolder]] = None

    canton_railways: Optional[List[ValueHolder]] = None

    canton_water_affected: Optional[bool] = None
    canton_waters: Optional[List[ValueHolder]] = None

    canton_forest_distance: Optional[bool] = None
    canton_special_case_dev: Optional[bool] = None
    canton_groundwater_lowering_planned: Optional[bool] = None
    canton_awa: Optional[bool] = None
    canton_construction_project_in_forest: Optional[bool] = None
    canton_flood_hazard: Optional[bool] = None
    canton_monument_protection: Optional[bool] = None
    canton_hiking_trails: Optional[bool] = None
    canton_townscape_protection: Optional[bool] = None
    canton_major_accident_ordinance_affected: Optional[bool] = None
    canton_archaeology: Optional[bool] = None
    canton_traffic: Optional[bool] = None
    canton_noise_protection: Optional[bool] = None
    canton_material_extraction: Optional[bool] = None
    canton_agv: Optional[bool] = None
    canton_cycle_paths: Optional[bool] = None

    canton_sewerage: Optional[str] = None
    canton_area_consumption: Optional[str] = None
    canton_koko_date: Optional[str] = None
    canton_koko_status: Optional[str] = None
    canton_municipal_decision: Optional[str] = None
    canton_decision_type: Optional[str] = None
    canton_delay_caused_by: Optional[str] = None
    canton_justification: Optional[str] = None
    canton_subsequent_application: Optional[bool] = None

    canton_fees: Optional[List[Fee]] = None
    canton_suspensions: Optional[List[KtAgSuspension]] = None
    document_statuses: Optional[List[DocumentStatus]] = None
