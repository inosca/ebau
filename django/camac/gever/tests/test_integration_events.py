import pytest
from caluma.caluma_workflow.api import complete_work_item

from camac.document.models import Attachment
from camac.gever import events as gever_events


@pytest.mark.vcr
@pytest.mark.freeze_time("2025-05-12 15:15:15+02:00")
@pytest.mark.django_db(reset_sequences=True)
def test_decision_decreed(
    be_gever_settings,
    be_instance,
    attachment_factory,
    gever_config_data,
    gever_test_utils,
    be_gever_task,
    admin_client,
    gever_groups,
    linked_instance_and_geschaeft,
    caluma_work_item_factory,
    be_gever_workitem,
    caluma_admin_user,
    be_decision_settings,
    be_distribution_settings,
    django_q_sync_mode,
    instance_state_factory,
    group_factory,
    active_inquiry_factory,
    user_factory,
    mocker,
    disable_ech0211_settings,
):
    """Test event: Decision.

    Assuming a GEVER Geschaeft has already been created, we need to ensure that
    the documents are re-synchronized at the point of decision.
    """

    instance_state_factory(
        name=be_decision_settings["INSTANCE_STATE_AFTER_NEGATIVE_DECISION"]
    )

    # Don't care about unrelated side effects today
    mocker.patch("camac.notification.utils.send_mail")
    mocker.patch(
        "camac.document.views.AttachmentView.get_queryset",
        # get_queryset() is calles with a group parameter, but we don't care
        # here - just return all of them
        side_effect=lambda _: Attachment.objects.all(),
    )

    attachments = attachment_factory.create_batch(
        2,
        instance=be_instance,
        service=gever_groups[0].service,
        context={"isDecision": True},
    )

    work_item = caluma_work_item_factory(
        case=be_instance.case, task_id=be_decision_settings["TASK"]
    )

    # Necessary for complete_work_item()
    work_item.child_case.status = work_item.child_case.STATUS_COMPLETED
    work_item.child_case.save()

    complete_work_item(work_item, caluma_admin_user)

    for att in attachments:
        # Ensure the "new" attachments have been sent to GEVER
        att.refresh_from_db()
        assert att.context["gever_document_id"]


def test_events_gever_disabled(db, disable_gever_settings, instance):
    assert gever_events.decision_decreed(instance) is False
    assert gever_events.sync_button_pressed(instance) is False
