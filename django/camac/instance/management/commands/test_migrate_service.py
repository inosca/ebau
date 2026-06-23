from io import StringIO

import pytest
from django.core.management import call_command


@pytest.mark.parametrize("exec", [True, False])
@pytest.mark.parametrize("disable", [True, False])
@pytest.mark.django_db
def test_migrate_service(
    exec,
    disable,
    service_factory,
    instance_service_factory,
    caluma_work_item_factory,
    user_factory,
    snapshot,
    mocker,
    ag_instance,
    set_application_ag,
    service_group_factory,
):
    sg = service_group_factory(name="municipality")
    instance_service_factory(instance=ag_instance, service__service_group=sg)
    source = ag_instance.responsible_service()
    source_2 = service_factory(service_group=sg)
    target = service_factory(service_group=sg)
    work_item = caluma_work_item_factory(
        addressed_groups=[source_2.pk], assigned_users=[user_factory().username]
    )
    controlling_work_item = caluma_work_item_factory(controlling_groups=[source_2.pk])

    mocker.patch(
        "camac.instance.master_data.MasterData.get_question_slug",
        return_value="gemeinde",
    )
    mocker.patch(
        "camac.caluma.extensions.data_sources.Municipalities.get_data",
        return_value=[
            (
                str(source.pk),
                {
                    "de": "Source Municipality",
                    "fr": None,
                    # test escape characters in hstore string
                    "it": "Source escape \\' quote\"",
                },
            ),
            (
                str(target.pk),
                {
                    "de": "Target Municipality",
                    "fr": None,
                    # test escape characters in hstore string
                    "it": "Target escape \\' quote\"",
                },
            ),
        ],
    )

    args = [
        "--source",
        ",".join([str(source.pk), str(source_2.pk)]),
        "--target",
        target.pk,
        "--form-answer",
    ]
    if exec:
        args.append("--exec")
    if disable:
        args.append("--disable")

    out = StringIO()
    call_command("migrate_service", *args, stdout=out)
    ag_instance.refresh_from_db()
    source.refresh_from_db()
    work_item.refresh_from_db()
    controlling_work_item.refresh_from_db()
    addressed_groups = [int(i) for i in work_item.addressed_groups]
    controlling_groups = [int(i) for i in controlling_work_item.controlling_groups]

    if exec:
        assert ag_instance.responsible_service() == target
        assert addressed_groups == [target.pk]
        assert work_item.assigned_users == []
        assert controlling_groups == [target.pk]
        assert ag_instance.case.meta["migrated-from-service"] == source.pk
    else:
        assert ag_instance.responsible_service() == source
        assert not work_item.addressed_groups == target.pk
        assert not work_item.assigned_users == []
        assert not controlling_work_item.controlling_groups == target.pk
        assert "migrated-from-service" not in ag_instance.case.meta

        snapshot.assert_match(
            out.getvalue()
            .replace(str(source.pk), "<<source_id_1>>")
            .replace(str(source_2.pk), "<<source_id_2>>")
            .replace(str(target.pk), "<<target_id>>")
        )
