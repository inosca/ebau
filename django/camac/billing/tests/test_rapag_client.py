import datetime
from unittest.mock import MagicMock

import pytest

from camac.billing.kt_ag.client import RapagClient
from camac.billing.kt_ag.models import (
    RapagOrderNumberSequence,
    RapagSalesOrder,
    RapagSalesOrderGetItem,
    RapagSalesOrderPos,
    RapagStatus,
)


@pytest.fixture(scope="session", autouse=True)
def setup_sql_views():
    """Prevent SQL views setup for these tests."""
    return


@pytest.fixture
def mock_rapag_sequence(monkeypatch):
    mock_get_next = MagicMock(return_value="123456")
    monkeypatch.setattr(RapagOrderNumberSequence, "get_next", mock_get_next)
    return "DIBA123456"


@pytest.fixture
def test_pdf_content():
    import pathlib

    project_root = pathlib.Path(__file__).parent.parent.parent.parent
    pdf_path = project_root / "camac/document/tests/data/important.pdf"
    return pdf_path.read_bytes()


@pytest.mark.vcr
# think of sanitizing recorded cassette yaml file and remove any authentication secret (basic auth and bearer tokens and auth reponse) when recording new responses
def test_get_sales_orders_real(ag_billing_settings):
    result = RapagClient().get_sales_orders()

    # Basic verification of the response
    assert isinstance(result, list)
    assert len(result) > 1
    # If the API returns results, verify they have the expected structure
    for order in result:
        assert isinstance(order, RapagSalesOrderGetItem)
        assert order.ext_aufnr or order.auftr_key
        if order.status:
            # Verify it's a valid status if present
            assert any(s.value == order.status for s in RapagStatus)


@pytest.mark.vcr
# think of sanitizing recorded cassette yaml file and remove any authentication secret (basic auth and bearer tokens and auth reponse) when recording new responses
def test_create_sales_order_real(
    ag_billing_settings, test_pdf_content, mock_rapag_sequence
):
    client = RapagClient()

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    order = RapagSalesOrder(
        ext_aufnr=f"BAUGES{timestamp}",
        name="Eberhard",
        vorname="Thomas",
        strasse="Schulhausstrasse",
        haus_nr="84",
        plz="5000",
        ort="Aarau",
        land="CH",
        email="thomas.eberhard@test.ch",
        email_re_empf="",
        mail_vers="X",
        tel_nr="0791234567",
        bes_betr=700,
        waerk="CHF",
        debitor_nr_import="",
        file_name="Testdokument.pdf",
        bin_data=test_pdf_content,
        pos=[
            RapagSalesOrderPos(
                auftr_pos="10",
                matnr="106973",
                ktext="Test Position 10",
                menge=1,
                meins="LE",
                preis=400,
                waers="CHF",
                ltext="Positionslangtext Pos 1 Positionslangtext Pos 1 Positionslangtext Pos 1",
            ),
            RapagSalesOrderPos(
                auftr_pos="20",
                matnr="106973",
                ktext="Test Position 20",
                menge=1,
                meins="LE",
                preis=300,
                waers="CHF",
                ltext="Positionslangtext Pos 2 Positionslangtext Pos 2 Positionslangtext Pos 2",
            ),
        ],
    )

    response = client.create_sales_order(order)
    assert response.state == "success"
    assert not response.error

    # Verify that the order can be retrieved and check its status
    auftr_key = mock_rapag_sequence
    retrieved_orders = client.get_sales_orders(ktag_auftr_key=auftr_key)
    assert len(retrieved_orders) == 1
    retrieved_order = retrieved_orders[0]
    assert isinstance(retrieved_order, RapagSalesOrderGetItem)
    assert retrieved_order.auftr_key == auftr_key
    assert retrieved_order.status is not None
    assert any(s.value == retrieved_order.status for s in RapagStatus)

    # Log sapFakturaUrl for inspection
    sap_faktura_url = retrieved_order.sap_faktura_url
    print(f"\nsapFakturaUrl for {auftr_key}: {sap_faktura_url}")
