import pytest


@pytest.fixture
def mandatory_answers():
    return {
        "beschreibung-bauvorhaben": "test beschreibung",
        "form-name": "Baugesuch",
        "gemeinde": "Testgemeinde",
        "parzelle": [{"ort-parzelle": "Burgdorf", "parzellennummer": "1586"}],
        "personalien-gesuchstellerin": [
            {
                "name-gesuchstellerin": "Testname",
                "ort-gesuchstellerin": "Testort",
                "plz-gesuchstellerin": 2323,
                "vorname-gesuchstellerin": "Testvorname",
            }
        ],
    }


@pytest.fixture
def ech_instance(db, admin_user, instance_service_factory):
    inst_serv = instance_service_factory(
        instance__user=admin_user,
        service__name="Leitbehörde Burgdorf",
        service__zip="3400",
        service__address="Teststrasse 23",
    )
    return inst_serv.instance
