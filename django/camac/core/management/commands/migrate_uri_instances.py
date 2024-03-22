from datetime import timedelta

from caluma.caluma_user.models import AnonymousUser
from caluma.caluma_workflow.models import Task, WorkItem
from caluma.caluma_workflow.utils import get_jexl_groups
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from tqdm import tqdm

from camac.constants import kt_uri as uri_constants
from camac.core.models import InstanceService
from camac.instance.models import Instance
from camac.user.models import Group, Location, Service

GBB_ROLE_ID = 6

KOOR_NP_SERVICE = Service.objects.get(pk=uri_constants.KOOR_NP_SERVICE_ID)
KOOR_SD_SERVICE = Service.objects.get(pk=uri_constants.KOOR_SD_SERVICE_ID)
KOOR_BD_SERVICE = Service.objects.get(pk=uri_constants.KOOR_BD_SERVICE_ID)
KOOR_AFE_SERVICE = Service.objects.get(pk=uri_constants.KOOR_AFE_SERVICE_ID)
KOOR_AFJ_SERVICE = Service.objects.get(pk=uri_constants.KOOR_AFJ_SERVICE_ID)

WORK_ITEM_TO_WORKFLOW_ENTRY_MAPPING = {
    "complete-check": 1,  # Prüfung durch gemeinde
    "archive": 62,  # Archiviert
}

WORK_ITEMS_FOR_INSTANCE_IN_PROGRESS = [
    ("submit", WorkItem.STATUS_COMPLETED, {"applicant": True}),
    ("create-manual-workitems", WorkItem.STATUS_READY, {}),
    ("instance-management", WorkItem.STATUS_READY, {}),
    (
        "complete-check",
        WorkItem.STATUS_COMPLETED,
        {},
    ),
]

INSTANCE_STATUS_MAPPING = {
    "comm": [  # "name": "comm", "description": "Bearbeitung Leitbehörde"
        *WORK_ITEMS_FOR_INSTANCE_IN_PROGRESS
    ],
    "ext": [  # "name": "ext", "description": "Bearbeitung Koordinationsstelle"
        *WORK_ITEMS_FOR_INSTANCE_IN_PROGRESS
    ],
    "circ": [
        *WORK_ITEMS_FOR_INSTANCE_IN_PROGRESS
    ],  # "name": "circ", "description": "In Zirkulation"
    "redac": [  # "name": "redac", "description": "Zirkulation beendet"
        *WORK_ITEMS_FOR_INSTANCE_IN_PROGRESS,
        ("decision", WorkItem.STATUS_READY, {}),
    ],
    "done": [  # "name": "done", "description": "Zurück bei Gemeinde"
        *WORK_ITEMS_FOR_INSTANCE_IN_PROGRESS,
        ("decision", WorkItem.STATUS_READY, {}),
    ],
    "arch": [  # "name": "arch", "description": "Archiviert"
        *WORK_ITEMS_FOR_INSTANCE_IN_PROGRESS,
        ("decision", WorkItem.STATUS_COMPLETED, {}),
        ("construction-supervision", WorkItem.STATUS_COMPLETED, {}),
        ("archive", WorkItem.STATUS_COMPLETED, {}),
    ],
    "del": [],  # "name": "del", "description": "Gelöscht"
    "new": [  # "name": "new", "description": "Neu Erstellt"
        ("submit", WorkItem.STATUS_READY, {"applicant": True}),
    ],
    "nfd": [  # "name": "nfd", "description": "Nachforderung Dokumente"
        *WORK_ITEMS_FOR_INSTANCE_IN_PROGRESS
    ],
    "subm": [  # "name": "subm", "description": "Eingereicht bei Gemeinde"
        ("submit", WorkItem.STATUS_COMPLETED, {}),
        ("create-manual-workitems", WorkItem.STATUS_READY, {}),
        ("instance-management", WorkItem.STATUS_READY, {}),
        ("complete-check", WorkItem.STATUS_READY, {}),
    ],
    "rejected": [  # "name": "rejected", "description": "Abgelehnt"
        *WORK_ITEMS_FOR_INSTANCE_IN_PROGRESS
    ],
    "ext_gem": [  # "name": "ext_gem", "description": "Dossier bleibt bei Gemeindebaubehörde"
        *WORK_ITEMS_FOR_INSTANCE_IN_PROGRESS
    ],
    "old": [],  # "name": "old", "description": "Archivdossier"
    "control": [  # "name": "control", "description": "Bau- und Einspracheentscheid zugestellt"
        *WORK_ITEMS_FOR_INSTANCE_IN_PROGRESS,
        ("decision", WorkItem.STATUS_COMPLETED, {}),
        ("construction-supervision", WorkItem.STATUS_READY, {}),
    ],
}

SERVICE_LOCATIONS = {}
for location in Location.objects.all():
    responsible_group = Group.objects.filter(
        locations=location, role_id=GBB_ROLE_ID
    ).first()

    SERVICE_LOCATIONS[location.communal_federal_number] = Service.objects.filter(
        groups=responsible_group
    ).first()

ALL_TASKS = list(Task.objects.all())

WORKFLOW_ENTRIES = {
    "PRUEFUNG_DURCH_GEMEINDE": [1],
    "DOSSIER_VOLLSTAENDIG": [14, 43],
    "START_ZIRKULATION": [44],
    "WEITERLEITUNG_AN_KOOR": [16],
    "DOSSIER_ERFASST": [12],
    "DOSSIER_ARCHIVIERT": [62],
    "BAUENTSCHEID": [47],
    "ENDABNAHME": [59],
    "VERFAHREN_ABGESCHLOSSEN": [61],
}


class Command(BaseCommand):
    help = "Kanton Uri: Create a caluma case and work items for every instance"

    def add_arguments(self, parser):
        parser.add_argument(
            "--only-creation-log",
            dest="only_creation_log",
            action="store_true",
            default=False,
        )

    def create_work_item_from_task(  # noqa: C901
        self,
        instance,
        case,
        task_slug,
        meta={},
        child_case=None,
        context={},
        applicant=False,
        status=WorkItem.STATUS_READY,
    ):
        task = next(task for task in ALL_TASKS if task.slug == task_slug)

        if case.work_items.filter(task=task).exists():
            return

        meta = {
            "migrated": True,
            "not-viewed": True,
            "notify-deadline": True,
            "notify-completed": False,
            **meta,
        }

        addressed_groups = get_jexl_groups(
            task.address_groups, task, case, AnonymousUser(), None, context
        )

        if applicant:
            addressed_groups.append("applicant")

        closed_at = None

        def get_workflow_entry(instance, ids):
            return instance.workflowentry_set.filter(workflow_item_id__in=ids).first()

        if task_slug in ["complete-check"]:
            # ! If the "complete-check" is completed we ALWAYS need a closed_at date so the circulation migration can run!
            corresponding_workflow_entry = (
                get_workflow_entry(
                    instance, WORKFLOW_ENTRIES["PRUEFUNG_DURCH_GEMEINDE"]
                )
                or get_workflow_entry(
                    instance, WORKFLOW_ENTRIES["DOSSIER_VOLLSTAENDIG"]
                )
                or get_workflow_entry(instance, WORKFLOW_ENTRIES["START_ZIRKULATION"])
                or get_workflow_entry(
                    instance, WORKFLOW_ENTRIES["WEITERLEITUNG_AN_KOOR"]
                )
                or get_workflow_entry(instance, WORKFLOW_ENTRIES["DOSSIER_ERFASST"])
                or get_workflow_entry(instance, WORKFLOW_ENTRIES["DOSSIER_ARCHIVIERT"])
            )

            closed_at = (
                corresponding_workflow_entry.workflow_date
                if corresponding_workflow_entry
                else timezone.now()
            )
            if not corresponding_workflow_entry:
                status = WorkItem.STATUS_SKIPPED

        if task_slug in ["decision"]:
            # we have to deduce the date of the decision from the expiry of the permit
            if corresponding_workflow_entry := get_workflow_entry(
                instance, WORKFLOW_ENTRIES["BAUENTSCHEID"]
            ):  # "Bau und Einspracheentscheid"
                closed_at = corresponding_workflow_entry.workflow_date

        deadline = None
        if task.lead_time:
            deadline = closed_at or timezone.now() + timedelta(seconds=task.lead_time)

        created_at = timezone.now()
        if task_slug == "construction-supervision":
            if (
                not instance.case.work_items.filter(task__slug="decision").exists()
                and instance.instance_state.name == "arch"
            ):
                # a dossier in the "arch" state might not have a construction-supervision worfklowentry
                return

            if not instance.case.work_items.get(task__slug="decision").closed_at:
                # we have never completed the decision work item (maybe the dossier was archived before that)
                # therefore we need to return early and avoid creating the other workitems
                return

            created_at = instance.case.work_items.get(task__slug="decision").closed_at

            if created_at:
                deadline = created_at + timedelta(
                    days=365 * 1.5
                )  # "construction supervision" is always 1.5 years in uri

            if corresponding_workflow_entry := get_workflow_entry(
                instance,
                [
                    *WORKFLOW_ENTRIES["ENDABNAHME"],
                    *WORKFLOW_ENTRIES["VERFAHREN_ABGESCHLOSSEN"],
                ],
            ):
                closed_at = corresponding_workflow_entry.workflow_date
                status = WorkItem.STATUS_COMPLETED

        work_item = WorkItem.objects.create(
            case=case,
            task=task,
            meta=meta,
            name=task.name,
            status=status or WorkItem.STATUS_READY,
            child_case=child_case,
            deadline=deadline,
            addressed_groups=addressed_groups,
            controlling_groups=get_jexl_groups(
                task.control_groups, task, case, AnonymousUser(), None, context
            ),
        )

        work_item.created_at = created_at if created_at else work_item.created_at
        work_item.closed_at = closed_at if closed_at else work_item.closed_at

        work_item.save()

        return work_item

    def handle(self, *args, **options):  # noqa: C901
        self.verbose = not options["only_creation_log"]

        self.stdout.write("Starting Instance to Caluma Case and WorkItem migration")

        instances = Instance.objects.all()

        WorkItem.objects.filter(
            case__instance__in=instances, meta__migrated=True
        ).delete()

        InstanceService.objects.filter(instance__in=instances).delete()

        for instance in tqdm(instances, mininterval=1, maxinterval=2):
            with transaction.atomic():
                instance_state = instance.instance_state.name

                case = instance.case

                if not case:
                    self.stdout.write(f"⚠️ No case found for: {instance.pk}")
                    continue

                if instance_state not in [
                    "new",
                    "del",
                ]:  # "new" is the only state that doesnt have an InstanceService yet
                    self._create_instance_service_object(instance)

                for (
                    task_slug,
                    work_item_status,
                    options,
                ) in INSTANCE_STATUS_MAPPING[instance_state]:
                    self.create_work_item_from_task(
                        instance, case, task_slug, status=work_item_status, **options
                    )

        self.stdout.write("Created Cases and WorkItems for Instances")

    def _get_responsible_service(self, instance):
        form_slug = instance.case.document.form_id
        municipality_answer = instance.case.document.answers.filter(
            question_id="municipality"
        ).first()
        municipality_value = municipality_answer.value if municipality_answer else None

        if form_slug in [
            "oereb",
            "oereb-verfahren-gemeinde",
            "mitbericht-kanton",
            "mitbericht-bund",
        ]:
            if municipality_value in ["1221", "1222"]:
                return KOOR_NP_SERVICE

            if instance.group.service.service_group.pk == 70:  # bundesstellen
                return KOOR_BD_SERVICE

            return instance.group.service

        if form_slug in ["commercial-permit"]:
            if municipality_value in ["1221", "1222"]:
                return KOOR_NP_SERVICE

        if form_slug in ["cantonal-territory-usage"]:
            veranstaltung_answer = instance.case.document.answers.filter(
                question_id="veranstaltung-art"
            ).first()
            event_type_answer = (
                veranstaltung_answer.value if veranstaltung_answer else None
            )

            if event_type_answer in [
                "veranstaltung-art-sportanlass",
                "veranstaltung-art-foto-und-filmaufnahmen",
                "veranstaltung-art-andere",
            ]:
                return KOOR_SD_SERVICE
            else:
                return KOOR_BD_SERVICE

        if form_slug in ["konzession-waermeentnahme", "bohrbewilligung-waermeentnahme"]:
            return KOOR_AFE_SERVICE

        if form_slug in ["pgv-gemeindestrasse"]:
            return KOOR_BD_SERVICE

        if instance.group.pk == uri_constants.KOOR_AFJ_GROUP_ID:
            # instances where the koor afj was previously responsible for
            # stay with the koor afj
            return KOOR_AFJ_SERVICE

        return SERVICE_LOCATIONS.get(municipality_value)

    def _create_instance_service_object(self, instance):
        responsible_service = self._get_responsible_service(instance)

        InstanceService.objects.get_or_create(
            instance=instance,
            service=responsible_service,
            active=1,
            defaults={"activation_date": None},
        )
