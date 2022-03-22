from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import models as caluma_workflow_models
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from camac.echbern.models import Message
from camac.instance.models import Instance
from camac.user.models import Group, GroupT, Service, ServiceT, User, UserGroup

SERVICE_GROUP_SERVICE = 1
SERVICE_GROUP_MUNICIPALITY = 2
SERVICE_GROUP_DISTRICT = 20000
SERVICE_GROUP_CONSTRUCTION_CONTROL = 3

ROLE_LEITUNG_LEITBEHOERDE = 3
ROLE_LEITUNG_FACHSTELLE = 4
ROLE_LEITUNG_BAUKONTROLLE = 5
ROLE_UNTERFACHSTELLE = 20000
ROLE_SACHBEARBEITER_LEITBEHOERDE = 20004
ROLE_SACHBEARBEITER_BAUKONTROLLE = 20005
ROLE_SACHBEARBEITER_FACHSTELLE = 20001
ROLE_READONLY_LEITBEHOERDE = 20003
ROLE_READONLY_BAUKONTROLLE = 20006
ROLE_READONLY_FACHSTELLE = 20002
ROLE_ADMIN_LEITBEHOERDE = 20007
ROLE_ADMIN_BAUKONTROLLE = 20009
ROLE_ADMIN_FACHSTELLE = 20008

GROUP_SYSTEMBETRIEB = 10000
GROUP_ADMIN = 1


class Command(BaseCommand):
    help = """Prepare services for the dossier import in bern."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry",
            default=False,
            action="store_true",
            help="Don't apply changes",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        for model in [
            Instance,  # Delete all instances, attachments and attachment download histories
            Message,
            caluma_workflow_models.Case,
            caluma_workflow_models.HistoricalCase,
            caluma_workflow_models.HistoricalWorkItem,
            caluma_form_models.HistoricalAnswer,
            caluma_form_models.HistoricalAnswerDocument,
            caluma_form_models.HistoricalDocument,
            caluma_form_models.HistoricalFile,
        ]:
            model.objects.all().delete()
            self.stdout.write(f"Table {model} was deleted")

        caluma_form_models.Document.objects.exclude(form_id="dashboard").delete()
        caluma_form_models.Answer.objects.exclude(
            document__form_id="dashboard"
        ).delete()

        # Delete all entries in UserGroup except service accounts and system-betrieb user
        service_account_user_ids = [
            user.id
            for user in User.objects.filter(username__contains="service-account")
        ]
        UserGroup.objects.all().exclude(
            Q(user_id__in=service_account_user_ids)
            | Q(group_id=GROUP_SYSTEMBETRIEB)
            | Q(group_id=GROUP_ADMIN)
        ).delete()

        # Create the services
        district = self.create_service(
            "Regierungsstatthalteramt Testertal",
            "Préfecture du Test",
            SERVICE_GROUP_DISTRICT,
        )
        municipality = self.create_service(
            "Leitbehörde Beispieldorf",
            "Autorité directrice Test",
            SERVICE_GROUP_MUNICIPALITY,
        )
        service = self.create_service(
            "Amt für Testzwecke", "Office du Test", SERVICE_GROUP_SERVICE
        )
        service2 = self.create_service(
            "Amt für Testzwecke 2", "Office du Test 2", SERVICE_GROUP_SERVICE
        )
        subservice = self.create_service(
            "Abteilung Spezialtests (Amt für Testzwecke)",
            "Unité du Test spécial (Office du Test)",
            SERVICE_GROUP_SERVICE,
            parent=service,
        )
        construction_control = self.create_service(
            "Baukontrolle Beispieldorf",
            "Contrôle construction Test",
            SERVICE_GROUP_CONSTRUCTION_CONTROL,
        )

        services = [district, municipality, service, service2, construction_control]

        # Create the groups and translated groups
        self.create_groups(services)
        self.create_group_for_subservice(subservice)

        # Assign all new created groups to all users
        groups = Group.objects.filter(
            service__in=services + [subservice],
            role_id__in=[
                ROLE_LEITUNG_LEITBEHOERDE,
                ROLE_LEITUNG_FACHSTELLE,
                ROLE_LEITUNG_BAUKONTROLLE,
                ROLE_ADMIN_LEITBEHOERDE,
                ROLE_ADMIN_FACHSTELLE,
                ROLE_UNTERFACHSTELLE,
            ],
        )
        for user in User.objects.exclude(id__in=service_account_user_ids):
            for group in groups:
                UserGroup.objects.create(
                    default_group=0, user_id=user.pk, group_id=group.pk
                )

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def create_service(self, name_de, name_fr, service_group_id, parent=None):
        service = Service.objects.create(
            sort=9999,
            service_group_id=service_group_id,
            service_parent=parent,
        )
        ServiceT.objects.create(name=name_de, language="de", service=service)
        ServiceT.objects.create(name=name_fr, language="fr", service=service)
        self.stdout.write(f"Service {service.get_name('de')} was created")
        return service

    def create_group(self, name_de, name_fr, role_id, service, parent=None):
        group = Group.objects.create(role_id=role_id, service=service)
        GroupT.objects.create(name=name_de, group=group, language="de")
        GroupT.objects.create(name=name_fr, group=group, language="fr")
        return group

    def service_group_to_role(self, service, level):
        mapping = {
            SERVICE_GROUP_DISTRICT: {
                "admin": ROLE_ADMIN_LEITBEHOERDE,
                "lead": ROLE_LEITUNG_LEITBEHOERDE,
                "clerk": ROLE_SACHBEARBEITER_LEITBEHOERDE,
                "readonly": ROLE_READONLY_LEITBEHOERDE,
            },
            SERVICE_GROUP_MUNICIPALITY: {
                "admin": ROLE_ADMIN_LEITBEHOERDE,
                "lead": ROLE_LEITUNG_LEITBEHOERDE,
                "clerk": ROLE_SACHBEARBEITER_LEITBEHOERDE,
                "readonly": ROLE_READONLY_LEITBEHOERDE,
            },
            SERVICE_GROUP_CONSTRUCTION_CONTROL: {
                "admin": ROLE_ADMIN_BAUKONTROLLE,
                "lead": ROLE_LEITUNG_BAUKONTROLLE,
                "clerk": ROLE_SACHBEARBEITER_BAUKONTROLLE,
                "readonly": ROLE_READONLY_BAUKONTROLLE,
            },
            SERVICE_GROUP_SERVICE: {
                "admin": ROLE_ADMIN_FACHSTELLE,
                "lead": ROLE_LEITUNG_FACHSTELLE,
                "clerk": ROLE_SACHBEARBEITER_FACHSTELLE,
                "readonly": ROLE_READONLY_FACHSTELLE,
            },
        }
        return mapping[service.service_group_id][level]

    def create_groups(self, services):
        for service in services:
            self.create_group(
                f"Administration {service.get_name('de')}",
                f"Administration {service.get_name('fr')}",
                self.service_group_to_role(service, "admin"),
                service,
            )
            self.create_group(
                f"Leitung {service.get_name('de')}",
                f"Responsable {service.get_name('fr')}",
                self.service_group_to_role(service, "lead"),
                service,
            )
            self.create_group(
                f"Sachbearbeiter {service.get_name('de')}",
                f"Collaborateur {service.get_name('fr')}",
                self.service_group_to_role(service, "clerk"),
                service,
            )
            self.create_group(
                f"Einsichtsberechtigte {service.get_name('de')}",
                f"Personne autorisée à consulter {service.get_name('fr')}",
                self.service_group_to_role(service, "readonly"),
                service,
            )
            self.stdout.write(
                f"For the service {service.get_name('de')}, all groups were created"
            )

    def create_group_for_subservice(self, sub_service):
        self.create_group(
            "Abteilung Spezialtests (Amt für Testzwecke)",
            "Unité du Test spécial (Office du Test)",
            ROLE_UNTERFACHSTELLE,
            sub_service,
        )
