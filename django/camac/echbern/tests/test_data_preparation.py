from ..data_preparation import (
    get_document,
    slugs_baugesuch,
    slugs_vorabklaerung_einfach,
)
from .caluma_document_data import baugesuch_data, vorabklaerung_data


def all_question_slugs(table):
    slugs = []
    for key, sub in table.items():
        if key == "top":
            slugs.extend([slug for slug, _ in sub])
        else:
            slugs.extend([key, *[slug for slug, _ in sub[0]]])

    return slugs


def test_get_document(vorabklaerung_einfach_filled, baugesuch_filled, mocker):
    # Instead of building a corresponding document, we just "whitelist" all
    # occurring question slugs, effectively removing the impact of the
    # DocumentValidator.visible_questions call.
    mock = mocker.patch(
        "camac.echbern.data_preparation.DocumentValidator.visible_questions"
    )
    mock.return_value = all_question_slugs(slugs_baugesuch)
    # Test Baugesuch
    data = get_document(baugesuch_filled.case.instance.pk)
    # Make sure the order of sub-lists is consistent
    data["parzelle"] = sorted(data["parzelle"], key=lambda k: k["e-grid-nr"])
    data["personalien-gesuchstellerin"] = sorted(
        data["personalien-gesuchstellerin"], key=lambda k: k["name-gesuchstellerin"]
    )
    assert data == baugesuch_data

    # Test Vorabklärung
    mock.return_value = all_question_slugs(slugs_vorabklaerung_einfach)
    data = get_document(vorabklaerung_einfach_filled.case.instance.pk)
    assert data == vorabklaerung_data
