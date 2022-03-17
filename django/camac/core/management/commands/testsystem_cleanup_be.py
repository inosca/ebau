from caluma.caluma_form import models
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from camac.document.models import AttachmentDownloadHistory
from camac.instance.models import Instance
from camac.user.models import Group, GroupT, Service, ServiceT, User, UserGroup

FORM_MODELS = [
    models.HistoricalAnswer,
    models.HistoricalAnswerDocument,
    models.HistoricalDocument,
    models.HistoricalDynamicOption,
    models.HistoricalFile,
    models.HistoricalForm,
    models.HistoricalFormQuestion,
    models.HistoricalOption,
    models.HistoricalQuestion,
    models.HistoricalQuestionOption,
]

SERVICE_GROUP_SERVICE = 1
SERVICE_GROUP_MUNICIPALITY = 2
SERVICE_GROUP_DISTRICT = 20000
SERVICE_GROUP_CONSTRUCTION_CONTROL = 3

ROLE_SERVICE_LEAD = 4
ROLE_SERVICE_ADMIN = 20008
ROLE_SERVICE_CLERK = 20001
ROLE_SERVICE_READONLY = 20002
ROLE_SUBSERVICE = 20000

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

        # Delete all instances, historical tables and attachment download histories
        Instance.objects.all().delete()
        AttachmentDownloadHistory.objects.all().delete()
        self.delete_historical_tables()

        # Delete all entries in UserGroup except service accounts and system-betrieb user
        user_ids = [
            user.id
            for user in User.objects.filter(username__contains="service-account")
        ]
        UserGroup.objects.all().exclude(
            Q(user_id__in=user_ids),
            Q(group_id=GROUP_SYSTEMBETRIEB),
            Q(group_id=GROUP_ADMIN),
        ).delete()

        # Create the services
        district = self.create_service(
            "Test Regierungsstatthalteramt",
            "Test Regierungsstatthalteramt",
            1,
            SERVICE_GROUP_DISTRICT,
        )
        municipality = self.create_service(
            "Test Gemeinde", "Test Gemeinde", 2, SERVICE_GROUP_MUNICIPALITY
        )
        service = self.create_service(
            "Test Fachstelle", "Test Fachstelle", 3, SERVICE_GROUP_SERVICE
        )
        service2 = self.create_service(
            "Test Fachstelle 2", "Test Fachstelle 2", 4, SERVICE_GROUP_SERVICE
        )
        subservice = self.create_service(
            "Test Unterfachstelle", "Test Unterfachstelle", 5, SERVICE_GROUP_SERVICE
        )
        construction_control = self.create_service(
            "Test Baukontrolle",
            "Test Baukontrolle",
            6,
            SERVICE_GROUP_CONSTRUCTION_CONTROL,
        )

        services = [district, municipality, service, service2, construction_control]

        # Create the translated services
        services_t = [
            self.create_service_t(
                "Test Préfecture",
                "Test Regierungsstatthalteramt",
                "fr",
                district,
            ),
            self.create_service_t(
                "Test Municipalité", "Test Gemeinde", "fr", municipality
            ),
            self.create_service_t(
                "Test Service spécialisé", "Test Fachstelle", "fr", service
            ),
            self.create_service_t(
                "Test Service spécialisé 2", "Test Fachstelle 2", "fr", service2
            ),
            self.create_service_t(
                "Test contrôle construction",
                "Test Baukontrolle",
                "fr",
                construction_control,
            ),
            self.create_service_t(
                "Test Regierungsstatthalteramt",
                "Test Regierungsstatthalteramt",
                "de",
                district,
            ),
            self.create_service_t("Test Gemeinde", "Test Gemeinde", "de", municipality),
            self.create_service_t("Test Fachstelle", "Test Fachstelle", "de", service),
            self.create_service_t(
                "Test Fachstelle 2", "Test Fachstelle 2", "de", service2
            ),
            self.create_service_t(
                "Test Baukontrolle",
                "Test Baukontrolle",
                "de",
                construction_control,
            ),
        ]

        # Create the subservice group and translated subservice group
        subservices_t = [
            self.create_service_t(
                "Test Unité d'un service spécialisé",
                "Test Unterfachstelle",
                "fr",
                subservice,
            ),
            self.create_service_t(
                "Test Unterfachstelle",
                "Test Unterfachstelle",
                "de",
                subservice,
            ),
        ]
        self.create_group_subservice(subservice)
        self.create_group_t_subservices(subservices_t)

        # Create the groups and translated groups
        self.create_groups(
            services,
        )
        self.create_groups_t(services_t)

        # Assign all new created groups to all users
        groups = Group.objects.filter(name__isnull=False)
        for user in User.objects.all():
            for group in groups:
                UserGroup.objects.create(
                    default_group=0, user_id=user.pk, group_id=group.pk
                )

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def delete_historical_tables(self):
        for model in FORM_MODELS:
            model.objects.all().delete()
            self.stdout.write(f"Table {model} was deleted")

    def create_service(self, name, description, sort, service_group_id):
        service = Service.objects.create(
            name=name,
            description=description,
            sort=sort,
            service_group_id=service_group_id,
        )
        self.stdout.write(f"Service {service.name} was created")
        return service

    def create_service_t(self, name, description, language, service):
        service_t = ServiceT.objects.create(
            name=name, description=description, language=language, service=service
        )
        self.stdout.write(f"ServiceT {service_t.name} was created")
        return service_t

    def create_group(self, name, role_id, service):
        group = Group.objects.create(name=name, role_id=role_id, service=service)
        self.stdout.write(f"Group {group.name} was created")
        return group

    def create_group_t(self, name, group, language):
        group_t = GroupT.objects.create(name=name, group=group, language=language)
        self.stdout.write(f"GroupT {group_t.name} was created")
        return group_t

    def create_groups(self, services):
        for service in services:
            self.create_group(
                f"Administration {service.name}", ROLE_SERVICE_ADMIN, service
            )
            self.create_group(f"Leitung {service.name}", ROLE_SERVICE_LEAD, service)
            self.create_group(
                f"Sachbearbeitung {service.name}", ROLE_SERVICE_CLERK, service
            )
            self.create_group(
                f"Einsichtsberechtigte {service.name}", ROLE_SERVICE_READONLY, service
            )
            self.stdout.write(
                f"For the service {service.name}, the admin, lead, clerk and readonly groups were created"
            )

    def create_group_subservice(self, sub_service):
        self.create_group(sub_service.name, ROLE_SUBSERVICE, sub_service)

    def create_group_t_subservices(self, sub_services_t):
        for sub_service_t in sub_services_t:
            subservice_name = self.get_translated_service_name(
                sub_service_t,
                "Test Unterfachstelle",
                "Test Unité d'un service spécialisé",
            )
            self.create_group_t(
                subservice_name,
                Group.objects.get(name="Test Unterfachstelle"),
                sub_service_t.language,
            )

    def create_groups_t(self, services):
        for service in services:
            lead_name = self.get_translated_service_name(
                service, "Leitung ", "Responsable "
            )
            clerk_name = self.get_translated_service_name(
                service, "Sachbearbeitung ", "Collaborateur "
            )
            readonly_name = self.get_translated_service_name(
                service, "Einsichtsberechtigte ", "Personne autorisée "
            )

            self.create_group_t(
                f"Administration {service.name}",
                Group.objects.get(name=f"Administration {service.description}"),
                service.language,
            )
            self.create_group_t(
                lead_name + service.name,
                Group.objects.get(name=f"Leitung {service.description}"),
                service.language,
            )
            self.create_group_t(
                clerk_name + service.name,
                Group.objects.get(name=f"Sachbearbeitung {service.description}"),
                service.language,
            )
            self.create_group_t(
                readonly_name + service.name,
                Group.objects.get(name=f"Einsichtsberechtigte {service.description}"),
                service.language,
            )
            self.stdout.write(
                f"For the ServiceT {service.name}, the admin, lead, clerk and readonly groups were created in language {service.language}"
            )

    def get_translated_service_name(self, service, name_de, name_fr):
        return name_de if service.language == "de" else name_fr
