import json
import os

from django.core.management.base import BaseCommand
from django.db import transaction

from camac.user.models import Group, User, UserGroup

DEFAULT_EXPORT_PATH = "user_backup_export.json"


class Command(BaseCommand):
    help = "Saves and restores users and their group memberships."

    def add_arguments(self, parser):
        parser.add_argument(
            "action", choices=["save", "restore"], help="Action: save or restore"
        )

    def handle(self, *args, **options):
        action = options["action"]

        if action == "save":
            self.handle_save(DEFAULT_EXPORT_PATH)
        elif action == "restore":
            self.handle_restore(DEFAULT_EXPORT_PATH)

    def handle_save(self, file_path):
        self.stdout.write(f"Saving users and groups to {file_path}...")

        users_data = self._collect_users_data()

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(users_data, f, indent=4, ensure_ascii=False)

        self.stdout.write(
            self.style.SUCCESS(f"{len(users_data)} users successfully exported.")
        )

    def _collect_users_data(self):
        users_data = []
        users = User.objects.prefetch_related(
            "user_groups__group__trans",
        ).all()

        for user in users:
            groups = []
            default_group_name = None
            for ug in user.user_groups.all():
                group = ug.group
                name = group.get_name("de")
                groups.append(name)

                if ug.default_group:
                    default_group_name = name

            if not groups:
                continue

            user_entry = {
                "username": user.username,
                "groups": groups,
            }
            if default_group_name:
                user_entry["default_group"] = default_group_name

            users_data.append(user_entry)
        return users_data

    @transaction.atomic
    def handle_restore(self, file_path):
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"File {file_path} not found."))
            return

        self.stdout.write(f"Restoring users from {file_path}...")

        with open(file_path, "r", encoding="utf-8") as f:
            users_data = json.load(f)

        users_created = 0
        memberships_created = 0
        for user_entry in users_data:
            u_created, mem_count = self._process_user_entry(user_entry)
            users_created += u_created
            memberships_created += mem_count

        self.stdout.write(
            self.style.SUCCESS(
                f"{users_created} users created and {memberships_created} memberships successfully created."
            )
        )

    def _process_user_entry(self, user_entry):
        username = user_entry.get("username")

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "name": username,
                "surname": username,
                "language": "de",
            },
        )
        if created:
            self.stdout.write(f"Created new user: {username}")

        memberships_created = 0
        default_group_name = user_entry.get("default_group")

        for group_entry in user_entry.get("groups", []):
            group = self._find_group(group_entry)
            if not group:
                self.stdout.write(
                    self.style.WARNING(
                        f"Group '{group_entry}' not found. Skipping membership for {username}."
                    )
                )
                continue

            is_default = group_entry == default_group_name
            mem_created = self._assign_group(user, group, is_default=is_default)
            memberships_created += mem_created

        return 1 if created else 0, memberships_created

    def _find_group(self, group_name):
        return Group.objects.filter(
            trans__name=group_name, trans__language="de"
        ).first()

    def _assign_group(self, user, group, is_default=False):
        default_val = 1 if is_default else 0
        ug, created = UserGroup.objects.get_or_create(
            user=user, group=group, defaults={"default_group": default_val}
        )
        if not created and ug.default_group != default_val:
            ug.default_group = default_val
            ug.save(update_fields=["default_group"])
        return 1 if created else 0
