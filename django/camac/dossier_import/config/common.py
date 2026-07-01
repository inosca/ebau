import mimetypes

from caluma.caluma_form import api as form_api
from caluma.caluma_form.models import Question

from camac.instance.models import Instance

# add mime types by file extension here if some exotic
# files are to imported that are not recognized
mimetypes.add_type("application/vnd.ms-outlook", ".msg")


class PersonalDataTriageFieldsMixin:
    """Answer the personal data triage questions based on the imported tables."""

    def _post_write_fields(self, instance: Instance, dossier):
        self._write_triage_fields(instance)
        return super()._post_write_fields(instance, dossier)

    def _write_triage_fields(self, instance: Instance):
        """Write triage answers for personal data.

        The table questions for landowner, and project author are only displayed
        if the associated triage question whether the data is different from the
        applicant is answered with yes. This method checks if there is any data
        in the personal table and answers the triage question accordingly.
        """

        for table_question in [
            "grundeigentuemerin",
            "projektverfasserin",
            # As the invoice recipient can not be passed to the import, the
            # table will always be empty and the triage question will always be
            # answered with "no". However, we still use the same logic as for
            # the others in order to avoid more code.
            "rechnungsempfaengerin",
        ]:
            table_answer = instance.case.document.answers.filter(
                question_id=table_question
            ).first()
            has_rows = table_answer.documents.exists() if table_answer else False

            suffix = "ja" if has_rows else "nein"
            triage_question = f"{table_question}-abweichend"
            value = f"{triage_question}-{suffix}"

            form_api.save_answer(
                document=instance.case.document,
                question=Question.objects.get(pk=triage_question),
                value=value,
                user=self._caluma_user,
            )
