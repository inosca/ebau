from celery import shared_task
from django.conf import settings

from camac.agsmartservice.client import AGSmartServiceClient

SUBMITTED = "SUBMITTED"
IN_PROGRESS = "IN_PROGRESS"
DONE = "DONE"


@shared_task()
def submit_procedure_task(instance_id, title, assignee_id):
    payload = {
        "title": title,
        "assignment": {
            "id": assignee_id,
            "roles": None,
        },
        "status": {
            "id": SUBMITTED,
            "details": {
                "id": "submitted",
                "name": "Eingereicht",
                "text": "Ihr Dossier wurde erfolgreich eingereicht.",
            },
            "action": {
                "required": False,
                "deadline": None,
            },
        },
        "actions": [
            {
                "type": "openUrl",
                "title": "Zu eBau",
                "url": settings.PUBLIC_INSTANCE_URL_TEMPLATE.format(
                    instance_id=instance_id
                ),
            }
        ],
    }

    AGSmartServiceClient.put_procedure(instance_id, payload)


@shared_task()
def complete_preliminary_check_task(instance_id, title):
    payload = {
        "title": title,
        "status": {
            "id": IN_PROGRESS,
            "details": {
                "id": "decided",
                "name": "Im Verfahren",
                "text": "Ihr Dossier befindet sich im Verfahren.",
            },
            "action": {
                "required": False,
                "deadline": None,
            },
        },
        "actions": [],
    }

    AGSmartServiceClient.put_procedure(instance_id, payload)


@shared_task()
def start_construction_monitoring_task(instance_id, title):
    payload = {
        "title": title,
        "status": {
            "id": IN_PROGRESS,
            "details": {
                "id": "decided",
                "name": "In Baubegleitung",
                "text": "Ihr Dossier befindet sich in der Baubegleitung.",
            },
            "action": {
                "required": False,
                "deadline": None,
            },
        },
        "actions": [],
    }

    AGSmartServiceClient.put_procedure(instance_id, payload)


@shared_task()
def complete_procedure_task(instance_id, title):
    payload = {
        "title": title,
        "status": {
            "id": DONE,
            "details": {
                "id": "done",
                "name": "Abgeschlossen",
                "text": "Ihr Dossier ist abgeschlossen.",
            },
            "action": {
                "required": False,
                "deadline": None,
            },
        },
        "actions": [],
    }

    AGSmartServiceClient.put_procedure(instance_id, payload)


@shared_task()
def delete_procedure_task(instance_id):
    AGSmartServiceClient.delete_procedure(instance_id)
