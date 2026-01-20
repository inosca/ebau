import importlib

from django.core.management.base import BaseCommand, CommandError
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
