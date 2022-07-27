from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Answer, Document, Question
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Exists, OuterRef
from tqdm import tqdm


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        question = Question.objects.get(pk="bab-landwirtschaft-nutzung")
        documents = Document.objects.filter(form_id="bab-form").exclude(
            Exists(Answer.objects.filter(question=question, document_id=OuterRef("pk")))
        )

        for document in tqdm(documents):
            save_answer(
                document=document,
                question=question,
                value="bab-landwirtschaft-nutzung-nein",
            )
