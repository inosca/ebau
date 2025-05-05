# Test API model behaviour.
#
# Note: This is mainly to explore the dataclasses-json stuff, but also
# to verify behaviour of the classes

import datetime
import json
from uuid import UUID

from .. import apimodels


def test_subclass_overflow_attrs():
    sample = {
        "guid": "fb79267b-08a5-4d93-9dba-1f4eba3dcf1e",
        "version": 3,
        "typeName": "Geschaeft",
        "unexpected": "spanish inquisition",
        "bemerkung": "hello",
        "customArchiviert": False,
        # "customGrundbucheintrag": None,
        # "customOrdnungsgemaess": None,
        # "customVerfahrenseingang": None,
        "geschaeftsstatus": "InBearbeitung",
        "lifecycleStatus": "InBearbeitung",
    }

    jsondata = json.dumps(sample)

    geschaeft = apimodels.Geschaeft.schema().loads(jsondata, partial=True)

    assert geschaeft.other_attributes["unexpected"] == "spanish inquisition"
    assert geschaeft.guid == UUID("fb79267b-08a5-4d93-9dba-1f4eba3dcf1e")


def test_to_json_and_back_roundtrip():
    geschaeft = apimodels.Geschaeft(
        guid=UUID("fb79267b-08a5-4d93-9dba-1f4eba3dcf1e"),
        version=8,
        typeName="Geschäft",
        other_attributes={
            "customDringlDir": False,
            "customDringlVorstoesser": False,
            "customDringlgewaehrt": False,
            "customFederfuehrendesAmt": {
                "displayName": "Amt für Digitalisierungsfragen",
                "guid": "035641ae-a54a-49f7-bb39-a4e926d17c1e",
                "url": "/Amt/035641aea54a49f7bb39a4e926d17c1e",
            },
            "customRRGeschaeft": False,
            "customUeberwiesen": False,
            "customVorstossBeantwortet": False,
            "custommitVoranfrage": False,
            "geschaeftseigner": {
                "displayName": "Generalsekretariat; GS",
                "guid": "e59bbb03-d396-40c6-b0f2-61a46862a0fa",
                "url": "/Organisationseinheit/e59bbb03d39640c6b0f261a46862a0fa",
            },
            "zugriffsteuerung": "Offen",
        },
        geschaeftsstatus="InBearbeitung",
        lifecycleStatus="InBearbeitung",
        customArchiviert=False,
        bemerkung="Geschäftsart: 14.311, 14.310\r\n"
        'Herkunft "Gemeinden", "Regierungsstadthalteramt"\r\n'
        'Verfahrensstand: "Offen", "Abgeschlossen"\r\n'
        "Gemeinde BFS-Nummer, einige Beispiele rüberziehen\r\n"
        "Erledigungsart: Einige Beispiele rein",
        customGrundbucheintrag=False,
        customOrdnungsgemaess=False,
        customVerfahrenseingang=datetime.date(2025, 3, 12),
        customVerfahrensende=datetime.date(2025, 3, 12),
        beginn=datetime.date(2025, 1, 30),
        titel="test dvo",
        laufnummer="2025-STA-2",
    )

    geschaeft_json = geschaeft.to_json()

    geschaeft_copy = apimodels.Geschaeft.schema().loads(geschaeft_json)

    geschaeft_dict = json.loads(geschaeft_json)

    assert geschaeft_dict["customVerfahrenseingang"] == "12.03.2025"

    assert geschaeft_copy.titel == geschaeft.titel
    assert geschaeft_copy.beginn == geschaeft.beginn
    assert geschaeft_copy.laufnummer == geschaeft.laufnummer
    assert geschaeft_copy.customVerfahrenseingang == geschaeft.customVerfahrenseingang


def test_instance_id_linking():
    gesch = apimodels.Geschaeft(
        guid=None,
        version=0,
        typeName="Geschaeft",
        lifecycleStatus=apimodels.LifecycleStatus.IN_BEARBEITUNG,
        geschaeftsstatus=apimodels.GeschaeftsStatus.IN_BEARBEITUNG,
    )

    gesch.set_linked_instance_ids([123])
    assert 123 in gesch.get_linked_instance_ids()

    gesch.link_new_instance_id(5555)
    # both must still be linked
    assert 123 in gesch.get_linked_instance_ids()
    assert 5555 in gesch.get_linked_instance_ids()

    assert gesch.parentkey == "ebaube:123,5555"
