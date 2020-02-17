from ..data_preparation import get_document
from .caluma_document_data import baugesuch_data, vorabklaerung_data


def test_get_document(vorabklaerung_einfach_filled, baugesuch_filled, instance_factory):
    # Test Baugesuch
    instance_1 = instance_factory(pk=1)
    data = get_document(instance_1.pk)
    # Make sure the order of sub-lists is consistent
    data["parzelle"] = sorted(data["parzelle"], key=lambda k: k["e-grid-nr"])
    data["personalien-gesuchstellerin"] = sorted(
        data["personalien-gesuchstellerin"], key=lambda k: k["name-gesuchstellerin"]
    )
    assert data == baugesuch_data

    # Test Vorabklärung
    instance_2 = instance_factory(pk=2)
    data = get_document(instance_2.pk)
    assert data == vorabklaerung_data
