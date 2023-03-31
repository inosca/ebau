from django.conf import settings

from camac.notification import utils as notification_utils


def notify_receivers(message, context):
    # Currently, we do not send notification to internal
    # services.
    if "APPLICANT" in message.topic.involved_entities:
        _notify_applicants(message, context)


def _notify_applicants(message, context):

    instance = message.topic.instance

    notification_utils.send_mail(
        slug=settings.APPLICATION["COMMUNICATIONS"]["template_slug"],
        context=context,
        recipient_types=["email_list"],
        email_list=",".join(
            [applicant.email for applicant in instance.involved_applicants.all()]
        ),
        instance={"id": instance.pk, "type": "instances"},
    )
