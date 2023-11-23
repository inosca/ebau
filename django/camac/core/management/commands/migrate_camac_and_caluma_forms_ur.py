from caluma.caluma_workflow.models import Case
from django.core.management.base import BaseCommand
from django.db import transaction

ARCHIVE_DOSSIER_CAMAC_FORM_ID = 293
BGBB_CAMAC_FORM_ID = 41
MELDUNG_VORHABEN_CAMAC_FORM_ID = 290


class Command(BaseCommand):
    help = """Migrate the Camac forms to the correct Caluma forms and vice versa"""

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        # archivedossiers
        all_archive_dossiers = Case.objects.filter(
            document__form_id="archivdossier",
            instance__form_id=BGBB_CAMAC_FORM_ID,
        )
        for archive_dossier in all_archive_dossiers:
            archive_dossier.instance.form_id = ARCHIVE_DOSSIER_CAMAC_FORM_ID
            form_type = archive_dossier.document.answers.get(question_id="form-type")
            if form_type.value != "form-type-archiv":
                form_type.value = "form-type-archiv"
                form_type.save()
                self.stdout.write("Form-type was changed to 'form-type-archiv'")
            archive_dossier.instance.save()
            self.stdout.write(
                f"Archivedossier with instance-id {archive_dossier.instance.pk} was migrated"
            )

        # meldung vorhaben
        all_meldung_vorhaben_dossiers = Case.objects.filter(
            document__form_id="meldung-vorhaben",
            instance__form_id=BGBB_CAMAC_FORM_ID,
        )
        for meldung_vorhaben in all_meldung_vorhaben_dossiers:
            meldung_vorhaben.instance.form_id = MELDUNG_VORHABEN_CAMAC_FORM_ID
            form_type = meldung_vorhaben.document.answers.get(question_id="form-type")
            if form_type.value != "form-type-project-announcement":
                form_type.value = "form-type-project-announcement"
                form_type.save()
                self.stdout.write(
                    "Form-type was changed to 'form-type-project-announcement'"
                )
            meldung_vorhaben.instance.save()
            self.stdout.write(
                f"Meldung Vorhaben with instance-id {meldung_vorhaben.instance.pk} was migrated"
            )

        # baugesuch
        all_bgbb_dossiers = Case.objects.filter(
            document__form_id="building-permit",
            instance__form_id=BGBB_CAMAC_FORM_ID,
        )
        for bgbb_dossier in all_bgbb_dossiers:
            bgbb_dossier.document.form_id = "bgbb"
            form_type = bgbb_dossier.document.answers.get(question_id="form-type")
            if form_type.value != "form-type-bgbb":
                form_type.value = "form-type-bgbb"
                form_type.save()
                self.stdout.write("Form-type was changed to 'form-type-bgbb'")
            bgbb_dossier.document.save()
            self.stdout.write(
                f"BGBB Dossier with instance-id {bgbb_dossier.instance.pk} was migrated"
            )

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
