import logging
import os.path

import pytest
import xmlschema
from alexandria.core.factories import (
    CategoryFactory,
    DocumentFactory,
    FileFactory,
    MarkFactory,
)
from alexandria.core.models import Document
from pyxb import IncompleteElementContentError, UnprocessedElementContentError

from camac.constants.kt_bern import ECH_BASE_DELIVERY
from camac.document.models import Attachment
from camac.ech0211 import formatters
from camac.ech0211.utils import clean_text_for_xml

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "form",
    ["baugesuch", "einfache vorabklaerung", "vollstaendige vorabklaerung"],
)
def test_base_delivery(
    form,
    set_application_be,
    ech_instance_be,
    multilang,
    master_data_is_visible_mock,
    fake_request,
):
    configured_base_delivery_formatter = formatters.BaseDeliveryFormatter()

    xml = formatters.delivery(
        ech_instance_be,
        subject=form,
        message_type=ECH_BASE_DELIVERY,
        eventBaseDelivery=configured_base_delivery_formatter.format_base_delivery(
            ech_instance_be, fake_request
        ),
    )

    assert xml

    my_dir = os.path.dirname(__file__)
    my_schema = xmlschema.XMLSchema(my_dir + "/../xsd/ech_0211_2_0.xsd")
    try:
        xml_data = xml.toxml()
    except (
        IncompleteElementContentError,
        UnprocessedElementContentError,
    ) as e:  # pragma: no cover
        logger.error(e.details())
        raise

    my_schema.validate(xml_data)


def test_office(set_application_be, ech_instance_be, ech_snapshot, multilang):
    off = formatters.office(
        ech_instance_be.responsible_service(filter_type="municipality"),
        organization_category="ebaube",
    )
    ech_snapshot(off.toxml(element_name="office"))


@pytest.mark.parametrize("amount", [0, 1, 2])
@pytest.mark.parametrize("with_display_name", [True, False])
@pytest.mark.django_db
def test_get_documents(
    attachment_factory,
    amount,
    with_display_name,
    ech_snapshot,
    settings,
    application_settings,
    fake_request,
):
    application_settings["DOCUMENT_BACKEND"] = "camac-ng"
    settings.INTERNAL_BASE_URL = "http://ebau.localhost"
    context = {}
    if with_display_name:
        context = {"displayName": "baz"}
    uuids = [
        "7604864d-fada-4431-b63b-fc9f4915233d",
        "23daf554-c2f5-4aa2-b5f2-734a96ed84d8",
    ]
    for count in range(1, amount + 1):
        attachment_factory(
            name="foo.bar",
            context=context,
            attachment_id=count,
            uuid=uuids[count - 1],
            mime_type="application/pdf",
        )

    xml = formatters.get_documents(
        Attachment.objects.filter(uuid__in=uuids), fake_request
    )

    assert xml

    for doc in xml:
        try:
            ech_snapshot(doc.toxml(element_name="doc"))
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise


@pytest.mark.django_db
def test_get_alexandria_documents(
    ech_snapshot,
    settings,
    application_settings,
    group,
    instance,
    fake_request,
    mocker,
):
    mocker.patch(
        "camac.alexandria.extensions.visibilities.CustomVisibility._all_visible_instances",
        return_value=[instance.pk],
    )

    application_settings["DOCUMENT_BACKEND"] = "alexandria"
    settings.INTERNAL_BASE_URL = "http://ebau.localhost"

    void = MarkFactory(pk="void")
    decision = MarkFactory(pk="decision")

    visible_category = CategoryFactory(
        metainfo={"access": {group.role.name: {"visibility": "all"}}}
    )
    hidden_category = CategoryFactory()

    d1 = DocumentFactory(
        pk="7604864d-fada-4431-b63b-fc9f4915233d",
        category=visible_category,
        metainfo={"camac-instance-id": instance.pk},
    )
    d1.marks.add(void)
    FileFactory(document=d1)

    d2 = DocumentFactory(
        pk="23daf554-c2f5-4aa2-b5f2-734a96ed84d8",
        category=visible_category,
        metainfo={"camac-instance-id": instance.pk},
    )
    FileFactory(document=d2)

    d2.marks.add(decision)
    d3 = DocumentFactory(
        pk="394f53af-24bc-4324-986e-c3901c310263",
        category=visible_category,
        metainfo={"camac-instance-id": instance.pk},
    )
    FileFactory(document=d3)

    # Document that should not be visible
    d4 = DocumentFactory(
        pk="c1e547d5-4d98-479f-87fb-d3fb382d0f1c",
        category=hidden_category,
        metainfo={"camac-instance-id": instance.pk},
    )
    FileFactory(document=d4)

    xml = formatters.get_documents(
        Document.objects.filter(pk__in=[d1.pk, d2.pk, d3.pk, d4.pk]), fake_request
    )

    assert xml
    assert len(xml) == 3

    for doc in xml:
        try:
            ech_snapshot(doc.toxml(element_name="doc"))
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise


@pytest.mark.parametrize(
    ("value", "min_length", "max_length", "expected"),
    [
        (" foo ", 0, 2, "f…"),
        (" f", 3, 10, "f.."),
        (" foo  ", 1, 10, "foo"),
    ],
)
def test_assure_string_length(value, min_length, max_length, expected):
    assert formatters.assure_string_length(value, min_length, max_length) == expected


@pytest.mark.parametrize(
    ("text", "expected_result"),
    [
        # Replacement of illegal characters
        ("test\x0b.pdf", "test.pdf"),
        ("test\x0c.pdf", "test.pdf"),
        ("test\x0e.pdf", "test.pdf"),
        ("test\u0001.pdf", "test.pdf"),
        ("test\ud8ff.pdf", "test.pdf"),
        ("test\ufffe.pdf", "test.pdf"),
        ("test\x0b\x0c\x03.pdf", "test.pdf"),
        # Ensure legal characters are kept
        ("test.pdf", "test.pdf"),
        ("test\u0009.pdf", "test\u0009.pdf"),
        ("test\u000a.pdf", "test\u000a.pdf"),
        ("test\u00f6.pdf", "test\u00f6.pdf"),
    ],
)
def test_clean_text_for_xml(text, expected_result):
    assert clean_text_for_xml(text) == expected_result
