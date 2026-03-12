from datetime import datetime

from reversion.models import Version

from camac.core.utils import create_history_entry
from camac.timelines.management.commands.migrate_form_timelines import (
    Command as MigrateFormTimelinesCommand,
)


def test_corrections_history(
    db, instance_factory, instance_state_factory, user_factory, settings
):
    instance = instance_factory()
    offset = datetime.now()
    new_state = instance_state_factory(name="new")
    correction_state = instance_state_factory(name="correction")
    user = user_factory()
    cmd = MigrateFormTimelinesCommand()
    cmd.init({})

    create_history_entry(instance, user, settings.CORRECTION["HISTORY_ENTRY"])
    create_history_entry(instance, user, settings.CORRECTION["HISTORY_ENTRY"])
    create_history_entry(instance, user, settings.CORRECTION["HISTORY_ENTRY"])

    instance.set_instance_state(new_state, user)
    instance.set_instance_state(correction_state, user)
    instance.set_instance_state(new_state, user)
    instance.set_instance_state(correction_state, user)
    instance.set_instance_state(new_state, user)
    instance.set_instance_state(correction_state, user)
    instance.set_instance_state(new_state, user)

    # set final state to open correction.
    instance.set_instance_state(correction_state, user)

    reversion_versions = Version.objects.get_for_object(instance).order_by(
        "revision__date_created"
    )

    history_corrections = cmd._get_corrections_from_historyentries(instance, offset)
    reversion_corrections = cmd._get_corrections_from_reversion(
        instance, reversion_versions
    )

    # both methods should yield the same results (3 closed + 1 open-ended)
    assert len(history_corrections) == 4
    assert len(reversion_corrections) == 4

    # last correction should be open-ended
    assert history_corrections[-1][1] is None
    assert reversion_corrections[-1][1] is None
