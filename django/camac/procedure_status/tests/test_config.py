import pytest
from django.conf import settings
from django.core.management import call_command
from pydantic import ValidationError

from camac.instance.models import InstanceState
from camac.settings.modules.procedure_status_schema import (
    ProcedureStatusConfig,
    StepMapping,
)


@pytest.mark.parametrize("canton", settings.APPLICATIONS.keys())
@pytest.mark.django_db
def test_all_instance_states_mapped(canton, request):
    short_name = settings.APPLICATIONS[canton]["SHORT_NAME"]

    try:
        module_settings: ProcedureStatusConfig = request.getfixturevalue(
            f"{short_name}_procedure_status_settings"
        )
    except pytest.FixtureLookupError:
        # Cantons that don't use the procedure status module don't have to be
        # checked
        return

    # Load all instance states to compare with the configured instance state
    # mapping
    call_command("loaddata", settings.ROOT_DIR(f"{canton}/config/instance.json"))

    for instance_state_name in InstanceState.objects.values_list("name", flat=True):
        assert instance_state_name in module_settings.instance_state_map, (
            f"Procedure status mapping for instance state '{instance_state_name}' is missing."
        )


def test_instance_state_map_validation():
    with pytest.raises(ValidationError, match="unknown step"):
        ProcedureStatusConfig(
            steps=["submit", "finish"],
            instance_state_map={"new": StepMapping(step="typo")},
        )

    with pytest.raises(ValidationError, match="non-final step"):
        ProcedureStatusConfig(
            steps=["submit", "finish"],
            instance_state_map={"new": StepMapping(step="submit", done=True)},
        )
