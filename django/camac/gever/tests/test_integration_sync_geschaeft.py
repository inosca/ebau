import random

import pytest

from camac.caluma.extensions import data_sources
from camac.core import utils as core_utils
from camac.document.models import Attachment
from camac.gever import api, client
from camac.tests.utils import Utils
from camac.utils import retry


def get_user_with_corresponding_gever_user(gever: client.GEVERClient, user_factory):
    """Return a random GEVER user for testing."""
    gever_user = random.choice([user for user in gever.user.all() if user.email])

    db_user = user_factory(email=gever_user.email)
    return db_user, gever_user


@pytest.fixture
def configure_for_gever(
    be_instance,
    be_gever_workitem,
    service_factory,
    mocker,
    instance_service_factory,
    utils: Utils,
    gever_test_utils,
    user_factory,
    gever_groups,
):
    def do_it(api_client, set_erledigungsart, service_group_name, has_responsible_user):
        # Define lead authority, defines "origin"
        lead_auth = service_factory(service_group__name=service_group_name)
        be_instance.instance_services.add(instance_service_factory(service=lead_auth))

        if has_responsible_user:
            responsible_user, gever_user = get_user_with_corresponding_gever_user(
                api_client, user_factory
            )
            be_instance.responsible_services.create(
                service=gever_groups[0].service,
                responsible_user=responsible_user,
            )

        gever_test_utils.add_plot_data()
        if set_erledigungsart:
            erledigungsart, _label = data_sources.GEVERErledigungsart().get_data(
                user=None, question=None, context=None
            )[0]

            utils.add_answer(
                be_gever_workitem.document, "agr-erledigungsart-auswahl", erledigungsart
            )

        # We don't wanna test the document module's visibility layer here
        mocker.patch(
            "camac.document.views.AttachmentView.get_queryset",
            return_value=Attachment.objects.all(),
        )

    return do_it


@pytest.mark.parametrize("set_erledigungsart", [True, False])
@pytest.mark.parametrize("has_responsible_user", [True, False])
@pytest.mark.parametrize("service_group_name", ["municipality", "rsta"])
@pytest.mark.vcr
@pytest.mark.freeze_time("2025-05-12 15:15:15+02:00")
@pytest.mark.django_db(reset_sequences=True)
def test_initial_sync(
    be_gever_settings,
    be_instance,
    attachment_factory,
    gever_config_data,
    gever_groups,
    be_gever_workitem,
    has_responsible_user,
    instance_service_factory,
    service_group_name,
    service_factory,
    user_factory,
    set_erledigungsart,
    snapshot,
    configure_for_gever,
):
    attachments = attachment_factory.create_batch(2, instance=be_instance)

    api_client = client.GEVERClient()

    configure_for_gever(
        api_client, set_erledigungsart, service_group_name, has_responsible_user
    )

    # We need reset_sequences(see django_db mark above)
    # to ensure that VCR will properly replay our requests, and that our code
    # finds the data needed in the responses from VCR
    assert be_instance.pk == 1

    # Instance needs eBau Number for this to work
    core_utils.assign_ebau_nr(be_instance)

    gever = api.GeverAPI(instance=be_instance)

    gever.sync_full()

    # sync_documents tries to find the Geschaeft via ebau number. Due to
    # the fact that the API is async, even though it's "HerkunftsNr" is set,
    # we might not yet find the object via search
    retry(gever.sync_documents, 3, sleep_between_tries=1)

    # ensure the reloaded geschaeft now has a folder that matches be_instance,
    # and the folder contains our 3 attachments.
    reloaded = gever.reload_geschaeft()
    folders = reloaded.get_folders(api_client)
    matching_folders = [f for f in folders if f.titel.startswith(f"{be_instance.pk} ")]

    assert len(matching_folders) == 1
    the_folder = matching_folders[0]

    gever_docs = sorted([f.resolve(api_client).titel for f in the_folder.children])

    ebau_docs = sorted(att.name for att in attachments)

    assert gever_docs == ebau_docs

    # Matching on model objects is fragile, as ordering in the dicts could change.
    # Dict comparison is much more stable
    assert snapshot == reloaded.to_dict()


@pytest.mark.parametrize("set_erledigungsart", [True, False])
@pytest.mark.parametrize("has_responsible_user", [True, False])
@pytest.mark.parametrize("service_group_name", ["municipality", "rsta"])
@pytest.mark.vcr
@pytest.mark.freeze_time("2025-05-14 15:00:15+02:00")
@pytest.mark.django_db(reset_sequences=True)
def test_update_geschaeft(
    be_gever_settings,
    linked_instance_and_geschaeft,
    attachment_factory,
    gever_config_data,
    gever_groups,
    be_gever_workitem,
    has_responsible_user,
    instance_service_factory,
    service_group_name,
    service_factory,
    user_factory,
    set_erledigungsart,
    snapshot,
    configure_for_gever,
):
    be_instance, cmi_geschaeft = linked_instance_and_geschaeft
    attachments = attachment_factory.create_batch(2, instance=be_instance)
    api_client = client.GEVERClient()

    configure_for_gever(
        api_client, set_erledigungsart, service_group_name, has_responsible_user
    )

    gever = api.GeverAPI(instance=be_instance)

    gever.sync_full()
    # ensure the reloaded geschaeft now has a folder that matches be_instance,
    # and the folder contains our 3 attachments.
    reloaded = gever.reload_geschaeft()
    folders = reloaded.get_folders(api_client)
    matching_folders = [f for f in folders if f.titel.startswith(f"{be_instance.pk} ")]

    assert len(matching_folders) == 1
    the_folder = matching_folders[0]

    gever_docs = sorted([f.resolve(api_client).titel for f in the_folder.children])

    # This should now be more than before
    ebau_docs = sorted(att.name for att in attachments)

    assert gever_docs == ebau_docs

    # Matching on model objects is fragile, as ordering in the dicts could change.
    # Dict comparison is much more stable
    assert snapshot == reloaded.to_dict()
