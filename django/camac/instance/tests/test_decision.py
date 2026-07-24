import pytest

from camac.instance.domain_logic.decision import DecisionLogic


@pytest.mark.parametrize(
    ("form", "is_permit"),
    [
        ("baugesuch", True),
        ("anfrage", False),
        ("auszahlung-abbruchpraemie", False),
    ],
)
def test_notification_config_ag(mocker, set_application_ag, form, is_permit):
    instance = mocker.MagicMock()
    instance.case.document.form_id = form
    expected = (
        {"entscheid-gesuchsteller", "entscheid-behoerden"}
        if is_permit
        else {"beurteilung-behoerden", "beurteilung-gesuchsteller"}
    )
    assert {
        e["template_slug"]
        for e in DecisionLogic.get_notification_config(instance, None)
    } == expected
