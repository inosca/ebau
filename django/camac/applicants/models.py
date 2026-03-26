from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from camac.instance.models import Instance


class ApplicantManager(models.Manager):
    def create_or_update_project_owners_for_instance(
        self, instance: Instance, applicants_from_form: list[Any]
    ) -> None:
        """Assign the applicants as well as their deputy from the form as project owner.

        This is required for the digital signature process since legally, not everyone can
        accept a legal document which is deliviered digitally. In SO, the person who is legally
        allowed to receive documents is the applicant and their deputy from the form.

        There may be more than one applicant, they will all receive the new project_owner role.
        """

        emails = []
        for applicant in applicants_from_form:
            if email := applicant.get("email"):
                emails.append(email.lower())

            if representative_email := applicant.get("representative_email"):
                emails.append(representative_email.lower())

        existing_applicants = self.filter(instance=instance, email__in=emails)

        for email in set(emails):
            if existing := existing_applicants.filter(email=email).first():
                if not existing.role == ROLE_CHOICES.PROJECT_OWNER:
                    existing.role = ROLE_CHOICES.PROJECT_OWNER
                    existing.save()
            else:
                User = get_user_model()
                system_user = User.objects.get(
                    username=settings.APPLICATION.get("SYSTEM_USER")
                )
                applicant = self.create(
                    role=ROLE_CHOICES.PROJECT_OWNER,
                    email=email.lower(),
                    invitee=User.objects.filter(email=email, disabled=False).first(),
                    instance=instance,
                    user=system_user,
                )

                notification_template = settings.APPLICATION["NOTIFICATIONS"][
                    "APPLICANT"
                ]["EXISTING" if applicant.invitee else "NEW"]
                if notification_template:
                    from camac.notification.utils import send_mail_without_request

                    send_mail_without_request(
                        notification_template,
                        recipient_types=["email_list"],
                        email_list=applicant.email,
                        instance={"id": instance.pk, "type": "instances"},
                    )


class ROLE_CHOICES(models.TextChoices):
    PROJECT_OWNER = "PROJECT_OWNER", "Project owner"
    ADMIN = "ADMIN", "Admin"
    EDITOR = "EDITOR", "Editor"
    READ_ONLY = "READ_ONLY", "Read only"


class Applicant(models.Model):
    instance = models.ForeignKey(
        "instance.Instance",
        models.CASCADE,
        db_column="INSTANCE_ID",
        # NOTE: The "involved_" prefix is required because the instance views annotate
        # "applicants". And we did not wanted to break backwards compatibility
        related_name="involved_applicants",
    )
    user = models.ForeignKey(
        "user.User", models.DO_NOTHING, db_column="USER_ID", related_name="+"
    )
    invitee = models.ForeignKey(
        "user.User",
        models.DO_NOTHING,
        db_column="APPLICANT_USER_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    created = models.DateTimeField(db_column="CREATED", auto_now=True)
    email = models.EmailField(db_collation="case_insensitive", blank=True)
    username = models.CharField(db_collation="case_insensitive", blank=True)
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES.choices,
        default=ROLE_CHOICES.ADMIN.value,
    )

    objects = ApplicantManager()

    class Meta:
        managed = True
        db_table = "APPLICANTS"
        unique_together = (("instance", "invitee"),)
