from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Exists, OuterRef
from tqdm import tqdm

from camac.applicants.models import ROLE_CHOICES, Applicant
from camac.notification.utils import send_mail_without_request
from camac.permissions.events.core import Trigger
from camac.permissions.models import InstanceACL
from camac.user.models import User


class Command(BaseCommand):
    help = """Create custom work item for AfU service"""

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit", dest="commit", action="store_true", default=False
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if settings.APPLICATION_NAME != "kt_so":
            raise Exception("Only for Kt SO")

        if not settings.ENABLE_TOKEN_EXCHANGE:
            # Without it, portal and internal users are indistinguishable and
            # the migration below would delete every project owner applicant.
            raise Exception("Only with token exchange enabled")

        # Grant the ACLs of applicants that never got one

        applicants_missing_acl = (
            Applicant.objects.filter(invitee__isnull=False)
            .annotate(
                acls_exists=Exists(
                    InstanceACL.objects.filter(
                        user=OuterRef("invitee"), instance=OuterRef("instance")
                    )
                )
            )
            .exclude(acls_exists=True)
        )

        sid = transaction.savepoint()
        for applicant in tqdm(applicants_missing_acl, desc="Creating permissions"):
            Trigger.applicant_added(None, applicant.instance, applicant)

        # Fix applicants where we created an entry for an internal user instead of the
        # portal user with the same email.
        system_user = User.objects.get(username=settings.APPLICATION.get("SYSTEM_USER"))

        applicants_linked_to_wrong_user = Applicant.objects.filter(
            role=ROLE_CHOICES.PROJECT_OWNER,
            invitee__in=User.objects.internal_users(),
        )

        for old_applicant in tqdm(
            applicants_linked_to_wrong_user,
            desc="Moving permissions from internal user to portal user",
        ):
            instance = old_applicant.instance
            email = old_applicant.email.lower()
            internal_user = old_applicant.invitee

            portal_user = User.objects.only_active().portal_users().get_by_email(email)

            new_applicant, created = Applicant.objects.get_or_create(
                instance=instance,
                invitee=portal_user,
                email=email,
                defaults={
                    "role": ROLE_CHOICES.PROJECT_OWNER,
                    "user": system_user,
                },
            )

            if created:
                Trigger.applicant_added(None, instance, new_applicant)
            elif new_applicant.role != ROLE_CHOICES.PROJECT_OWNER:
                # The portal user was already an applicant, they only need the
                # role. Their ACL was granted by the loop above.
                new_applicant.role = ROLE_CHOICES.PROJECT_OWNER
                new_applicant.save()

            Trigger.applicant_removed(None, instance, old_applicant)
            old_applicant.delete()

            if portal_user:
                tqdm.write(
                    f"Moved Applicant from user {internal_user.username}:{internal_user.email} to {portal_user.username}:{portal_user.email}. Instance: {instance.pk}."
                )

            else:
                tqdm.write(
                    f"Moved Applicant from user {internal_user.username}:{internal_user.email} to {email} as no existing portal user was found for this email. Instance: {instance.pk}."
                )

                # These applicants originally received the "EXISTING" invitation
                # telling them to log in with an account they don't have. Send
                # the "NEW" invitation so they can register.
                if template := settings.APPLICATION["NOTIFICATIONS"]["APPLICANT"][
                    "NEW"
                ]:
                    # Mails can't be rolled back, so only send them on a real run.
                    if options["commit"]:
                        send_mail_without_request(
                            template,
                            recipient_types=["email_list"],
                            email_list=email,
                            instance={"id": instance.pk, "type": "instances"},
                        )
                        tqdm.write(f"Sent Mail to {email} for new registration.")
                    else:
                        tqdm.write(f"Would send Mail to {email} for new registration.")

        if options["commit"]:
            transaction.savepoint_commit(sid)
        else:
            transaction.savepoint_rollback(sid)
