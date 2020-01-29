from pathlib import Path

import pytest
from caluma.caluma_form.models import Document
from django.conf import settings
from django.core.management import call_command

from camac.utils import build_url

from ..document_merge_service import DMSClient, DMSVisitor


@pytest.fixture
def caluma_form_fixture(db):
    # load caluma config
    path = Path(settings.ROOT_DIR) / "kt_bern" / "config-caluma.json"
    call_command("loaddata", path)

    # load custom caluma data (includes sb1 and sb2)
    path = Path(__file__).parent / "fixtures" / "data-caluma.json"
    call_command("loaddata", path)


@pytest.mark.parametrize(
    "instance_id,form_slug", [(1, "baugesuch"), (1, "sb1"), (1, "sb2"), (3, None)]
)
def test_document_merge_service_snapshot(
    db,
    snapshot,
    service_factory,
    service_group_factory,
    caluma_form_fixture,
    instance_id,
    form_slug,
):

    service_group = service_group_factory(pk=2)
    service_factory(pk=2, service_group=service_group, name="Leitbehörde Burgdorf")

    _filter = {"meta__camac-instance-id": instance_id}
    if form_slug:
        _filter["form__slug"] = form_slug

    root_document = Document.objects.get(**_filter)

    visitor = DMSVisitor()
    snapshot.assert_match(
        visitor.visit(
            root_document, append_receipt_page=(form_slug not in ["sb1", "sb2"])
        )
    )


def test_document_merge_service_client(db, requests_mock):
    template = "some-template"
    faked_result = b"foo\nNot a pdf"

    requests_mock.register_uri(
        "POST",
        build_url(
            settings.DOCUMENT_MERGE_SERVICE_URL,
            f"/template/{template}/merge",
            trailing=True,
        ),
        content=faked_result,
    )

    client = DMSClient("some token")
    result = client.merge({"foo": "some data"}, template)

    assert result == faked_result
