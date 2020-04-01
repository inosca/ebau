from django.db import migrations
from django.core.exceptions import ObjectDoesNotExist


def migrate_wald_answers(apps, schema_editor):
    # Migrate the answers

    Document = apps.get_model("caluma_form", "Document")

    documents = Document.objects.all()

    for document in documents:
        try:
            waldabstandsbereich_answer = document.answers.get(
                question_id="liegt-die-baute-im-waldabstandsbereich"
            )
            baute_im_wald_answer = document.answers.get(
                question_id="handelt-es-sich-um-eine-baute-im-wald"
            )

            if baute_im_wald_answer.value == "handelt-es-sich-um-eine-baute-im-wald-ja":
                baute_im_wald_answer.value = (
                    "handelt-es-sich-um-eine-baute-im-wald-im-wald"
                )
            elif (
                waldabstandsbereich_answer.value
                == "liegt-die-baute-im-waldabstandsbereich-ja"
            ):
                baute_im_wald_answer.value = (
                    "handelt-es-sich-um-eine-baute-im-wald-innert-30m"
                )

            baute_im_wald_answer.save()

        except ObjectDoesNotExist:
            pass

    # Delete the question 'liegt-die-baute-im-waldabstandsbereich'

    try:
        Question = apps.get_model("caluma_form", "Question")

        Question.objects.get(
            pk="liegt-die-baute-im-waldabstandsbereich"
        ).answers.all().delete()
        Question.objects.get(pk="liegt-die-baute-im-waldabstandsbereich").delete()

    except ObjectDoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [("core", "0053_auto_20200325_1556")]

    operations = [
        migrations.RunPython(
            migrate_wald_answers, reverse_code=migrations.RunPython.noop
        )
    ]
