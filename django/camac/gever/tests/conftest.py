import datetime

import pytest

from camac.core import utils as core_utils
from camac.gever import apimodels, models
from camac.gever.client import GEVERClient


@pytest.fixture(scope="module")
def vcr_config():
    # We don't match on host, so when the tests run in CI, and we don't have
    # the CMI API available (and in a known state), we can still replay the
    # "known" responses
    return {"match_on": ["method", "path", "query"]}


@pytest.fixture
def gever_geschaeft_in_cmi(be_gever_settings):
    """Generate a GEVER Geschaeft in CMI, ready for testing.

    Will be deleted again after the test has run.
    """
    client = GEVERClient()
    org_units = client.orgunit.search_by_tentaql("FULLTEXT[*]")
    aemter = client.amt.search_by_tentaql("FULLTEXT[*]")

    regs = client.registraturplan.search_by_tentaql("FULLTEXT[*]")

    geschaeft = apimodels.Geschaeft(
        guid=None,
        typeName="Geschaeft",
        beginn=datetime.date.today(),
        # Version must be 0 or -1 for a new object
        version=0,
        # TODO: `customRegistraturplan` should be set via template, and we
        # shouldn't need to actually set this. Templates are broken right now
        # however, so we're creating "Geschaeft"s this way.
        customRegistraturplan=regs[0].ref(),
        lifecycleStatus=apimodels.LifecycleStatus.IN_BEARBEITUNG,
        geschaeftsstatus=apimodels.GeschaeftsStatus.IN_BEARBEITUNG,
        titel=f"adfinis-test {datetime.datetime.now().isoformat()}",
        geschaeftseigner=org_units[0].ref(),
        customFederfuehrendesAmt=aemter[0].ref(),
        customVerfahrenseingang=datetime.date.today(),
        customVerfahrensende=datetime.datetime.now() + datetime.timedelta(days=365),
    )

    client.geschaeft.create(
        geschaeft,
        template=None,
        raise_on_error=True,
    )

    # We should yield the Geschaeft object as it comes from the API, not as we
    # created it
    yield geschaeft.ref().resolve(client)

    client.geschaeft.delete(geschaeft)


@pytest.fixture
def linked_instance_and_geschaeft(
    be_instance, gever_geschaeft_in_cmi: apimodels.Geschaeft
):
    """Return a tuple of a BE instance and a GEVER Geschaeft that are linked together."""

    # Instance needs eBau Number for this to work
    core_utils.assign_ebau_nr(be_instance)

    api_client = GEVERClient()
    gever_geschaeft_in_cmi.customHerkunftsNummer = be_instance.case.meta["ebau-number"]
    gever_geschaeft_in_cmi.set_linked_instance_ids([be_instance.pk])
    api_client.geschaeft.update(gever_geschaeft_in_cmi)

    return be_instance, gever_geschaeft_in_cmi


@pytest.fixture
def geschaeft_object_templates(db):
    templates_data = [
        {
            "pk": "ebau-bg-gemeinde",
            "use_for": "Geschaeft",
            "template_path": "Global\\AGR\\Bauen eBau BG (Gemeinde)",
        },
        {
            "pk": "ebau-bg-rsta",
            "use_for": "Geschaeft",
            "template_path": "Global\\AGR\\Bauen eBau BG (RSTA)",
        },
        {
            "pk": "ebau-va-gemeinde",
            "use_for": "Geschaeft",
            "template_path": "Global\\AGR\\Bauen eBau VA (Gemeinde)",
        },
        {
            "pk": "ebau-va-rsta",
            "use_for": "Geschaeft",
            "template_path": "Global\\AGR\\Bauen eBau VA (RSTA)",
        },
    ]

    return [
        obj
        for obj, _ in [
            models.CMIObjectTemplate.objects.get_or_create(**args)
            for args in templates_data
        ]
    ]
