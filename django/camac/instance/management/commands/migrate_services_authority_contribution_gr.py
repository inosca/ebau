from logging import getLogger

from django.core.management.base import BaseCommand
from django.db import transaction

from camac.constants import kt_gr as gr_constants
from camac.user.models import (
    Group,
    GroupT,
    Role,
    Service,
    ServiceGroup,
    ServiceT,
    User,
    UserGroup,
)

log = getLogger(__name__)

OFFICES = [
    {
        "slug": "apsp",
        "de": "Alters- und Pflegeheim sowie Pflegegruppen",
        "it": "Alters- und Pflegeheim sowie Pflegegruppen",
    },
    {
        "slug": "sssh",
        "de": "Sonderschulen/Sonderschullheime",
        "it": "Sonderschulen/Sonderschullheime",
    },
    {
        "slug": "wate",
        "de": "Wohn-, Arbeits- und Tagesstrukturplätze Erwachsene",
        "it": "Wohn-, Arbeits- und Tagesstrukturplätze Erwachsene",
    },
    {
        "slug": "bfgb",
        "de": "Berufliche Grundbildung",
        "it": "Berufliche Grundbildung",
    },
    {
        "slug": "wbah",
        "de": "Weiterführende Bildungsangebote Hochschule",
        "it": "Weiterführende Bildungsangebote Hochschule",
    },
]

BUILDING_DEPARTMENTS = [
    {
        "slug": "hochbauamt",
        "de": "Hochbauamt",
        "it": "Hochbauamt",
    },
]


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--commit", dest="commit", action="store_true", default=False
        )
        parser.add_argument(
            "--assign_to",
            dest="assign_to",
            type=str,
            default=None,
            help="Assign to user with this ID",
        )

    def create_service(self, opts, service_group_id, parent=None):
        service = Service.objects.create(
            sort=9999,
            service_group_id=service_group_id,
            service_parent=parent,
            slug=opts["slug"],
            email=f"example-{opts['slug']}@example.com",
        )
        ServiceT.objects.create(name=opts["de"], language="de", service=service)
        ServiceT.objects.create(name=opts["it"], language="it", service=service)
        log.info(
            f"- Created service {service.pk}/{service.slug} ({service.get_name()})"
        )

        return service

    def assign_to_user(self, group, user_id):
        user = User.objects.get(pk=user_id)

        UserGroup.objects.create(user=user, group=group, default_group=1)
        log.info(
            f"   -> Assigned group {group.pk} ({group.get_name()}) to user {user.pk} ({user.get_full_name()})"
        )

    def create_group(self, opts, role_id, service):
        group = Group.objects.create(role_id=role_id, service=service)
        GroupT.objects.create(name=opts["de"], group=group, language="de")
        GroupT.objects.create(name=opts["it"], group=group, language="it")
        log.info(f"   -> Created group {group.pk} ({group.get_name()})")

        return group

    @transaction.atomic
    def handle(self, *args, **options):
        self.verbosity = options.get("verbosity", 1)
        sid = transaction.savepoint()

        service_group_ac = ServiceGroup.objects.get(
            name=gr_constants.AUTHORITY_CONTRIBUTION_SERVICE_GROUP
        )
        service_group_bd = ServiceGroup.objects.get(
            name=gr_constants.BUILDING_DEPARTMENT_SERVICE_GROUP
        )
        role_municipality_admin = Role.objects.get(name="municipality-admin")
        role_municipality_lead = Role.objects.get(name="municipality-lead")
        role_service_admin = Role.objects.get(name="service-admin")
        role_service_lead = Role.objects.get(name="service-lead")

        log.info("=== Creating services and groups for authority contribution ===")
        for dienststelle in OFFICES:
            if Service.objects.filter(slug=dienststelle["slug"]).exists():
                log.warning(
                    f"- Service {dienststelle['slug']} already exists, skipping creation"
                )
                continue

            service = self.create_service(
                dienststelle,
                service_group_ac.pk,
            )
            group_admin = self.create_group(
                {
                    "de": f"Administration {dienststelle['de']}",
                    "it": f"Administration {dienststelle['it']}",
                },
                role_municipality_admin.pk,
                service,
            )
            group_service = self.create_group(
                {
                    "de": f"Sachbearbeitung {dienststelle['de']}",
                    "it": f"Sachbearbeitung {dienststelle['it']}",
                },
                role_municipality_lead.pk,
                service,
            )

            if options["assign_to"]:
                self.assign_to_user(group_admin, options["assign_to"])
                self.assign_to_user(group_service, options["assign_to"])

        log.info("=== Creating services and groups for building departments ===")
        for building_dept in BUILDING_DEPARTMENTS:
            if Service.objects.filter(slug=building_dept["slug"]).exists():
                log.warning(
                    f"- Service {building_dept['slug']} already exists, skipping creation"
                )
                continue

            service = self.create_service(
                building_dept,
                service_group_bd.pk,
            )
            group_admin = self.create_group(
                {
                    "de": f"Administration {building_dept['de']}",
                    "it": f"Administration {building_dept['it']}",
                },
                role_service_admin.pk,
                service,
            )
            group_service = self.create_group(
                {
                    "de": f"Sachbearbeitung {building_dept['de']}",
                    "it": f"Sachbearbeitung {building_dept['it']}",
                },
                role_service_lead.pk,
                service,
            )

            if options["assign_to"]:
                self.assign_to_user(group_admin, options["assign_to"])
                self.assign_to_user(group_service, options["assign_to"])

        if options["commit"]:
            print("Committing changes to database")
            transaction.savepoint_commit(sid)
        else:
            print(
                "Not committing changes to database. Run again with --commit to actually apply changes"
            )
            transaction.savepoint_rollback(sid)
