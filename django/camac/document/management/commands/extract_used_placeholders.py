from django.core.management.base import BaseCommand
from docxtpl import DocxTemplate
from jinja2.exceptions import TemplateSyntaxError

from camac.document.models import Template
from camac.jinja import get_jinja_env


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.all_placeholders = set()
        self.fail_count = 0
        self.jinja_env = get_jinja_env()

    def handle(self, *args, **options):
        for template in Template.objects.all():
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
