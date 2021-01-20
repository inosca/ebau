from django.core.management.base import BaseCommand
from django.db import transaction

from camac.applicants.models import Applicant
from camac.user.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)
        parser.add_argument(
            "--verbose", dest="verbose", action="store_true", default=False
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        self.verbose = options.get("verbose", False)

        self.remove_duplicates()
        self.assign()
        self.remove_deactivated()

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def assign(self):
        count = 0

        for applicant in Applicant.objects.filter(invitee__isnull=True):
            user = User.objects.filter(email=applicant.email).first()

            if user:
                if self.verbose:
                    self.stdout.write(
                        f"Instance {applicant.instance_id} - assigned matching applicant {applicant.email}"
                    )

                applicant.invitee = user
                applicant.save()
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Assigned {count} matching applicants"))

    def remove_duplicates(self):
        count = 0

        for applicant in Applicant.objects.filter(invitee__isnull=True):
            user = User.objects.filter(email=applicant.email).first()

            has_email_duplicates = (
                applicant.instance.involved_applicants.exclude(pk=applicant.pk)
                .filter(email=applicant.email)
                .exists()
            )
            has_user_duplicates = (
                applicant.instance.involved_applicants.exclude(pk=applicant.pk)
                .filter(invitee=user)
                .exists()
                if user
                else False
            )

            if has_email_duplicates or has_user_duplicates:
                if self.verbose:
                    self.stdout.write(
                        f"Instance {applicant.instance_id} - deleted duplicated applicant {applicant.email}"
                    )
                applicant.delete()
                count += 1

        self.stdout.write(self.style.WARNING(f"Deleted {count} duplicated applicants"))

    def remove_deactivated(self):
        deactivated = Applicant.objects.filter(invitee__disabled=1)
        count = deactivated.count()
        deactivated.delete()

        self.stdout.write(self.style.WARNING(f"Deleted {count} deactivated applicants"))
