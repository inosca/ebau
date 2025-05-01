import datetime
import random

import pytest

from camac.gever import apimodels, models
from camac.gever.client import GEVERClient


@pytest.mark.vcr
@pytest.mark.django_db(reset_sequences=True)
# TODO: mark using all GESCHAEFT_TEMPLATES once the templates work
# @pytest.mark.parametrize("template", constants.GESCHAEFT_TEMPLATES + [None])
@pytest.mark.parametrize("template", [None])
@pytest.mark.parametrize("template_as_obj", [True, False])
def test_create_and_delete_geschaeft(
    be_gever_settings, template, geschaeft_object_templates, template_as_obj
):
    client = GEVERClient()

    if template_as_obj and template:  # pragma: no cover
        # cov: This will be covered once we re-enable the GESCHAEFT_TEMPLATES
        # parametrisation
        template = models.CMIObjectTemplate.objects.get(slug=template)

    org_units = client.orgunit.all()
    aemter = client.amt.all()

    geschaeft = apimodels.Geschaeft(
        guid=None,
        typeName="Geschaeft",
        beginn=datetime.date.today(),
        # Version must be 0 or -1 for a new object
        version=0,
        lifecycleStatus=apimodels.LifecycleStatus.IN_BEARBEITUNG,
        geschaeftsstatus=apimodels.GeschaeftsStatus.IN_BEARBEITUNG,
        titel=f"adfinis-test {datetime.datetime.now().isoformat()}",
        geschaeftseigner=org_units[0].ref(),
        customFederfuehrendesAmt=aemter[0].ref(),
    )
    if not template:
        # This field *must* be set - normally via template
        # TODO: `customRegistraturplan` should be set via template, and we
        # shouldn't need to actually set this. Templates are broken right now
        # however, so we're creating "Geschaeft"s this way.
        regs = client.registraturplan.all()
        geschaeft.customRegistraturplan = regs[0].ref()

    create_resp = client.geschaeft.create(
        geschaeft,
        template=template,
        raise_on_error=False,
    )
    assert create_resp.status_code == 200, create_resp.json()

    delete_resp = client.geschaeft.delete(geschaeft)
    assert delete_resp.status_code == 200, delete_resp.json()


@pytest.mark.vcr
@pytest.mark.django_db(reset_sequences=True)
def test_set_responsible(gever_geschaeft_in_cmi):
    """Verify that we can correctly set the responsible user on the Geschaeft.

    This involves setting both "Sachbearbeiter" and "Geschaeftsverantwortung" fields
    and being able to have them stored properly.
    """
    client = GEVERClient()

    users = client.user.all()

    user0 = random.choice(users).ref()
    user1 = random.choice(users).ref()

    gever_geschaeft_in_cmi.customSachbearbeiter = user0
    gever_geschaeft_in_cmi.customGeschaeftsverantwortung = user1

    resp = client.geschaeft.update(gever_geschaeft_in_cmi, raise_on_error=False)
    assert resp.status_code == 200, resp.json()

    refreshed_geschaeft: apimodels.Geschaeft = gever_geschaeft_in_cmi.ref().resolve(
        client
    )

    assert refreshed_geschaeft.customSachbearbeiter.guid == user0.guid
    assert refreshed_geschaeft.customGeschaeftsverantwortung.guid == user1.guid


@pytest.mark.vcr
@pytest.mark.django_db(reset_sequences=True)
@pytest.mark.parametrize("set_as_ref", [True, False])
def test_set_gemeinde(gever_geschaeft_in_cmi, set_as_ref):
    """Verify that we can correctly set the municipality on the Geschaeft.

    This involves setting both "Sachbearbeiter" and "Geschaeftsverantwortung"
    fields and being able to have them stored properly.
    """
    client = GEVERClient()

    munis = client.municipality.all()

    muni = munis[0].ref() if set_as_ref else munis[0]

    gever_geschaeft_in_cmi.customGemeinde = muni

    resp = client.geschaeft.update(gever_geschaeft_in_cmi, raise_on_error=False)
    assert resp.status_code == 200, resp.json()

    refreshed_geschaeft: apimodels.Geschaeft = gever_geschaeft_in_cmi.ref().resolve(
        client
    )

    assert refreshed_geschaeft.customGemeinde.guid == munis[0].guid


@pytest.mark.vcr
@pytest.mark.django_db(reset_sequences=True)
def test_set_erledigungsart(gever_geschaeft_in_cmi):
    """Verify that we can correctly set the municipality on the Geschaeft.

    This involves setting both "Sachbearbeiter" and "Geschaeftsverantwortung"
    fields and being able to have them stored properly.
    """
    client = GEVERClient()

    all_erledigungsart = client.erledigungsart.all()

    choice = random.choice(all_erledigungsart)

    assert isinstance(all_erledigungsart, list)
    assert len(all_erledigungsart)  # This tests the server contents, but we need it

    gever_geschaeft_in_cmi.customErledigungsart = choice

    resp = client.geschaeft.update(gever_geschaeft_in_cmi, raise_on_error=False)
    assert resp.status_code == 200, resp.json()

    refreshed_geschaeft: apimodels.Geschaeft = gever_geschaeft_in_cmi.ref().resolve(
        client
    )

    assert refreshed_geschaeft.customErledigungsart.guid == choice.guid


@pytest.mark.vcr
@pytest.mark.django_db(reset_sequences=True)
def test_folders(gever_geschaeft_in_cmi):
    client = GEVERClient()

    folder = apimodels.Ordner(
        titel="2025-0331",
        guid=None,
        parent=gever_geschaeft_in_cmi,
        geschaeft=gever_geschaeft_in_cmi,
    )
    folder_create_resp = client.folder.create(folder, raise_on_error=False)
    assert folder_create_resp.status_code <= 201, folder_create_resp.json()

    refreshed_geschaeft: apimodels.Geschaeft = gever_geschaeft_in_cmi.ref().resolve(
        client
    )

    folders = refreshed_geschaeft.get_folders(client)

    assert len(folders) == 1

    assert folders[0].guid == folder.guid


@pytest.mark.vcr
@pytest.mark.django_db(reset_sequences=True)
def test_search_by_ebau_number(linked_instance_and_geschaeft):
    instance, geschaeft = linked_instance_and_geschaeft

    client = GEVERClient()

    ebau_nr = instance.case.meta.get("ebau-number")

    result = client.geschaeft.search_by_ebau_nr(ebau_nr)

    assert len(result) == 1

    assert result[0].guid == geschaeft.guid
