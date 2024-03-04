import json

import pytest
from caluma.caluma_form.models import Question
from django.urls import reverse
from rest_framework import status

from camac.gis.models import GISDataSource


@pytest.fixture
def gr_data_sources(
    question_factory, question_option_factory, option_factory, mock_municipalities
):
    gis_questions = [
        ("gemeinde", Question.TYPE_DYNAMIC_CHOICE),
        ("parzelle", Question.TYPE_TABLE),
        ("parzellennummer", Question.TYPE_TEXT),
        ("baurecht-nummer", Question.TYPE_TEXT),
        ("ort", Question.TYPE_TEXT),
        ("street-and-housenumber", Question.TYPE_TEXT),
        ("zonenplan", Question.TYPE_TEXT),
        ("genereller-gestaltungsplan", Question.TYPE_TEXT),
        ("genereller-erschliessungsplan", Question.TYPE_TEXT),
        ("folgeplanung", Question.TYPE_TEXT),
        ("e-grid-nr", Question.TYPE_TEXT),
        (
            "waldareal",
            Question.TYPE_CHOICE,
            ["ja", "waldabstandsbereich", "nein"],
        ),
        ("kantonsstrassen", Question.TYPE_CHOICE, ["ja", "nein"]),
        ("ausserhalb-bauzone", Question.TYPE_CHOICE, ["ja", "nein"]),
        (
            "das-bauvorhaben-befindet-sich-in",
            Question.TYPE_MULTIPLE_CHOICE,
            ["gefahrenzone", "gewaesserschutzbereich", "archaeologiezone"],
        ),
        ("gis-map", Question.TYPE_TEXT),
        ("ort-grundstueck", Question.TYPE_TEXT),
        ("art-gewaesserschutzbereich", Question.TYPE_CHOICE, ["au", "nicht-betroffen"]),
        (
            "lageranlagen-gewaesserschutzbereich",
            Question.TYPE_CHOICE,
            ["au", "nicht-betroffen"],
        ),
        (
            "grundwasserschutzzone",
            Question.TYPE_CHOICE,
            ["s1", "s2", "s3", "sh", "sm", "nicht-betroffen"],
        ),
        (
            "lageranlagen-grundwasserschutzzone",
            Question.TYPE_CHOICE,
            ["s1", "s2", "s3", "sh", "sm", "nicht-betroffen"],
        ),
    ]

    for config in gis_questions:
        slug = config[0]
        type = config[1]
        q = question_factory(slug=slug, type=type, label=slug)
        if len(config) == 3:
            for i, option in enumerate(reversed(config[2])):
                question_option_factory(
                    question=q,
                    option=option_factory(slug=f"{slug}-{option}", label=option),
                    sort=i,
                )

    Question.objects.filter(slug="gemeinde").update(data_source="Municipalities")
    mock_municipalities(["Chur", "Roveredo (GR)"])

    return GISDataSource.objects.all()


@pytest.fixture
def gr_config(gis_data_source_factory, question_factory):
    gis_data_source_factory(
        client=GISDataSource.CLIENT_PARAM,
        config=[{"hidden": True, "question": "gis-map", "parameterName": "query"}],
    )
    gis_data_source_factory(
        client=GISDataSource.CLIENT_KT_GR,
        config=[
            {
                "identifier": "liegenschaften",
                "properties": [
                    {
                        "question": "gemeinde",
                        "propertyName": "gdename",
                        "forms": [
                            "baugesuch",
                            "bauanzeige",
                            "solaranlage",
                            "vorlaeufige-beurteilung",
                        ],
                    },
                ],
            },
            {
                "identifier": "gebaeudeadressen_av",
                "properties": [
                    {
                        "question": "street-and-housenumber",
                        "mapper": "street_and_housenumber",
                        "forms": [
                            "baugesuch",
                            "bauanzeige",
                            "solaranlage",
                            "vorlaeufige-beurteilung",
                        ],
                    },
                ],
            },
            {
                "identifier": "zp_wald_puffer",
                "properties": [
                    {
                        "question": "waldareal",
                        "mapper": "near_forest",
                        "forms": ["baugesuch"],
                    },
                ],
            },
            {
                "identifier": "zp_grundnutzung",
                "properties": [
                    {
                        "question": "ausserhalb-bauzone",
                        "propertyName": "Kt_Code",
                        "mapper": "ausserhalb_bauzone",
                        "forms": ["baugesuch"],
                    },
                    {
                        "question": "waldareal",
                        "propertyName": "Kt_Code",
                        "mapper": "in_forest",
                        "forms": ["baugesuch"],
                    },
                    {
                        "question": "das-bauvorhaben-befindet-sich-in",
                        "propertyName": "Kt_Code",
                        "mapper": "archaeologiezone",
                        "forms": ["baugesuch"],
                    },
                ],
            },
            {
                "identifier": "kantonales_strassennetz",
                "properties": [
                    {
                        "question": "kantonsstrassen",
                        "mapper": "yes_or_no",
                        "forms": ["baugesuch"],
                    },
                ],
            },
            {
                "identifier": "zp_gefahrenzonen",
                "properties": [
                    {
                        "question": "das-bauvorhaben-befindet-sich-in",
                        "propertyName": "Kt_Code",
                        "mapper": "gefahrenzone",
                        "forms": ["baugesuch"],
                    },
                ],
            },
            {
                "identifier": "gewaesserschutzbereiche",
                "properties": [
                    {
                        "question": "das-bauvorhaben-befindet-sich-in",
                        "propertyName": "typ",
                        "mapper": "bauvorhaben_gewaesser",
                        "forms": ["baugesuch"],
                    },
                    {
                        "question": "art-gewaesserschutzbereich",
                        "propertyName": "typ",
                        "mapper": "gewaesserschutzbereich",
                        "forms": ["baugesuch"],
                    },
                    {
                        "question": "lageranlagen-gewaesserschutzbereich",
                        "propertyName": "typ",
                        "mapper": "gewaesserschutzbereich",
                        "forms": ["baugesuch"],
                        "hidden": True,
                    },
                ],
            },
            {
                "identifier": "grundwasserschutzzonen",
                "properties": [
                    {
                        "question": "grundwasserschutzzone",
                        "propertyName": "typ",
                        "mapper": "grundwasserschutzzone",
                        "forms": ["baugesuch"],
                    },
                    {
                        "question": "lageranlagen-grundwasserschutzzone",
                        "propertyName": "typ",
                        "mapper": "grundwasserschutzzone",
                        "forms": ["baugesuch"],
                        "hidden": True,
                    },
                ],
            },
            {
                "identifier": "zp_ortsbild_und_kulturgueterschutzzonen",
                "properties": [
                    {
                        "question": "das-bauvorhaben-befindet-sich-in",
                        "propertyName": "Kt_Code",
                        "mapper": "archaeologiezone_2",
                        "forms": ["baugesuch"],
                    },
                ],
            },
            {
                "identifier": "ortschaftsname",
                "properties": [
                    {
                        "question": "ort-grundstueck",
                        "propertyName": "ortschaftsname",
                        "forms": ["baugesuch", "bauanzeige"],
                    },
                ],
            },
        ],
    )


@pytest.mark.parametrize(
    "query,form",
    [
        (
            {
                "markers": [{"x": 2759870.935699284, "y": 1190699.1389424137}],
                "geometry": "POINT",
            },
            "baugesuch",
        ),  # archaeologiezone_2
        (
            {
                "markers": [{"x": 2730678.226988568, "y": 1122327.0823116319}],
                "geometry": "POINT",
            },
            "baugesuch",
        ),
        (
            {
                "markers": [{"x": 2730678.226988568, "y": 1122327.0823116319}],
                "geometry": "POINT",
            },
            "bauanzeige",
        ),
        (
            {
                "markers": [
                    {"x": 2730686.563711087, "y": 1122237.578980265},
                    {"x": 2730701.779260571, "y": 1122223.4682885902},
                ],
                "geometry": "LINESTRING",
            },
            "baugesuch",
        ),
        (
            {
                "markers": [
                    {"x": 2758821.8885866464, "y": 1191884.7759206274},
                    {"x": 2758835.689140816, "y": 1191889.2217609326},
                    {"x": 2758844.747878619, "y": 1191856.4200200567},
                    {"x": 2758832.507804883, "y": 1191854.8711072344},
                ],
                "geometry": "POLYGON",
            },
            "baugesuch",
        ),
        (
            {
                "markers": [
                    {"x": 2731195.9499999997, "y": 1122174.3312499998},
                ],
                "geometry": "POINT",
            },
            "baugesuch",
        ),  # Baurecht
        (
            {
                "markers": [{"x": 2758622.7126099495, "y": 1190131.3069476}],
                "geometry": "POINT",
            },
            "baugesuch",
        ),  # Ausserhalb Bauzone, Wald
        (
            {
                "markers": [{"x": 2760943.8499999996, "y": 1192035.0312499998}],
                "geometry": "POINT",
            },
            "baugesuch",
        ),  # Waldabstandsbereich
        (
            {
                "markers": [
                    {"x": 2760930.5289222472, "y": 1192035.707010256},
                    {"x": 2760963.900865463, "y": 1192057.817393839},
                ],
                "geometry": "LINESTRING",
            },
            "baugesuch",
        ),  # Wald and Waldabstandsbereich
        (
            {
                "markers": [{"x": 2760376.3950000005, "y": 1190000.739375}],
                "geometry": "POINT",
            },
            "baugesuch",
        ),  # Kantonsstrasse
        (
            {
                "markers": [{"x": 2757567.75, "y": 1192209.3312499998}],
                "geometry": "POINT",
            },
            "baugesuch",
        ),  # Gewässerschutzbereich
        (
            {
                "markers": [{"x": 2757771.4499999997, "y": 1192182.0312499998}],
                "geometry": "POINT",
            },
            "baugesuch",
        ),  # Gefahrenzone
        (
            {
                "markers": [{"x": 2759143.4499999997, "y": 1190625.23125}],
                "geometry": "POINT",
            },
            "baugesuch",
        ),  # Archäologische Schutzzone
        (
            {
                "markers": [
                    {"x": 2757239.7999999993, "y": 1191422.925},
                    {"x": 2757141.7999999993, "y": 1191215.725},
                ],
                "geometry": "LINESTRING",
            },
            "baugesuch",
        ),  # Grundwasserschutzzone S2 and S3
    ],
)
@pytest.mark.vcr()
def test_gr_client(
    db,
    admin_client,
    gis_snapshot,
    vcr_config,
    gr_config,
    query,
    form,
    gr_data_sources,
):
    response = admin_client.get(
        reverse("gis-data"),
        data={
            "query": json.dumps(query),
            "form": form,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == gis_snapshot
