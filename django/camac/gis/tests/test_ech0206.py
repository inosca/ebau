import json

import pytest
from caluma.caluma_form.models import Question
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status

from camac.gis.models import GISDataSource


@pytest.fixture
def ech0206_data_sources(
    caluma_question_factory,
    caluma_question_option_factory,
    caluma_option_factory,
    settings,
):
    call_command("loaddata", settings.ROOT_DIR("kt_gr/config/gis.json"))

    gis_questions = [
        ("egid-nr", Question.TYPE_TEXT),
        (
            "energie-waermequelle-heizung",
            Question.TYPE_CHOICE,
            [
                "7500",
                "7501",
                "7510",
                "7511",
                "7512",
                "7513",
                "7520",
                "7530",
                "7540",
                "7541",
                "7542",
                "7550",
                "7560",
                "7570",
                "7580",
                "7581",
                "7582",
                "7598",
                "7599",
                "noch-nicht-festgelegt",
            ],
        ),
        (
            "energie-waermequelle-warmwasser",
            Question.TYPE_CHOICE,
            [
                "7500",
                "7501",
                "7510",
                "7511",
                "7512",
                "7513",
                "7520",
                "7530",
                "7540",
                "7541",
                "7542",
                "7550",
                "7560",
                "7570",
                "7580",
                "7581",
                "7582",
                "7598",
                "7599",
                "noch-nicht-festgelegt",
            ],
        ),
        (
            "waermeerzeuger-warmwasser",
            Question.TYPE_CHOICE,
            [
                "7600",
                "7610",
                "7620",
                "7630",
                "7632",
                "7634",
                "7640",
                "7650",
                "7651",
                "7660",
                "7699",
            ],
        ),
        (
            "waermeerzeuger-heizung",
            Question.TYPE_CHOICE,
            [
                "7400",
                "7410",
                "7420",
                "7430",
                "7431",
                "7432",
                "7433",
                "7434",
                "7435",
                "7436",
                "7440",
                "7441",
                "7450",
                "7451",
                "7460",
                "7461",
                "7499",
                "noch-nicht-festgelegt",
            ],
        ),
    ]

    for config in gis_questions:
        slug = config[0]
        question_type = config[1]
        q = caluma_question_factory(slug=slug, type=question_type, label=slug)
        if len(config) == 3:
            for option in config[2]:
                caluma_question_option_factory(
                    question=q,
                    option=caluma_option_factory(slug=f"{slug}-{option}", label=option),
                )

    return GISDataSource.objects.all()


@pytest.fixture
def ech0206__config(ech0206_data_sources, gis_data_source_factory):
    # Remove/disable configs that are handled in test_kt_gr.py
    ech0206_data_sources.filter(client__contains="GisClient").update(disabled=True)

    gis_data_source_factory(
        client=GISDataSource.CLIENT_KT_GR,
        config=[
            {
                "identifier": "gebaeudeadressen_av",
                "properties": [
                    {"question": "egid-nr", "propertyName": "gwr_egid"},
                ],
            },
        ],
        # Make sure the configs are loaded in the right order
        sort=0,
    )


@pytest.mark.parametrize(
    ("query_x", "query_y"),
    [
        (
            2759664.9038492967,
            1191395.5015286694,
        ),  # multiple egid numbers with multiple properties
        (
            2759647.4234941704,
            1191526.8007143869,
        ),  # egid nr with Energiebezugsfläche
        (
            2759652.9068137,
            1191423.1268269215,
        ),  # no egid number
        (
            2759746.044642407,
            1191415.6188414234,
        ),  # single egid number
        (
            2759772.4989033034,
            1191611.9958049427,
        ),  # Energie-/Wärmequelle Heizung= Unbestimmt & official building = NN
        (
            2760073.7106244904,
            1191456.8678512666,
        ),  # Werden Flächen beheizt? --> Nein  and Ist ein Warmwasseranschluss geplant? --> Nein
        (
            2759626.1504406286,
            1191908.3321774867,
        ),  # Ist ein Warmwasseranschluss geplant? --> Nein
    ],
)
@pytest.mark.vcr
@pytest.mark.django_db
def test_ech0206_client(
    admin_client,
    gis_snapshot,
    vcr_config,
    ech0206__config,
    celery_fake_worker,
    query_x,
    query_y,
):
    query = {"markers": [{"x": query_x, "y": query_y}], "geometry": "POINT"}
    task_response = admin_client.get(
        reverse("gis-data"),
        data={
            "query": json.dumps(query),
            "form": "baugesuch",
        },
    )

    assert task_response.status_code == status.HTTP_200_OK

    task_id = task_response.json()["task_id"]

    # let "celery" process the task
    celery_fake_worker.run_tasks()

    response = admin_client.get(reverse("gis-data", args=[task_id]))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == gis_snapshot
