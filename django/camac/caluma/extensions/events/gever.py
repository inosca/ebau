from caluma.caluma_core.events import filter_events, on
from caluma.caluma_form.models import Document
from caluma.caluma_workflow.events import (
    post_resume_work_item,
)
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db import transaction

from camac.caluma.api import CalumaApi
from camac.gever.utils import get_gever_task, is_agr_addressed
from camac.instance.master_data import MasterData
from camac.user.models import Service


@on(post_resume_work_item, raise_exception=True)
@filter_events(lambda: settings.GEVER.get("ENABLED"))
@filter_events(lambda work_item: work_item.task_id == "inquiry")
@filter_events(is_agr_addressed)
@transaction.atomic
def post_resume_inquiry_for_gever(
    sender, work_item, user, context=None, **kwargs
):  # pragma: no cover
    case = work_item.case.family

    if case.work_items.filter(task_id="gever").exists():
        return  # "gever" work-item already exists

    task = get_gever_task()

    agr_service = Service.objects.get(slug=settings.GEVER["AGR_SERVICE_SLUG_BAUEN"])

    gever_work_item = WorkItem.objects.create(
        task=task,
        name=task.name,
        addressed_groups=[str(agr_service.pk)],
        case=case,
        status=WorkItem.STATUS_READY,
        document=Document.objects.create_document_for_task(task, None),
    )

    # fill work-item with instance data
    master_data = MasterData(case)
    api = CalumaApi()
    document = gever_work_item.document

    api.update_or_create_answer(
        document, "agr-titel", create_agr_title(master_data), None
    )

    rows = master_data.plot_data
    if rows:
        parcels = ",".join([str(row["plot_number"]) for row in rows])

        first_parcel = rows[0]
        coord_east = first_parcel["coord_east"]
        coord_north = first_parcel["coord_north"]

        api.update_or_create_answer(document, "agr-parzellen", parcels, None)
        api.update_or_create_answer(document, "agr-koordinate-ost", coord_east, None)
        api.update_or_create_answer(document, "agr-koordinate-nord", coord_north, None)

    if has_preliminary_clarification(master_data.case.instance):
        api.update_or_create_answer(
            document, "agr-voranfrage", "agr-voranfrage-ja", None
        )


def has_preliminary_clarification(instance):  # pragma: no cover
    for link in instance.get_linked_instances():
        document = link.case.document
        instance_type = settings.GEVER["INSTANCE_TYPE_SHORT"][document.form.name.de]
        if instance_type == "VA":
            return True

    return False


def create_agr_title(master_data):  # pragma: no cover
    document = master_data.case.document
    instance_type = settings.GEVER["INSTANCE_TYPE_SHORT"][document.form.name.de]
    gemeinde = master_data.municipality_name
    ebau_nr = master_data.dossier_number
    street = master_data.street
    street_nr = master_data.street_number
    proposal = master_data.proposal

    applicants = ",".join(
        [
            get_applicant_for_agr_title(applicant)
            for applicant in master_data.applicants[:2]
        ]
    )
    return (
        f"{gemeinde}: {instance_type} eBau-Nr. {ebau_nr} "
        f"{applicants}, {street} {street_nr}, {proposal}"
    )


def get_applicant_for_agr_title(applicant_row):  # pragma: no cover
    if applicant_row.get("is_juristic_person"):
        return applicant_row["juristic_name"]
    return f"{applicant_row['first_name']} {applicant_row['last_name']}"
