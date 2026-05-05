import pytest
from caluma.caluma_form.models import Question
from django.urls import reverse
from pytest_lazy_fixtures import lf
from rest_framework import status

from camac.gis.models import GISDataSource

SG_EGRID = "CH538777599655"
BE_EGRID = "CH968746351115"


@pytest.fixture
def oereb_config(
    db,
    caluma_question_factory,
    caluma_question_option_factory,
    gis_data_source_factory,
):
    caluma_question_factory(
        pk="parzellennummer",
        label="Parzellennummer",
        type=Question.TYPE_TEXT,
    )
    caluma_question_factory(
        pk="gemeinde",
        label="Gemeinde",
        type=Question.TYPE_DYNAMIC_CHOICE,
        data_source="Municipalities",
    )
    caluma_question_factory(
        pk="zonenplan",
        label="Zonenplan",
        type=Question.TYPE_TEXT,
    )
    caluma_question_factory(
        pk="kbs",
        label="Belasteter Standort?",
        type=Question.TYPE_CHOICE,
    )
    caluma_question_option_factory(
        question_id="kbs",
        option__pk="kbs-ja",
        option__label="Ja",
    )
    caluma_question_option_factory(
        question_id="kbs",
        option__pk="kbs-nein",
        option__label="Nein",
    )

    return gis_data_source_factory(
        client=GISDataSource.CLIENT_OEREB,
        config={
            "realestate_properties": [
                {
                    "property": "Number",
                    "question": "parzellennummer",
                },
                {
                    "property": "MunicipalityCode",
                    "question": "gemeinde",
                    "cast": "municipality_bfs_to_dynamic_option",
                },
            ],
            "restriction_on_landownership_collections": [
                {
                    "theme": "ch.Nutzungsplanung",
                    "question": "zonenplan",
                },
            ],
            "concerned_themes": [
                {
                    "theme": [
                        "ch.BelasteteStandorte",
                        "ch.BelasteteStandorteMilitaer",
                        "ch.BelasteteStandorteZivileFlugplaetze",
                        "ch.BelasteteStandorteOeffentlicherVerkehr",
                    ],
                    "question": "kbs",
                }
            ],
        },
    )


@pytest.fixture
def be_oereb_config(mocker, oereb_config, service_factory, settings):
    settings.OEREB_URL = "https://www.oereb2.apps.be.ch"

    municipality = service_factory(
        pk=99,
        trans__name="Gemeinde Bern",
        external_identifier="351",
    )

    mocker.patch(
        "camac.caluma.extensions.data_sources.Municipalities.get_data",
        return_value=[[municipality.pk, {"de": "Bern"}]],
    )


@pytest.fixture
def sg_oereb_config(mocker, oereb_config, service_factory, settings):
    settings.OEREB_URL = "https://oereb.geo.sg.ch/ktsg/wsgi/oereb"

    municipality = service_factory(
        pk=99,
        trans__name="Gemeinde St.Gallen",
        external_identifier="3203",
    )

    mocker.patch(
        "camac.caluma.extensions.data_sources.Municipalities.get_data",
        return_value=[[municipality.pk, {"de": "St.Gallen"}]],
    )


@pytest.mark.parametrize(
    ("config", "egrid"),
    [
        (lf("sg_oereb_config"), SG_EGRID),
        (lf("be_oereb_config"), BE_EGRID),
    ],
)
@pytest.mark.vcr
def test_oereb_client(
    admin_client,
    celery_fake_worker,
    config,
    egrid,
    gis_snapshot,
    vcr_config,
):
    response = admin_client.get(reverse("gis-data"), data={"egrid": egrid})

    assert response.status_code == status.HTTP_200_OK

    celery_fake_worker.run_tasks()

    response = admin_client.get(reverse("gis-data", args=[response.json()["task_id"]]))

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert not result.get("errors")
    assert result["data"] == gis_snapshot


@pytest.mark.parametrize(
    ("reason", "error_msg"),
    [
        pytest.param(
            "out_of_bounds",
            "Keine ÖREB Daten für die E-GRID-Nr. CH968746351115 gefunden. Die Parzelle könnte ausserhalb des Kantons liegen.",
            id="out_of_bounds",
        ),
        pytest.param(
            "invalid_language",
            "Erreur 400 lors de la récupération des données depuis l'API RDPPF",
            id="invalid_language",
        ),
    ],
)
@pytest.mark.vcr
def test_oereb_errors(
    admin_client,
    celery_fake_worker,
    error_msg,
    reason,
    sg_oereb_config,
    vcr_config,
):
    egrid = SG_EGRID
    language = "de"

    if reason == "out_of_bounds":
        egrid = BE_EGRID
    elif reason == "invalid_language":
        language = "fr"

    response = admin_client.get(
        reverse("gis-data"),
        data={"egrid": egrid},
        HTTP_LANGUAGE=language,
        HTTP_ACCEPT_LANGUAGE=language,
    )

    assert response.status_code == status.HTTP_200_OK

    celery_fake_worker.run_tasks()

    response = admin_client.get(
        reverse("gis-data", args=[response.json()["task_id"]]),
        HTTP_LANGUAGE=language,
        HTTP_ACCEPT_LANGUAGE=language,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["errors"][0]["detail"] == error_msg
