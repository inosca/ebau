from logging import getLogger

import caluma.caluma_form.models as caluma_form_models
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.constants import kt_gr as gr_constants

log = getLogger(__name__)

TARGETS = [
    "apsp",
    "sssh",
    "wate",
    "bfgb",
    "wbah",
]
FORMS = [
    "invest",
    "phase1",
    "phase2",
    "teilzahlung",
    "bauabrechnung",
]

FORM_MAPPING = {
    "invest": gr_constants.BAUBEITRAGSWESEN_FORM_INVESTITIONSANMELDUNG,
    "phase1": gr_constants.BAUBEITRAGSWESEN_FORM_PHASE_1,
    "phase2": gr_constants.BAUBEITRAGSWESEN_FORM_PHASE_2,
    "teilzahlung": gr_constants.BAUBEITRAGSWESEN_FORM_TEILZAHLUNGEN,
    "bauabrechnung": gr_constants.BAUBEITRAGSWESEN_FORM_BAUABRECHNUNG,
}


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.verbosity = options.get("verbosity", 1)

        questions = caluma_form_models.Question.objects.filter(pk__startswith="ebbw-")
        for question in questions:
            forms, targets, question_slug = self.parse_question_slug(question)

            output = self.verify_base(forms, targets, question_slug)
            if len(output):
                self.write_output(question, output)
                continue

            output = self.verify_jexl(question, forms, targets)
            if len(output):
                self.write_output(question, output)

    def parse_question_slug(self, question):
        """Split a question slug into form selectors, target selectors and its name."""
        split = question.pk.split("-")
        forms = []
        targets = []
        cursor = 1

        while cursor < len(split) and self.validate_form(split[cursor]):
            if split[cursor] == "default" and forms:
                break

            forms.append(split[cursor])
            cursor += 1

            if forms[-1] == "default":
                break

        while cursor < len(split) and self.validate_target(split[cursor]):
            targets.append(split[cursor])
            cursor += 1

            if targets[-1] == "default":
                break

        question_slug = split[cursor:]

        return forms, targets, question_slug

    def validate_form(self, form_slug):
        return form_slug in FORMS or form_slug == "default"

    def validate_target(self, target_slug):
        return target_slug in TARGETS or target_slug == "default"

    def verify_base(self, forms, targets, question_slug):
        """Validate the question slug format and return validation issues."""
        output = []

        valid_forms = bool(forms) and all(self.validate_form(form) for form in forms)
        valid_targets = bool(targets) and all(
            self.validate_target(target) for target in targets
        )

        if not valid_forms or not valid_targets:
            correct_forms = forms if valid_forms else ["default"]
            correct_targets = targets if valid_targets else ["default"]
            correct_slug = [*correct_forms, *correct_targets, *question_slug]

            output.append(f"rename question to ebbw-{'-'.join(correct_slug)}")

        return output

    def verify_jexl(self, question, forms, targets):
        """Validate question is_hidden JEXL for all forms and targets."""
        output = []
        is_hidden = str(question.is_hidden)

        for form in forms:
            if form == "default":
                if '"baubeitragswesen" in info.root.form' not in is_hidden:
                    output.append(
                        'default form must check for "baubeitragswesen" '
                        f"in is_hidden ({is_hidden})"
                    )
                continue

            target_form = FORM_MAPPING[form]
            if (
                f'"{target_form}" in info.root.form' not in is_hidden
                and f'"{target_form}" == info.root.form' not in is_hidden
            ):
                output.append(
                    f"{form} form must check for {target_form} in is_hidden ({is_hidden})"
                )

        for target in targets:
            if target == "default":
                continue

            target_check = (
                f'"ebbw-default-default-art-des-gesuchs"|answer == "{target}"'
            )
            if target_check not in is_hidden:
                output.append(
                    f"{target} target must check for {target_check} "
                    f"in is_hidden ({is_hidden})"
                )

        return output

    def write_output(self, question, output):
        log.warning(f"## {question.pk} ##")
        for line in output:
            log.warning(f"  - {line}")
