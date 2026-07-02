from __future__ import annotations

from typing import TYPE_CHECKING, Any

from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Document, Question
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.db import models, transaction
from django.utils.timezone import now
from rest_framework.exceptions import PermissionDenied, ValidationError
from uuid_extensions import uuid7

from camac.applicants.utils import get_applicants_requiring_confirmation
from camac.permissions.api import PermissionManager

if TYPE_CHECKING:
    from rest_framework.request import Request

    from camac.instance.models import Instance
    from camac.user.models import User


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


class ApplicantConfirmationQuerySet(models.QuerySet["ApplicantConfirmation"]):
    def for_request(self, request: Request) -> ApplicantConfirmationQuerySet:
        """Return confirmations visible for a request."""

        return self.filter(
            PermissionManager.from_request(request).static_permission_expr(
                "applicant-confirmation-read", instance_prefix="round__instance"
            )
        )

    def only_pending(self) -> ApplicantConfirmationQuerySet:
        """Return pending confirmations."""

        return self.filter(status=ApplicantConfirmation.Status.PENDING)

    def only_confirmed(self) -> ApplicantConfirmationQuerySet:
        """Return confirmed confirmations."""

        return self.filter(status=ApplicantConfirmation.Status.CONFIRMED)

    def invalidate_confirmed(self) -> ApplicantConfirmationQuerySet:
        """Update status of confirmed confirmations to invalidated."""

        qs = self.only_confirmed()
        qs.update(status=ApplicantConfirmation.Status.INVALIDATED, closed_at=now())
        return qs

    def cancel_pending(self) -> ApplicantConfirmationQuerySet:
        """Update status of pending confirmations to canceled."""

        qs = self.only_pending()
        qs.update(status=ApplicantConfirmation.Status.CANCELED, closed_at=now())
        return qs

    def has_pending(self) -> bool:
        """Return `True` if the queryset contains pending confirmations."""

        return self.only_pending().exists()


class ApplicantConfirmation(models.Model):
    """Represents a single applicant's confirmation within a confirmation round.

    Each applicant can have at most one confirmation per round. A confirmation
    records whether the applicant has confirmed during that round and which
    source questions (e.g. applicant, landowner etc.) caused the confirmation to
    be required.
    """

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELED = "canceled", "Canceled"
        INVALIDATED = "invalidated", "Invalidated"

    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    applicant = models.ForeignKey(
        "applicants.Applicant", on_delete=models.CASCADE, related_name="+"
    )
    source_questions = models.ManyToManyField("caluma_form.Question", related_name="+")
    round = models.ForeignKey(
        "applicants.ApplicantConfirmationRound",
        on_delete=models.CASCADE,
        related_name="confirmations",
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(blank=True, null=True)

    objects: ApplicantConfirmationQuerySet = ApplicantConfirmationQuerySet.as_manager()

    @property
    def user(self) -> User | None:
        """User of the applicant confirmation.

        This is derived from the related applicant object and may be `None` if
        the applicant is not related to a registered user yet.
        """

        return self.applicant.invitee

    @property
    def roles(self) -> list[str]:
        """Roles of the applicant confirmation.

        This contains domain logic information that tells which roles (e.g.
        landowner, project author etc.) the related applicant has for the
        related instance. This has nothing to do with anything
        permission-related but is informational only.

        The roles are derived from the caluma table questions that we're used to
        determine the applicants that need to confirm.

        WARNING: Please make sure to prefetch the source questions if you're
        using this property.
        """

        return [question.label.translate() for question in self.source_questions.all()]

    @property
    def display_name(self) -> str:
        """Display name of the applicant confirmation.

        This will either return the related users full name or the invited
        applicant email address if the user is not registered yet.
        """

        return self.user.get_full_name() if self.user else self.applicant.email

    @transaction.atomic
    def confirm(self, request: Request) -> ApplicantConfirmation:
        """Confirm an applicant confirmation.

        If it is the last pending confirmation the related round will be
        completed.
        """

        PermissionManager.from_request(request).require_all(
            self.round.instance, "applicant-confirmation-confirm"
        )

        if self.user is None or request.user != self.user:
            raise PermissionDenied()

        if self.status != self.Status.PENDING:
            raise ValidationError(
                "Only pending applicant confirmations can be confirmed."
            )

        if self.round.status != ApplicantConfirmationRound.Status.RUNNING:
            raise ValidationError(
                "Applicant confirmations can only be confirmed while the round is running."
            )

        self.status = self.Status.CONFIRMED
        self.closed_at = now()
        self.save(update_fields=["status", "closed_at"])

        if self.round.confirmations.has_pending():
            # If we still have pending confirmations in the same round, we don't
            # update the round at all
            return self

        # If this was the last pending confirmation of the round, we update the
        # rounds status
        self.round.status = ApplicantConfirmationRound.Status.COMPLETED
        self.round.closed_at = now()
        self.round.save(update_fields=["status", "closed_at"])

        # Save caluma answer to trigger is_hidden of submit form
        save_answer(
            question=Question.objects.get(pk=settings.APPLICANTS.confirmation_question),
            document=self.round.document,
            user=request.caluma_info.context.user,
            value=settings.APPLICANTS.confirmation_answer,
        )

        return self

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["applicant", "round"],
                name="unique_applicant_confirmation_per_round",
            )
        ]


class ApplicantConfirmationRoundQuerySet(models.QuerySet["ApplicantConfirmationRound"]):
    def for_request(self, request: Request) -> ApplicantConfirmationRoundQuerySet:
        """Return confirmation rounds visible for a request."""

        return self.filter(
            PermissionManager.from_request(request).static_permission_expr(
                "applicant-confirmation-read", instance_prefix="instance"
            )
        )

    def for_document(self, document: Document) -> ApplicantConfirmationRoundQuerySet:
        """Return confirmation rounds for a document."""

        return self.filter(document=document)

    def only_active(self) -> ApplicantConfirmationRoundQuerySet:
        """Return active (running or completed) confirmation rounds."""

        return self.filter(
            status__in=[
                ApplicantConfirmationRound.Status.RUNNING,
                ApplicantConfirmationRound.Status.COMPLETED,
            ]
        )

    def has_active(self) -> bool:
        """Return `True` if the queryset contains active (running or completed) confirmation rounds."""

        return self.only_active().exists()


class ApplicantConfirmationRoundManager(models.Manager["ApplicantConfirmationRound"]):
    @transaction.atomic
    def start_for_document(
        self, document: Document, request: Request
    ) -> ApplicantConfirmationRound:
        """Start a new applicant confirmation round for a document.

        This will determine the step depending on the document that was passed
        in and make sure that there are no currently running rounds for this
        document yet.

        It will also create the individual applicant confirmations for each
        applicant that was identified through the personal-table source
        questions of the main form.
        """

        if hasattr(document, "case"):
            # The passed document is the main document of a case therefore we're
            # creating a confirmation round for the submit step.
            step = ApplicantConfirmationRound.Step.SUBMIT
            instance = document.case.instance

        elif document.work_item.task_id == settings.ADDITIONAL_DEMAND["FILL_TASK"]:
            # The passed document belongs to a fill-additional-demand work item.
            # We're creating a confirmation round for an additional demand.
            step = ApplicantConfirmationRound.Step.ADDITIONAL_DEMAND
            instance = document.work_item.case.family.instance

        else:
            raise ImproperlyConfigured(
                "Applicant confirmation rounds can only be created for the "
                "main document or additional demands. You passed in a document "
                f"of the form {document.form_id}."
            )

        PermissionManager.from_request(request).require_all(
            instance, "applicant-confirmation-start"
        )

        if ApplicantConfirmationRound.objects.for_document(document).has_active():
            raise ValidationError(
                "There is already an active applicant confirmation round for this document"
            )

        applicants = get_applicants_requiring_confirmation(instance)

        if not applicants:
            raise ValidationError(
                "Can't create an applicant confirmation round without any individual confirmations."
            )

        round = ApplicantConfirmationRound.objects.create(
            document=document,
            instance=instance,
            step=step,
        )

        for applicant, questions in applicants:
            confirmation = ApplicantConfirmation.objects.create(
                round=round,
                applicant=applicant,
            )
            confirmation.source_questions.set(questions)

        return round


class ApplicantConfirmationRound(models.Model):
    """Represents a round of collecting confirmations from applicants.

    A round belongs to a document and instance, is associated with a step that
    is derived from the document, and groups the individual applicant
    confirmations created for that point in the process.

    Rounds are repeatable. A round may be canceled (while running), or
    invalidated (after completion). The round will be automatically completed if
    the last individual applicant confirmation is confirmed.
    """

    class Step(models.TextChoices):
        SUBMIT = "submit", "Submit"
        ADDITIONAL_DEMAND = "additional_demand", "Additional demand"

    class Status(models.TextChoices):
        RUNNING = "running", "Running"
        COMPLETED = "completed", "Completed"
        CANCELED = "canceled", "Canceled"
        INVALIDATED = "invalidated", "Invalidated"

    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    document = models.ForeignKey(
        "caluma_form.Document", on_delete=models.CASCADE, related_name="+"
    )
    instance = models.ForeignKey(
        "instance.Instance",
        on_delete=models.CASCADE,
        related_name="confirmation_rounds",
    )
    step = models.CharField(max_length=32, choices=Step.choices)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.RUNNING, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(blank=True, null=True)

    objects: ApplicantConfirmationRoundQuerySet = (
        ApplicantConfirmationRoundManager.from_queryset(
            ApplicantConfirmationRoundQuerySet
        )()
    )

    @transaction.atomic
    def invalidate(self, request: Request) -> ApplicantConfirmationRound:
        """Invalidate a confirmation round.

        A confirmation round can only be invalidated if it has already been
        completed.

        This will also update the status of the individual applicant
        confirmations to invalidated.
        """

        PermissionManager.from_request(request).require_all(
            self.instance, "applicant-confirmation-invalidate"
        )

        if self.status != self.Status.COMPLETED:
            raise ValidationError(
                "Only completed applicant confirmation rounds can be invalidated."
            )

        self.confirmations.invalidate_confirmed()
        self.status = self.Status.INVALIDATED
        self.closed_at = now()
        self.save(update_fields=["status", "closed_at"])

        # Reset caluma answer to trigger is_hidden of submit form
        save_answer(
            question=Question.objects.get(pk=settings.APPLICANTS.confirmation_question),
            document=self.document,
            user=request.caluma_info.context.user,
            value=[],
        )

        return self

    @transaction.atomic
    def cancel(self, request: Request) -> ApplicantConfirmation:
        """Cancel a confirmation round.

        A confirmation round can only be canceled if it is still running.

        This will change the individual applicant confirmations status as
        follows:
        - pending confirmations are canceled
        - confirmed confirmations are invalidated
        """

        PermissionManager.from_request(request).require_all(
            self.instance, "applicant-confirmation-cancel"
        )

        if self.status != self.Status.RUNNING:
            raise ValidationError(
                "Only running applicant confirmation rounds can be canceled."
            )

        self.confirmations.invalidate_confirmed()
        self.confirmations.cancel_pending()
        self.status = self.Status.CANCELED
        self.closed_at = now()
        self.save(update_fields=["status", "closed_at"])

        return self

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["document"],
                condition=models.Q(status__in=["running", "completed"]),
                name="unique_running_confirmation_round_per_document",
            )
        ]
