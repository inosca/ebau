import pytest

from camac.dossier_import.dossier_classes import Dossier
from camac.user.models import User


@pytest.mark.parametrize(
    [
        "value",
        "previous_value",
        "expected_result",
        "has_responsible_service",
        "extra_user",
        "expected_message",
    ],
    [
        ("", None, None, True, False, None),
        ("admin@example.com", None, "admin@example.com", True, False, None),
        (None, "admin@example.com", "admin@example.com", True, False, None),
        # LOESCHEN is a typo, no deletion should happen
        (
            "<LOESCHEN>",
            "admin@example.com",
            "admin@example.com",
            True,
            False,
            "Keinen Benutzer mit Mailadresse <LOESCHEN> gefunden",
        ),
        # LÖSCHEN is the correct DELETE_KEYWORD
        ("<LÖSCHEN>", "admin@example.com", "admin@example.com", True, False, None),
        (
            "admin@example.com",
            None,
            None,
            False,
            False,
            (
                "Keine verantwortliche Stelle gefunden, kann "
                "verantwortliche Person nicht festlegen"
            ),
        ),
        (
            "admin@example.com",
            None,
            None,
            True,
            True,
            (
                "Es existieren mehrere Benutzer mit dieser "
                "E-Mail-Adresse: admin@example.com"
            ),
        ),
        (
            "inexistant@example.com",
            None,
            None,
            True,
            True,
            "Keinen Benutzer mit Mailadresse inexistant@example.com gefunden",
        ),
    ],
)
@pytest.mark.parametrize("service_group__name", ["municipality"])
def test_responsible_user_writer(
    be_dossier_import_settings,
    admin_user,
    setup_dossier_writer,
    be_instance,
    service,
    value,
    previous_value,
    user_factory,
    expected_result,
    has_responsible_service,
    extra_user,
    expected_message,
):
    # Lazy import - the dossier writer reads config upon import, where it's
    # not ready yet when running tests
    from ..writers import ResponsibleUserWriter

    setup_dossier_writer("kt_bern")
    dossier = Dossier("2024-07-25", "blah")
    dossier._meta = Dossier.Meta("new")
    dossier.responsible = value

    writer = ResponsibleUserWriter("test")
    writer.context = {"dossier": dossier}

    if extra_user:
        user_factory(email=admin_user.email)

    # ensure our code can run as expected
    if has_responsible_service:
        be_instance.instance_services.create(active=1, service=service)
        assert be_instance.responsible_service()
    else:
        be_instance.instance_services.update(active=0)
        assert not be_instance.responsible_service()

    if previous_value:
        be_instance.responsible_services.create(
            responsible_user=User.objects.get(email=previous_value),
            service=be_instance.responsible_service(),
        )

    writer.write(be_instance, value)

    if expected_message:
        assert any(
            expected_message in err.detail for err in dossier._meta.errors
        ), dossier._meta.errors
    else:
        assert dossier._meta.errors == []
        assert dossier._meta.warnings == []

    if expected_result:
        be_instance.responsible_services.filter(
            responsible_user__email=expected_result,
        ).exists()
    else:
        assert not be_instance.responsible_services.filter(
            responsible_user__isnull=False,
        ).exists()
