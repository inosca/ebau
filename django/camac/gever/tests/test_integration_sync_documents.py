import datetime

import pytest

from camac.document.models import Attachment
from camac.gever import api, apimodels, client
from camac.utils import retry


@pytest.mark.parametrize("has_plot_data", [True, False])
@pytest.mark.django_db(reset_sequences=True)
@pytest.mark.vcr
@pytest.mark.freeze_time("2025-05-12 15:15:15+02:00")
def test_sync_documents(
    be_gever_settings,
    gever_groups,
    linked_instance_and_geschaeft,
    attachment_factory,
    be_gever_workitem,
    has_plot_data,
    gever_test_utils,
    mocker,
):
    be_instance, geschaeft = linked_instance_and_geschaeft

    if has_plot_data:
        # Plot has impact on folder name
        gever_test_utils.add_plot_data()

    # We need reset_sequences(see django_db mark above)
    # to ensure that VCR will properly replay our requests, and that our code
    # finds the data needed in the responses from VCR
    assert be_instance.pk == 1

    attachments = attachment_factory.create_batch(2, instance=be_instance)
    # We don't wanna test the document module's visibility layer here
    mocker.patch(
        "camac.document.views.AttachmentView.get_queryset",
        # get_queryset() is calles with a group parameter, but we don't care
        # here - just return all of them
        side_effect=lambda _: Attachment.objects.all(),
    )

    gever = api.GeverAPI(instance=be_instance)

    # sync_documents tries to find the Geschaeft via ebau number. Due to
    # the fact that the API is async, even though it's "HerkunftsNr" is set,
    # we might not yet find the object via search
    retry(gever.get_or_create_instance_folder, sleep_between_tries=1)
    result = gever.sync_documents()

    assert result == {"created": 2, "updated": 0}

    api_client = client.GEVERClient()
    reloaded: apimodels.Geschaeft = geschaeft.ref().resolve(api_client)

    # ensure the reloaded geschaeft now has a folder that matches be_instance,
    # and the folder contains our 3 attachments.
    folders = reloaded.get_folders(api_client)
    matching_folders = [f for f in folders if f.titel.startswith(f"{be_instance.pk} ")]

    assert len(matching_folders) == 1
    the_folder = matching_folders[0]

    assert the_folder.titel == (
        "1 Baugesuch Parzelle(n) 473, 2592"
        if has_plot_data
        else "1 Baugesuch ohne Parzellenangabe"
    )

    gever_docs = sorted([f.resolve(api_client).titel for f in the_folder.children])

    ebau_docs = sorted(att.name for att in attachments)

    assert gever_docs == ebau_docs

    attachments.append(attachment_factory(instance=be_instance))

    # modify one of the attachments
    attachments[0].refresh_from_db()  # don't drop the link created by sync
    attachments[0].date = attachments[0].date + datetime.timedelta(seconds=3)
    attachments[0].save()

    ebau_docs_after_update = sorted(att.name for att in attachments)

    # Re-initialize gever api, we want to simulate a second sync, and not
    # keeping state between the sync calls
    gever2 = api.GeverAPI(instance=be_instance)

    result_after_update = gever2.sync_documents()
    assert result_after_update == {"created": 1, "updated": 1}

    the_folder_after_update = the_folder.ref().resolve(api_client)
    gever_docs_after_update = sorted(
        [f.resolve(api_client).titel for f in the_folder_after_update.children]
    )

    assert gever_docs_after_update == ebau_docs_after_update
