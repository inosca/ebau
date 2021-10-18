import re

from caluma.caluma_form.models import Answer
from django.core.management.base import BaseCommand

ANSWERS_FOR_PARTERRE = [
    "EG",
    "EG ",
    "Parterre",
    "Parterre inkl. Hochparterre",
    "Erdgeschoss",
]

ANSWERS_FOR_OBERGESCHOSS = [
    "OG",
    "DG",
    "1. Stockwerk",
    "2. Stockwerk",
    "1. Obergeschoss",
    "2. Obergeschoss",
    "1. Stock",
    "2. Stock",
    "1.OG",
    "2.OG",
    "3.OG",
    "4.OG",
    "5.OG",
    "1. OG",
    "2. OG",
    "2. OG / DG",
    "Ebene 1",
    "Ebene 2 + 3",
    "2.  OG",
    "1",
    "2",
    "3",
    "4",
    "1.",
    "2.",
    "3.",
    "4.",
]

ANSWERS_FOR_UNTERGESCHOSS = [
    "UG",
    "KG",
]


class Command(BaseCommand):
    help = """Migrate the answers in the 'stockwerk' questions."""

    def handle(self, *args, **kwargs):
        answers = Answer.objects.filter(question_id="stockwerk")

        self.assign_the_floor(answers)

    def assign_the_floor(self, answers):
        for answer in answers:

            if answer.value in ANSWERS_FOR_PARTERRE:
                Answer.objects.create(
                    question_id="stockwerktyp",
                    value="stockwerktyp-parterre",
                    document=answer.document,
                )
                self.assign_floor_number(answer)
                self.stdout.write(
                    "A new answer with the value 'stockwerktyp-parterre' was created."
                )
            elif answer.value in ANSWERS_FOR_OBERGESCHOSS:
                if sum(char.isdigit() for char in answer.value) >= 2:
                    Answer.objects.create(
                        question_id="weitere-angaben-zum-stockwerk",
                        value=answer.value,
                        document=answer.document,
                    )
                    self.stdout.write(
                        f"A new answer with the value '{answer.value}' was created for the question 'weitere-angaben-zum-stockwerk'."
                    )
                    continue

                Answer.objects.create(
                    question_id="stockwerktyp",
                    value="stockwerktyp-obergeschoss",
                    document=answer.document,
                )

                self.assign_floor_number(answer)
                self.stdout.write(
                    "A new answer with the value 'stockwerktyp-obergeschoss' was created."
                )
            elif answer.value in ANSWERS_FOR_UNTERGESCHOSS:
                Answer.objects.create(
                    question_id="stockwerktyp",
                    value="stockwerktyp-untergeschoss",
                    document=answer.document,
                )
                self.stdout.write(
                    "A new answer with the value 'stockwerktyp-untergeschoss' was created."
                )
            else:
                Answer.objects.create(
                    question_id="weitere-angaben-zum-stockwerk",
                    value=answer.value,
                    document=answer.document,
                )
                self.stdout.write(
                    f"A new answer with the value '{answer.value}' was created for the question 'weitere-angaben-zum-stockwerk'."
                )

    def assign_floor_number(self, answer):
        number = list(map(int, re.findall(r"\d+", answer.value)))
        value = ", ".join(str(n) for n in number)
        if number:
            Answer.objects.create(
                question_id="stockwerknummer",
                value=value,
                document=answer.document,
            )
            self.stdout.write(
                f"A new answer with the value '{value}' was created for the question 'stockwerknummer'."
            )
