from caluma.caluma_form.models import Document, Question
from caluma.caluma_user.models import AnonymousUser
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm


class Command(BaseCommand):
    help = """Migrate missing caluma default answers."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit", dest="commit", action="store_true", default=False
        )
        parser.add_argument(
            "--question",
            dest="question",
            type=str,
            default=None,
            help="Migrate only the specified question (by pk)",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()
        self.verbosity = options.get("verbosity", 1)
        question_slug = options.get("question")
        self.anonymous_user = AnonymousUser()

        # Query all questions with a default answer, optionally filter by slug.
        questions = Question.objects.filter(
            default_answer__isnull=False,
            is_archived=False,
        )
        if question_slug:
            questions = questions.filter(pk=question_slug)

        # Print summary of questions to be processed.
        print(f"Found {questions.count()} questions with a default answer:")
        for question in questions:
            print(f" - {question.pk}")

        print("\nStarting migration of default answers...")
        count = 0
        for question in tqdm(questions):
            count += self.migrate_question(question)

        if options["commit"]:
            print(f"Committing changes to database, {count} answers migrated")
            transaction.savepoint_commit(sid)
        else:
            print(f"{count} answers would have been migrated")
            print(
                "Not committing changes to database. Run again with --commit to actually apply changes"
            )
            transaction.savepoint_rollback(sid)

        print("\nMigration of default answers completed.")

    def migrate_question(self, question: Question) -> int:
        count = 0
        self.print_verbose(
            f"Starting migration of default answers for question {question.pk}"
        )

        forms = question.forms.all()
        self.print_verbose(f" - Found {forms.count()} forms for question")

        documents_missing_answer = (
            # Limit to documents of the relevant forms.
            Document.objects.filter(form__in=forms)
            # Exclude documents that already have an answer for this question.
            .exclude(answers__question=question)
        )
        self.print_verbose(
            f"   - Found {documents_missing_answer.count()} documents missing answer for question"
        )

        for document in documents_missing_answer.iterator(chunk_size=250):
            # use document creation/modification user/group if available.
            user = (
                AnonymousUser(
                    username=document.created_by_user or document.modified_by_user,
                    group=document.created_by_group or document.modified_by_group,
                )
                if (
                    document.created_by_user
                    or document.modified_by_user
                    or document.created_by_group
                    or document.modified_by_group
                )
                else self.anonymous_user
            )
            question.default_answer.copy(
                to_document=document,
                document_family=document.family,
                user=user,
            )
            count += 1

        return count

    def print_verbose(self, message) -> None:
        if self.verbosity >= 2:
            print(message)
