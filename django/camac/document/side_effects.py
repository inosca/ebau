from django.conf import settings
from django.utils import timezone

from camac.constants import kt_uri as uri_constants
from camac.core.models import BuildingAuthorityButtonstate, WorkflowEntry


def create_workflow_entry(attachment, request):
    """When the applicant downloads decision documents, write workflow date."""

    if not request.group or request.group.pk != settings.APPLICATION.get(
        "APPLICANT_GROUP_ID"
    ):
        return

    if not attachment.context.get("isDecision"):
        return

    buttons = BuildingAuthorityButtonstate.objects.filter(
        instance=attachment.instance,
        building_authority_button_id__in=[
            uri_constants.BUILDINGAUTHORITY_BUTTON_DECISION,
            uri_constants.BUILDINGAUTHORITY_BUTTON_PRELIMINARY_DECISION,
        ],
        is_clicked=True,
    )
    mapping = {
        uri_constants.BUILDINGAUTHORITY_BUTTON_DECISION: uri_constants.WORKFLOW_ENTRY_RECEIVED_DECISION,
        uri_constants.BUILDINGAUTHORITY_BUTTON_PRELIMINARY_DECISION: uri_constants.WORKFLOW_ENTRY_RECEIVED_PRELIMINARY_DECISION,
    }
    for button in buttons:
        WorkflowEntry.objects.get_or_create(
            instance=attachment.instance,
            workflow_item_id=mapping[button.building_authority_button_id],
            group=1,
            defaults={"workflow_date": timezone.now().replace(microsecond=0)},
        )
