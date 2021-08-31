import shutil
from pathlib import Path

from caluma.caluma_form.models import Answer, Document, Question
from caluma.caluma_user.models import BaseUser
from django.conf import settings
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError

from camac.core.models import AuthorityLocation
from camac.document.models import Attachment, AttachmentSection
from camac.instance import domain_logic, models
from camac.user.models import Group, Location, User

INSTANCE_STATE_DONE_ID = 25
GROUP_KOOR_ARE_BG_ID = 142
FORM_ARCHIVDOSSIER_ID = 293


def import_dossiers(records):
    return [_import_dossier(record) for record in records]


def _import_dossier(data):
    caluma_user = BaseUser()
    camac_user = User.objects.get(
        username=settings.APPLICATION["DOSSIER_IMPORT"]["USER"]
    )
    instance_state = models.InstanceState.objects.get(
        instance_state_id=INSTANCE_STATE_DONE_ID
    )
    group = Group.objects.get(group_id=GROUP_KOOR_ARE_BG_ID)
    location = Location.objects.get(
        communal_federal_number=int("".join(filter(str.isdigit, data["gemeinde"])))
    )

    for required_key in settings.APPLICATION["DOSSIER_IMPORT"].get("REQUIRED_KEYS", []):
        if required_key not in data.keys():
            raise ValidationError(
                f"The required field {required_key} has not been found in the record {data}"
            )  # pragma: no cover

    imported_instance = models.Instance.objects.filter(
        **{"case__meta__external-id": data["parashift-id"]}
    ).first()

    if imported_instance:  # pragma: no cover
        print(f"The instance with Nr. {imported_instance.pk} has already been imported")
        return

    creation_data = {
        "instance_state": instance_state,
        "location": location,
        "form": models.Form.objects.get(form_id=FORM_ARCHIVDOSSIER_ID),  # Archivdossier
        "user": camac_user,
        "group": group,
        "previous_instance_state": instance_state,
        "year": data["erfassungsjahr"],
    }

    instance = domain_logic.CreateInstanceLogic.create(
        creation_data,
        caluma_user,
        camac_user,
        group,
        lead=AuthorityLocation.objects.filter(location_id=location.location_id)
        .first()
        .authority_id,
        is_modification=False,
        caluma_form="building-permit",
        source_instance=None,
    )

    instance.case.meta["external-id"] = data["parashift-id"]
    instance.case.save()

    instance.form.description = "KOOR-ARE-BG;Koordinationsstelle f\u00fcr Baueingaben Amt f\u00fcr Raumentwicklung"
    instance.form.save()

    _write_answers(instance, data)
    _write_attachments(instance, data)

    return instance


def _write_answers(instance, data):
    # write the parcel-number and building-law-numer in the parcels table
    plot_table = instance.case.document.answers.create(question_id="parcels")
    plot_row = Document.objects.create(form_id="parcel-table")
    plot_row.answers.create(question_id="parcel-number", value=data["parzelle-nr"])
    plot_row.answers.create(
        question_id="building-law-number", value=data["baurecht-nr"]
    )
    plot_table.documents.add(plot_row)

    # write the last-name in the applicant table
    applicant_table = instance.case.document.answers.create(question_id="applicant")
    applicant_row = Document.objects.create(form_id="personal-data-table")
    applicant_row.answers.create(question_id="last-name", value=data["gesuchsteller"])
    applicant_table.documents.add(applicant_row)

    # write simple answers
    Answer.objects.create(
        value=data["vorhaben"],
        document=instance.case.document,
        question=Question.objects.get(slug="proposal-description"),
    )
    Answer.objects.create(
        value=data["ort"],
        document=instance.case.document,
        question=Question.objects.get(slug="parcel-city"),
    )
    print(f"The Instance with Nr. {instance.pk} has been imported")


def _write_attachments(instance, data):
    user = User.objects.get(username=settings.APPLICATION["DOSSIER_IMPORT"]["USER"])
    group = Group.objects.get(group_id=GROUP_KOOR_ARE_BG_ID)

    for document in data["documents"]:
        path = f"{settings.MEDIA_ROOT}/attachments/files/{instance.pk}"
        Path(path).mkdir(parents=True, exist_ok=True)
        with open(f'{path}/{document["name"]}', "wb") as output_file:
            document["data"].seek(0)
            shutil.copyfileobj(document["data"], output_file)

            attachment = Attachment.objects.create(
                instance=instance,
                user=user,
                service=group.service,
                group=group,
                name=document["name"],
                context={},
                path=f"attachments/files/{instance.pk}/{document['name']}",
                size=output_file.truncate(),
                date=now(),
                mime_type="application/pdf",
            )
            attachment_section = AttachmentSection.objects.get(
                attachment_section_id=document["section"]
            )
            attachment_section.attachments.add(attachment)
