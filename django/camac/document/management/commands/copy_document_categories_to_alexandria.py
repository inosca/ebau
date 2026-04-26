import json
import random

from alexandria.core import models as alexandria_models
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

import camac.document.permissions
from camac.document import (
    models as document_models,
    permissions as document_permissions,
)


class Command(BaseCommand):
    help = "Create Alexandria categories form Document Module AttachmentSections"

    def add_arguments(self, parser):
        parser.add_argument("--clear-before", action="store_true", default=False)
        parser.add_argument("--confirm", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        savepoint = transaction.savepoint()
        self._warned = set()

        if options["clear_before"]:
            self.clear()

        self.migrate()

        if not options["confirm"]:
            transaction.savepoint_rollback(savepoint)

    def migrate(self):
        for section in document_models.AttachmentSection.objects.all():
            self.migrate_section(section)

    def _unique_slug(self, base_slug):
        # Why is this even needed? In SZ, there are two attachment
        # sections with the exact same name:
        # "Interne Ablage (nur gruppenintern sichtbar)" (ids 2 and 7)

        suffix = 1
        slug = base_slug
        while alexandria_models.Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{suffix}"
            suffix += 1
        return slug

    def migrate_section(self, section: document_models.AttachmentSection):

        translated_attr = self.get_translated_data(section)
        name = translated_attr["name"]
        description = translated_attr["description"]

        slug = self._unique_slug(slugify(name["de"]))
        self.stdout.write(f"Creating Alexandria category: {slug} - {name['de']}\n")

        perms = self._permission_info(section)
        self.stdout.write("   Permissions:")
        metainfo = {
            "access": {},
            "_comment": "Access config provisional - full config follows",
        }
        for role, perm, condition in perms:
            access_level = self._role_to_accesslevel(role)
            if access_level not in settings.PERMISSIONS["ACCESS_LEVELS"]:
                self._warn(
                    f"        Access Level '{access_level}' does not yet have config in permissions module"
                )
            vis = self._permission_class_to_visibility(perm, condition)
            self.stdout.write(f"        {role}: {vis}")
            if vis:
                metainfo["access"][access_level] = {"visibility": vis}

        category = alexandria_models.Category.objects.create(
            slug=slug,
            name=name,
            description=description,
            allowed_mime_types=section.allowed_mime_types,
            color=self._randcolor(),
            parent=None,
            sort=section.sort,
            metainfo=metainfo,
            # Note:
            # - notification_template not used in SZ, UR
            # - recipient_types also not used in SZ, UR
        )

        self._collect_subcategories(section, category)

    def _warn(self, msg):
        if msg not in self._warned:
            self._warned.add(msg)
            self.stderr.write(msg)

    def _permission_class_to_visibility(self, perm_cls, cond_fn):
        if cond_fn not in [
            # These conditions don't affect the visibility, only the
            # *permissions*
            None,
            camac.document.permissions._is_general_instance,
            camac.document.permissions._is_internal_instance,
        ]:
            # This needs to be analyzed - does it affect visibility? If not, add
            # to the above list to ignore it.
            # If we find any conditional function that we need to consider, decide
            # on the further processing
            breakpoint()
        match perm_cls:
            case camac.document.permissions.ReadPermission:
                return "all"
            case camac.document.permissions.AdminDeleteableStatePermission:
                return "all"
            case camac.document.permissions.AdminPermission:
                return "all"
            case camac.document.permissions.AdminServicePermission:
                return "all"
            case camac.document.permissions.AdminInternalPermission:
                return "service"
            case camac.document.permissions.WritePermission:
                return "all"
            case camac.document.permissions.AdminInternalBusinessControlPermission:
                return "service"

            case _:
                # Check the permission class for visibility code to see what to
                # return (For example, a `build_q()` method in the permission
                # class or one if it's parent / mixin classes)
                raise RuntimeError(f"Permission class {perm_cls} not mapped yet")
        pass

    def _role_to_accesslevel(self, role_name):
        mapping = {
            "gemeinde": "lead-authority",
            "support": "support",
            "reader": "read",
            "public_reader": "public",
            "applicant": "applicant",
        }
        if role_name not in mapping:
            self._warn(
                f"        Role '{role_name}' not mapped to access level yet - "
                "falling back to role name"
            )
        return mapping.get(role_name, role_name)

    def _collect_subcategories(self, section, category):

        if settings.APPLICATION_NAME == "kt_schwyz" and section.pk == 1:
            # Schwyz has apidocuments.sectionsWithCategories[] = 1  ... and:
            # apidocuments.availableCategories[] = "dokument-grundstucksangaben"
            # apidocuments.availableCategories[] = "dokument-gutachten-nachweise-begrundungen"
            # apidocuments.availableCategories[] = "dokument-projektplane-projektbeschrieb"
            # apidocuments.availableCategories[] = "dokument-weitere-gesuchsunterlagen"
            # apidocuments.defaultCategory = "dokument-weitere-gesuchsunterlagen"
            #
            subcats = [
                "dokument-grundstucksangaben",
                "dokument-gutachten-nachweise-begrundungen",
                "dokument-projektplane-projektbeschrieb",
                "dokument-weitere-gesuchsunterlagen",
            ]
            default_subcat = "dokument-weitere-gesuchsunterlagen"

        elif settings.APPLICATION_NAME == "kt_uri" and section.pk == 12000000:
            # Uri has apidocuments.sectionsWithCategories[] = 12000000;  Dokumente Gesuchsteller
            # And:
            # apidocuments.availableCategories[] = "dokument-grundstucksangaben"
            # apidocuments.availableCategories[] = "dokument-gutachten-nachweise-begrundungen"
            # apidocuments.availableCategories[] = "dokument-projektplane-projektbeschrieb"
            # apidocuments.availableCategories[] = "dokument-weitere-gesuchsunterlagen"
            # apidocuments.defaultCategory = "dokument-weitere-gesuchsunterlagen"
            subcats = [
                "dokument-grundstucksangaben",
                "dokument-gutachten-nachweise-begrundungen",
                "dokument-projektplane-projektbeschrieb",
                "dokument-weitere-gesuchsunterlagen",
            ]
            default_subcat = "dokument-weitere-gesuchsunterlagen"
        else:
            subcats = []

        new_cats = []
        for sort, subcat in enumerate(subcats):
            question = self._question_info(subcat)
            slug = f"{category.slug}-{subcat}"
            self.stdout.write(
                f"   Creating sub category: {slug} - {question['label']}\n"
            )
            new_cats.append(
                alexandria_models.Category.objects.get_or_create(
                    slug=slug,
                    parent=category,
                    defaults={
                        "name": {"de": question["label"]},
                        "description": question["hint"],
                        # Note:
                        # - notification_template not used in SZ, UR
                        # - recipient_types also not used in SZ, UR
                        # - allowed mime types: inherit from parent by copying
                        # - Permissions should be inherited as well, so
                        #   we're explicitly not defining them here
                        "allowed_mime_types": category.allowed_mime_types,
                        "color": self._randcolor(),
                        "sort": sort,
                        "metainfo": {
                            "_is_default_subcategory": subcat == default_subcat
                        },
                    },
                )
            )
        return new_cats

    def _question_info(self, slug: str) -> dict:
        """Return a dict for the requested question.

        Question is fetched from backend as needed depending on application.

        The resulting dict is of the following form:

        >>> {
        ...     "label": "display label",
        ...     "hint": "description / documentation",
        ... }
        """

        if settings.APPLICATION_NAME == "kt_schwyz":
            path = settings.APPLICATION_DIR("form.json")
            with open(path, "r") as fh:
                return json.load(fh)["questions"][slug]
        elif settings.APPLICATION_NAME == "kt_uri":
            # Copied from php/public/public-shared/js/src/translation-messages.js
            uri_subcats = {
                "dokument-grundstucksangaben": "Grundstücksangaben",
                "dokument-projektplane-projektbeschrieb": "Projektpläne und Projektbeschrieb",
                "nachforderungen": "Nachforderungen",
                "dokument-gutachten-nachweise-begrundungen": "Gutachten, Nachweise, Begründungen",
                "dokument-weitere-gesuchsunterlagen": "Weitere Gesuchsunterlagen",
            }
            label = uri_subcats[slug]
            return {"label": label, "hint": ""}

    def get_translated_data(self, section: document_models.AttachmentSection):
        if settings.APPLICATION.get("IS_MULTILINGUAL"):
            name = {}
            description = {}
            for trans in section.trans.all():
                trans: document_models.AttachmentSectionT
                name[trans.language] = trans.name
                description[trans.language] = trans.description
            return {"name": name, "description": description}
        else:
            return {
                "name": {"de": section.name},
                "description": {"de": section.description},
            }

    def _permission_info(self, section: document_models.AttachmentSection):
        _role_permissions_lc = {
            role.lower(): actual_role
            for role, actual_role in settings.APPLICATION["ROLE_PERMISSIONS"].items()
        }
        if (
            "gemeinde" in _role_permissions_lc
            and "municipality" not in _role_permissions_lc
        ):
            # SZ special case - TODO verify why this discrepancy exists
            _role_permissions_lc["municipality"] = _role_permissions_lc["gemeinde"]
        elif (
            "sekretariat der gemeindebaubehörde" in _role_permissions_lc
            and "municipality" not in _role_permissions_lc
        ):
            # UR special case - TODO verify why this discrepancy exists
            _role_permissions_lc["municipality"] = _role_permissions_lc[
                "sekretariat der gemeindebaubehörde"
            ]

        results = []
        perms = document_permissions.PERMISSIONS[settings.APPLICATION_NAME]
        for role, perm_info in perms.items():
            if role not in _role_permissions_lc:
                if role in settings.APPLICATION["ROLE_PERMISSIONS"].values():
                    actual_role = role
                else:
                    breakpoint()
                    # Something not properly matched...
                    ...
            else:
                actual_role = _role_permissions_lc[role]

            for permission, section_ids in perm_info.items():
                cond = None
                if isinstance(section_ids, tuple):
                    # additional condition present
                    cond, section_ids = section_ids
                if section.pk in section_ids:
                    # affects current section - collect
                    results.append((actual_role, permission, cond))
        return results

    def clear(self):
        alexandria_models.Category.objects.all().delete()

    def _randcolor(self):
        h = random.randint(0, 360)
        s = random.randint(0, 100)
        l = 40  # noqa: E741
        return f"hsl({h} {s}% {l}%)"

        # RGB mode

        r = random.randint(80, 180)
        g = random.randint(80, 200)
        b = random.randint(80, 180)
        return f"#{r:2x}{g:2x}{b:2x}"
