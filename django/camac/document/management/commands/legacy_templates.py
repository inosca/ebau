import importlib
import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from docxtpl import DocxTemplate
from jinja2.exceptions import TemplateSyntaxError

from camac.jinja import get_jinja_env


class Command(BaseCommand):
    help = "Utilities for managing templates for legacy document creation."

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        try:
            self.template_class = getattr(
                importlib.import_module("camac.document.models"), "Template"
            )
        except ImportError:  # pragma: no cover, handles future deprecation
            raise CommandError(
                "'camac.document.models.Template' is not defined anymore."
            )
        self.all_placeholders = set()
        self.fail_count = 0
        self.jinja_env = get_jinja_env()

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(
            title="sub-commands",
            required=True,
        )

        # extract used placeholders
        extract_used_parser = subparsers.add_parser(
            "extract_used_placeholders",
            help="Extract used placeholders from legacy templates.",
        )
        extract_used_parser.set_defaults(method=self.extract_used)

        # migrate templates to DMS
        export_templates_parser = subparsers.add_parser(
            "export_templates", help="Dump templates to JSON for loading in DMS."
        )
        export_templates_parser.set_defaults(method=self.export_templates)
        export_templates_parser.add_argument(
            "--out_file",
            help="Absolute path of the resulting fixture file",
            default="dms_templates_fixture.json",
        )

        # cleanup dangling files in templates directory
        remove_dangling_parser = subparsers.add_parser(
            "remove_dangling",
            help="Remove unreferenced template files from upload dir.",
        )
        remove_dangling_parser.add_argument("--run", action="store_true", default=False)
        remove_dangling_parser.set_defaults(method=self.remove_dangling)

    def handle(self, *args, method, **options):
        method(*args, **options)

    def extract_used(self, *args, **options):
        for template in self.template_class.objects.all():
            doc = DocxTemplate(template.path)

            try:
                self.all_placeholders.update(
                    doc.get_undeclared_template_variables(self.jinja_env)
                )
            except TemplateSyntaxError:  # pragma: no cover
                self.fail_count += 1
                self.stdout.write(
                    f"Could not extract placeholders from template {template.name}"
                )
            except ValueError:  # pragma: no cover
                self.fail_count += 1
                self.stdout.write(f"Template {template.name} is not a word file")
            except Exception as e:  # pragma: no cover
                self.fail_count += 1
                self.stdout.write(
                    f"Unknown error when extracting placeholders from template {template.name}: {e}"
                )
        self.stdout.write(
            f"Extracted {len(self.all_placeholders)} used placeholders with {self.fail_count} errors:"
        )

        for placeholder in sorted(self.all_placeholders):
            self.stdout.write(f"\t- {placeholder}")

    def export_templates(self, *args, **options):
        """Create a JSON dump of all templates ready for loading to DMS."""
        target_file = Path(options["out_file"])

        templates = []
        for templ in self.template_class.objects.all():
            template = Path(templ.path.name).name
            templ_slug = (
                slugify(templ.name)
                if len(slugify(templ.name)) < 45
                else f"{slugify(templ.name)[:45]}{templ.pk:04}"
            )

            # make a fixture dump for templates for loading in document-merge-service
            dms_template = {
                "model": "api.template",
                "pk": templ_slug,
                "fields": {
                    "description": f"{templ.name}",
                    "template": template,
                    "engine": "docx-template",
                    "meta": {
                        # "service_group" expects the group SLUG for evaluation of template's visibility
                        "service_group": templ.group.service.slug or "",
                        # service id is expected to be a string
                        "service": str(templ.service_id or ""),
                    },
                },
            }
            templates.append(dms_template)
        json.dump(templates, target_file.open("w"), indent=4)
        self.stdout.write(
            f"Dumped {len(templates)} template entries to {target_file.absolute()}."
        )

    def remove_dangling(self, *args, **options):
        referenced = self.template_class.objects.values_list("path", flat=True)
        match = "**/templates/*"
        all_files = Path(settings.MEDIA_ROOT).glob(match)
        self.stdout.write(
            self.style.NOTICE(
                f"\n{len(list(all_files))} total number of files in $MEDIA_ROOT/templates/**"
            )
        )
        dangling = []
        for any_file in Path(settings.MEDIA_ROOT).glob(match):
            if "/".join(any_file.parts[-2:]) not in referenced:
                dangling.append(any_file)
                if options.get("run") is True:
                    any_file.unlink(missing_ok=True)
        self.stdout.write(
            self.style.NOTICE(
                f"\n{'Removed' if options.get('run') else 'Would remove'} {len(dangling)} dangling files from $MEDIA_ROOT/templates/ dir."
            )
        )
        self.stdout.write(self.style.WARNING("\n=== LEFTOVER FILES ==="))
        self.stdout.write(
            self.style.WARNING("\n".join(str(f.absolute()) for f in dangling))
        )
        self.stdout.write(
            self.style.SUCCESS("\n=== FILES REFERENCED BY TEMPLATE ===")
            if options.get("verbosity") > 1
            else ""
        )
        self.stdout.write(
            self.style.SUCCESS("\n".join(ref for ref in referenced))
        ) if options.get("verbosity") > 1 else ""
