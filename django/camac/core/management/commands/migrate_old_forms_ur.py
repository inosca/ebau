from caluma.caluma_form.models import Answer, DynamicOption, Question
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.caluma.extensions.data_sources import form_mapping_by_koor
from camac.instance.models import Form, Instance

FORM_ID_MAPPING = {
    # Reklame
    249: 121,
    # Cantonal territory usage
    291: 247,
    # Mitbericht Kanton
    42: 300,
    43: 300,
    45: 300,
    46: 300,
    161: 300,
    181: 300,
    201: 300,
    221: 300,
    222: 300,
    223: 300,
    224: 300,
    225: 300,
    241: 300,
    242: 300,
    243: 300,
    245: 300,
    246: 300,
    248: 300,
    251: 300,
    252: 300,
    253: 300,
    254: 300,
    255: 300,
    256: 300,
    257: 300,
    258: 300,
    259: 300,
    260: 300,
    286: 300,
    287: 300,
    288: 300,
    289: 300,
    # Mitbericht Bundesstelle
    244: 292,
    250: 292,
    # Meldung Vorhaben
    295: 290,
}

FORM_TYPE_MAPPING = {
    247: "form-type-veranstaltungsgesuch",
    121: "form-type-commercial-permit",
    300: "form-type-mitbericht-kanton",
    292: "form-type-mitbericht-bundesstelle",
    290: "form-type-project-announcement",
}

ANSWER_MITBERICHT_BUND_MAPPING = {
    244: "mbv-bund-type-pgv-eisenbahn",
    250: "mbv-bund-type-pgv-seilbahn",
}

values = list(form_mapping_by_koor.values())
flat = [item for sublist in values for item in sublist]


class Command(BaseCommand):
    help = """Migrate the old forms to new ones."""

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        instances_with_old_forms = Instance.objects.filter(
            form_id__in=list(FORM_ID_MAPPING.keys())
        )

        self.stdout.write("INSTANCE_ID, OLD_FORM_ID, NEW_FORM_ID")
        for instance in instances_with_old_forms:
            new_form = Form.objects.get(pk=FORM_ID_MAPPING[instance.form.pk])
            old_form = instance.form
            instance.form = new_form
            instance.save()
            self.stdout.write(f"{instance.instance_id}, {old_form.pk}, {new_form.pk}")

            if new_form.pk == 300:  # Mitberichtsverfahren Kanton
                special_cases = {
                    43: 42,  # Int. Genehmigungsverf. -> Int. Mitbericht
                }
                value = special_cases.get(old_form.form_id, old_form.form_id)
                _, created = Answer.objects.get_or_create(
                    document=instance.case.document,
                    question=Question.objects.get(slug="mbv-type"),
                    defaults={"value": str(value)},
                )

                if created:
                    pair = next(pair for pair in flat if pair[0] == value)
                    DynamicOption.objects.get_or_create(
                        document=instance.case.document,
                        question=Question.objects.get(slug="mbv-type"),
                        slug=str(value),
                        defaults={"label": pair[1]},
                    )

            elif new_form.pk == 292:  # Mitberichtsverfahren Bundesstelle
                Answer.objects.get_or_create(
                    document=instance.case.document,
                    question=Question.objects.get(slug="mbv-bund-type"),
                    defaults={
                        "value": ANSWER_MITBERICHT_BUND_MAPPING[old_form.form_id]
                    },
                )

            try:
                answer = instance.case.document.answers.filter(
                    question_id="form-type"
                ).first()

                answer.value = FORM_TYPE_MAPPING[new_form.pk]

                answer.save()
            except AttributeError:
                Answer.objects.create(
                    value=FORM_TYPE_MAPPING[new_form.pk],
                    document=instance.case.document,
                    question=Question.objects.get(slug="form-type"),
                )

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
