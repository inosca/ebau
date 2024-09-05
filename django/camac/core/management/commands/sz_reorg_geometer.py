import typing

from caluma.caluma_form.models import transaction
from django.core.management import call_command
from django.core.management.base import BaseCommand

from camac.user.models import Group, Location, Role, Service, ServiceGroup, UserGroup


class Command(BaseCommand):
    help = "Reorganize SZ geometer groups and services"

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            action="store_true",
            dest="commit",
            default=False,
            help="Do not pretend, commit changes to DB",
            required=False,
        )

        parser.add_argument(
            "--interactive",
            action="store_true",
            dest="interactive",
            default=False,
            help="Interactive mode. Ask before committing",
            required=False,
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.verbosity = options.get("verbosity", 1)
        do_commit = options.get("commit")
        self.stdout.write(
            "Commit mode active, changes will be written to DB"
            if do_commit
            else "Pretend mode, no change will be written"
        )

        sid = transaction.savepoint()

        # Consolidate Geometer groups and services (Task 1)
        geom_group, geom_service = self._create_group_and_service("Geometer (Geoinfra)")
        to_move_group_ids = [274, 507, 509, 510, 511, 513]
        to_move_groups = Group.objects.filter(pk__in=to_move_group_ids)
        to_move_services = Service.objects.filter(
            pk__in=to_move_groups.values("service_id")
        )
        for group in to_move_groups:
            self._move_members(from_group=group, to_group=geom_group)
        for service in to_move_services:
            self._migrate_service(service, geom_service)

        # Move water services and groups (Task 2)
        entw_group = Group.objects.get(pk=275)
        old_entw_group = Group.objects.get(pk=575)

        self._move_members(old_entw_group, entw_group)
        self._migrate_service(old_entw_group.service, entw_group.service)
        self._rename_group_and_service(entw_group, "Grundstücksentwässerung (Geoinfra)")

        # Add location "Riemenstalden" to group 275 (Task 2)
        self.stdout.write(f"Adding Riemenstalden to group {entw_group}")
        entw_group.locations.add(Location.objects.get(name="Riemenstalden"))

        # Rename Brandschutz  (Task 3)
        brandschutz_group = Group.objects.get(pk=265)
        self._rename_group_and_service(brandschutz_group, "Brandschutz (Geoinfra)")

        # Rename Umweltschutz (Task 5)
        umw_group = Group.objects.get(pk=570)
        self._rename_group_and_service(umw_group, "Umweltschutzbeauftragter (Geoinfra)")

        # Create Baurecht (Task 4)
        baurecht_group, baurecht_svc = self._create_group_and_service(
            "Baurecht (Geoinfra)"
        )
        baurecht_group.locations.set(
            Location.objects.filter(
                name__in=["Arth", "Lauerz", "Steinerberg", "Rothenthurm"]
            )
        )
        assert baurecht_group.locations.count() == 4

        # Create Kontrolle Hochbau (Task 6)

        hochbau_group, _ = self._create_group_and_service(
            "Kontrolle Hochbau (Geoinfra)"
        )
        hochbau_group.locations.set(
            Location.objects.filter(name__in=["Feusisberg", "Arth"])
        )
        assert hochbau_group.locations.count() == 2

        self._finish_transaction(sid, do_commit, options.get("interactive"))

    def _finish_transaction(self, sid, do_commit, interactive):
        if interactive:
            do_commit = (
                input("Finished work. Should we commit [yN]? ").strip().lower() == "y"
            )
        if do_commit:
            breakpoint()
            message = "Committing changes to database"
            transaction.savepoint_commit(sid)
        else:
            message = "Rolling back - no changes committed to DB"
            transaction.savepoint_rollback(sid)

        self.stdout.write(message)

    def _move_members(self, from_group: Group, to_group: Group):
        if self.verbosity >= 1:
            self.stdout.write(
                f"Moving group members from {from_group.name} ({from_group.pk}) "
                f"to {to_group.name} ({to_group.pk})"
            )

        if from_group.role != to_group.role:
            self.stderr.write(
                self.style.WARNING(
                    f"Group {from_group}({from_group.role}) has different "
                    f"role than {to_group}({to_group.role})"
                )
            )
        for entry in UserGroup.objects.filter(group=from_group):
            entry.pk = None
            entry.group = to_group
            if UserGroup.objects.filter(group=to_group, user=entry.user).exists():
                self.stdout.write(
                    self.style.NOTICE(f"User {entry.user} is already in {to_group}")
                )

                continue
            entry.save()

    def _migrate_service(self, from_service, to_service):
        if self.verbosity >= 1:
            self.stdout.write(
                f"Migrating service relations: {from_service.name} ({from_service.pk}) "
                f"--> {to_service.name} ({to_service.pk})"
            )

        call_command(
            "migrate_service",
            source=str(from_service.pk),
            target=str(to_service.pk),
            exec=True,
            disable=True,
            verbosity=self.verbosity,
        )

    def _rename_group_and_service(self, group, new_name):
        if self.verbosity >= 1:
            self.stdout.write(
                f"Renaming group and service: {group.name} ({group.pk}) --> {new_name}"
            )

        group.name = new_name
        group.service.name = new_name
        group.service.save()
        group.save()

    def _create_group_and_service(self, name) -> typing.Tuple[Group, Service]:
        if self.verbosity >= 1:
            self.stdout.write(f"Creating group and service: {name}")
        service, _ = Service.objects.get_or_create(
            name=name,
            defaults={
                "service_group": ServiceGroup.objects.get(name="Fachstellen"),
            },
        )
        group, _ = Group.objects.get_or_create(
            name=name,
            service=service,
            defaults={"role": Role.objects.get(name="Fachstelle")},
        )
        return group, service
