import datetime
from functools import partial

import faker
import pytest
from caluma.caluma_form import models as form_models
from caluma.caluma_workflow import models as workflow_models
from django.conf import settings
from django.core.management import call_command

from camac.conftest import reload_urlconf
from camac.core import utils as core_utils
from camac.gever import apimodels
from camac.gever.api import GeverAPI
from camac.gever.client import Endpoint, GEVERClient
from camac.tests.utils import Utils


@pytest.fixture(scope="module")
def vcr_config(request):
    def _make_vcr_path(suggested_name):
        """Overrule the vcr_cassette_dir fixture in camac.conftest."""
        module_basename = request.module.__name__.rsplit(".", 1)[-1]
        return f"{module_basename}__{suggested_name}.yaml"

    # We don't match on host, so when the tests run in CI, and we don't have
    # the CMI API available (and in a known state), we can still replay the
    # "known" responses
    return {
        "match_on": ["method", "path", "query"],
        "filter_headers": ["authorization"],
        "path_transformer": _make_vcr_path,
    }


@pytest.fixture(autouse=True)
def enable_gever_urls():
    """Ensure GEVER urls are enabled for our tests.

    Other modules won't explicitly need it, so we're taking
    care to restore the previous setting afterwards
    """
    old_setting = settings.GEVER["ENABLED"]
    settings.GEVER["ENABLED"] = True
    reload_urlconf("camac.urls")
    yield
    settings.GEVER["ENABLED"] = old_setting


@pytest.fixture(autouse=True)
def cleanup_gever(be_gever_settings, mocker, vcr):
    """Cleanup (our) GEVER objects after each test run.

    All Geschaeft objects that have been created, will be removed again after
    the test has run. This ensures the next run will not have any leaked objects
    still lying around.
    """
    spy = mocker.spy(Endpoint, "create")
    yield

    if spy.call_count == 0:
        return
    client = GEVERClient()
    for g in client.geschaeft.by_attribute("customHerkunftsnummer", "5000-*"):
        client.geschaeft.delete(g)  # pragma: no cover


@pytest.fixture
def gever_geschaeft_in_cmi(vcr, be_gever_settings):
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
    vcr, be_instance, gever_geschaeft_in_cmi: apimodels.Geschaeft
):
    """Return a tuple of a BE instance and a GEVER Geschaeft that are linked together."""

    # Instance needs eBau Number for this to work. We set a really high
    # year so we don't conflict with "human" test data
    core_utils.assign_ebau_nr(be_instance, year=5000)

    api_client = GEVERClient()
    gever_geschaeft_in_cmi.customHerkunftsNummer = be_instance.case.meta["ebau-number"]
    gever_geschaeft_in_cmi.set_linked_instance_ids([be_instance.pk])
    api_client.geschaeft.update(gever_geschaeft_in_cmi)
    be_instance.case.meta[GeverAPI.META_KEY_BASE_GESCHAEFT] = str(
        gever_geschaeft_in_cmi.guid
    )
    be_instance.case.save()

    return be_instance, gever_geschaeft_in_cmi


@pytest.fixture
def gever_config_data(db):
    call_command("loaddata", settings.ROOT_DIR("kt_bern/data/gever.json"))


@pytest.fixture
def gever_test_utils(be_instance, utils: Utils):
    """Provide test utils based on the camac "utils" fixture."""
    utils_cls = type(utils)

    class Helper(utils_cls):
        def add_plot_data(self):
            """
            Add plots to the be_instance.

            Plot has impact on folder name as well as the Geschaeftstitel.
            """
            doc = be_instance.case.document
            utils.add_table_answer(
                doc,
                "parzelle",
                [
                    {
                        "parzellennummer": 473,
                        "e-grid-nr": "CH334687350542",
                        "lagekoordinaten-ost": 2599941.0,
                        "lagekoordinaten-nord": 1198923.0,
                    },
                    {
                        "parzellennummer": 2592,
                        "e-grid-nr": "CH913553467614",
                        "lagekoordinaten-ost": 2601995.0,
                        "lagekoordinaten-nord": 1201340.0,
                    },
                ],
            )

    return Helper()


@pytest.fixture
def be_gever_task(settings):
    call_command(
        "loaddata",
        settings.ROOT_DIR("kt_bern/config/caluma_gever.json"),
    )

    gever_task, _ = workflow_models.Task.objects.get_or_create(
        slug="gever",
        defaults={"type": workflow_models.Task.TYPE_COMPLETE_TASK_FORM},
        form="gever",
    )
    return gever_task


@pytest.fixture
def gever_groups(group_factory, be_gever_settings):
    agr_group_main = group_factory(
        service__slug=settings.GEVER["AGR_SERVICE_SLUG_BAUEN"]
    )
    agr_group_shooting = group_factory(
        service__slug=settings.GEVER["AGR_SERVICE_SLUG_SHOOTING_NOISE"]
    )

    return (agr_group_main, agr_group_shooting)


@pytest.fixture
def be_gever_workitem(
    be_instance,
    be_gever_task,
    caluma_question_factory,
    caluma_answer_factory,
    caluma_document_factory,
    caluma_question_option_factory,
    gever_groups,
):
    gever_task, _ = workflow_models.Task.objects.get_or_create(
        slug="gever", defaults={"type": workflow_models.Task.TYPE_COMPLETE_TASK_FORM}
    )

    gever_work_item = workflow_models.WorkItem.objects.create(
        task=gever_task,
        name=gever_task.name,
        addressed_groups=[str(g.service_id) for g in gever_groups],
        case=be_instance.case,
        status=workflow_models.WorkItem.STATUS_READY,
        document=form_models.Document.objects.create_document_for_task(
            gever_task, None
        ),
    )

    ff = faker.Faker()

    af = partial(caluma_answer_factory, document=gever_work_item.document)

    # We only set the stuff that's *required* here.
    af(question_id="agr-titel", value=ff.text())
    af(question_id="agr-grundbucheintrag", value="agr-grundbucheintrag-ja")
    af(question_id="agr-koordinate-nord", value=1300000.0)
    af(question_id="agr-koordinate-ost", value=2480000.0)
    af(question_id="agr-parzellen", value="1234,4566")
    af(question_id="agr-voranfrage", value="agr-voranfrage-nein")

    return gever_work_item
