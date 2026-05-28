import pytest
from caluma.caluma_workflow.api import (
    complete_work_item,
    resume_work_item,
    skip_work_item,
)
from caluma.caluma_workflow.models import WorkItem

from camac.constants import kt_bern as bern_constants


def make_inquiry(
    to_service,
    from_service,
    sent,
    user,
    distribution_child_case,
    distribution_settings,
):
    create_work_item = distribution_child_case.work_items.get(
        task_id=distribution_settings["INQUIRY_CREATE_TASK"],
        addressed_groups=[str(from_service.pk)],
        status=WorkItem.STATUS_READY,
    )

    complete_work_item(
        work_item=create_work_item,
        user=user,
        context={"addressed_groups": [str(to_service.pk)]},
    )

    create_work_item.refresh_from_db()

    work_item = create_work_item.succeeding_work_items.get(
        addressed_groups=[str(to_service.pk)],
        controlling_groups=[str(from_service.pk)],
        status=WorkItem.STATUS_SUSPENDED,
    )

    if sent:
        resume_work_item(work_item=work_item, user=user)
        work_item.refresh_from_db()

    return work_item


@pytest.fixture
def distribution_case_be(
    be_instance,
    caluma_admin_user,
    instance_state_factory,
    be_distribution_settings,
    notification_template_factory,
):
    # this is needed so that simple workflow works
    notification_template_factory(slug="05-bericht-erstellt")
    notification_template_factory(slug="03-verfahrensablauf-fachstelle")
    notification_template_factory(slug="03-verfahrensablauf-gesuchsteller")
    notification_template_factory(slug="03-verfahren-vorzeitig-beendet")
    instance_state_factory(name="circulation")
    instance_state_factory(name="coordination")
    instance_state_factory(
        instance_state_id=bern_constants.INSTANCE_STATE_CORRECTION_IN_PROGRESS,
        name="correction",
    )

    case = be_instance.case

    for task in ["submit", "ebau-number"]:
        skip_work_item(
            work_item=case.work_items.get(task_id=task), user=caluma_admin_user
        )

    return case


@pytest.fixture
def distribution_case_gr(
    gr_instance,
    caluma_admin_user,
    instance_state_factory,
    gr_distribution_settings,
    set_application_gr,
    service,
    service_factory,
    mocker,
    notification_template_factory,
):
    # this is needed so that simple workflow works
    notification_template_factory(slug="verfahrensablauf-fachstelle")
    notification_template_factory(slug="verfahrensablauf-uso")
    notification_template_factory(
        slug="zirkulation-abgebrochen",
        subject="Information über vorzeitiger Abbruch der Stellungnahme",
    )
    instance_state_factory(name="circulation")
    instance_state_factory(name="decision")
    instance_state_factory(
        instance_state_id=bern_constants.INSTANCE_STATE_CORRECTION_IN_PROGRESS,
        name="correction",
    )

    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service,
    )

    case = gr_instance.case

    for task in ["submit", "formal-exam"]:
        skip_work_item(
            work_item=case.work_items.get(task_id=task), user=caluma_admin_user
        )

    return case


@pytest.fixture
def distribution_case_sz(
    sz_instance,
    caluma_admin_user,
    instance_state_factory,
    sz_distribution_settings,
    notification_template_factory,
):
    notification_template_factory(slug="einladung-zur-stellungnahme")

    instance_state_factory(name="circ")
    instance_state_factory(name="redac")

    case = sz_instance.case

    for task in ["submit", "complete-check"]:
        skip_work_item(
            work_item=case.work_items.get(task_id=task), user=caluma_admin_user
        )

    return case


@pytest.fixture
def distribution_case_ag(
    ag_instance,
    caluma_admin_user,
    instance_state_factory,
    ag_distribution_settings,
    set_application_ag,
    service,
    service_factory,
    mocker,
):
    mocker.patch("camac.notification.utils.send_mail")
    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service,
    )

    instance_state_factory(name="init-distribution")
    instance_state_factory(name="circulation")
    service_factory(slug="afb")

    case = ag_instance.case

    for task in ["submit", "formal-exam"]:
        skip_work_item(
            work_item=case.work_items.get(task_id=task), user=caluma_admin_user
        )

    return case


@pytest.fixture
def distribution_child_case_be(distribution_case_be, be_distribution_settings):
    return distribution_case_be.work_items.get(
        task_id=be_distribution_settings["DISTRIBUTION_TASK"]
    ).child_case


@pytest.fixture
def distribution_child_case_gr(distribution_case_gr, gr_distribution_settings):
    return distribution_case_gr.work_items.get(
        task_id=gr_distribution_settings["DISTRIBUTION_TASK"]
    ).child_case


@pytest.fixture
def distribution_child_case_sz(distribution_case_sz, sz_distribution_settings):
    return distribution_case_sz.work_items.get(
        task_id=sz_distribution_settings["DISTRIBUTION_TASK"]
    ).child_case


@pytest.fixture
def distribution_child_case_ag(distribution_case_ag, ag_distribution_settings):
    return distribution_case_ag.work_items.get(
        task_id=ag_distribution_settings["DISTRIBUTION_TASK"]
    ).child_case


@pytest.fixture
def inquiry_factory_be(
    caluma_admin_user,
    distribution_child_case_be,
    be_distribution_settings,
    service,
    service_factory,
):
    def factory(to_service=service_factory(), from_service=service, sent=False):
        return make_inquiry(
            to_service=to_service,
            from_service=from_service,
            sent=sent,
            user=caluma_admin_user,
            distribution_child_case=distribution_child_case_be,
            distribution_settings=be_distribution_settings,
        )

    return factory


@pytest.fixture
def inquiry_factory_gr(
    gr_distribution_settings,
    caluma_admin_user,
    distribution_child_case_gr,
    service_factory,
    service,
):
    def factory(to_service=service_factory(), from_service=service, sent=False):
        return make_inquiry(
            to_service=to_service,
            from_service=from_service,
            sent=sent,
            user=caluma_admin_user,
            distribution_child_case=distribution_child_case_gr,
            distribution_settings=gr_distribution_settings,
        )

    return factory


@pytest.fixture
def inquiry_factory_sz(
    caluma_admin_user,
    distribution_child_case_sz,
    sz_distribution_settings,
    service,
    service_factory,
):
    def factory(to_service=service_factory(), sent=False):
        return make_inquiry(
            to_service=to_service,
            from_service=service,
            sent=sent,
            user=caluma_admin_user,
            distribution_child_case=distribution_child_case_sz,
            distribution_settings=sz_distribution_settings,
        )

    return factory


@pytest.fixture
def inquiry_factory_ag(
    ag_distribution_settings,
    caluma_admin_user,
    distribution_child_case_ag,
    service_factory,
    service,
):
    def factory(to_service=service_factory(), from_service=service, sent=False):
        return make_inquiry(
            to_service=to_service,
            from_service=from_service,
            sent=sent,
            user=caluma_admin_user,
            distribution_child_case=distribution_child_case_ag,
            distribution_settings=ag_distribution_settings,
        )

    return factory
