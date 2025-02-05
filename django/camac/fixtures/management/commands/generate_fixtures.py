import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from inflection import humanize
from jinja2 import FileSystemLoader
from jinja2.sandbox import SandboxedEnvironment

from camac.settings.utils import get_all_modules, get_enabled_cantons_for_module

APP_DIR = os.path.join(settings.ROOT_DIR, "camac/fixtures")
TEMPLATE_DIR = os.path.join(APP_DIR, "templates")
OUTPUT_DIR = os.path.join(APP_DIR, "generated")


class Command(BaseCommand):
    help = "Command to generate dynamic fixtures for pytest"

    def add_arguments(self, parser):
        parser.add_argument(
            "-c",
            "--check",
            default=False,
            dest="check",
            action="store_true",
            help="Check if the generated files changed",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.engine = SandboxedEnvironment(
            trim_blocks=True,
            lstrip_blocks=True,
            loader=FileSystemLoader(TEMPLATE_DIR),
        )
        self.engine.filters["humanize"] = humanize

    def handle(self, *args, **options):
        check = options.get("check", False)

        self.generate_settings_fixtures(check)

    def generate_settings_fixtures(self, check: bool):
        filename = "settings_fixtures.py"

        template = self.engine.get_template(f"{filename}.j2")

        content = template.render(modules=self.get_settings_fixtures_config())
        content = content.strip() + "\n"

        output_file = os.path.join(OUTPUT_DIR, filename)

        if check:
            with open(output_file, "r") as f:
                if f.read() != content:
                    raise CommandError(
                        "The fixtures for the module settings do not match the "
                        "current configuration. Please run `./manage.py "
                        "generate_fixtures` and commit the changes."
                    )
        else:
            with open(output_file, "w") as f:
                f.write(content)

    def get_settings_fixtures_config(self):
        default_fixture_config = [
            {"prefix": "", "canton": None, "disable": False},
            {"prefix": "disable_", "canton": None, "disable": True},
        ]

        return {
            module_name: default_fixture_config
            + [
                {
                    "prefix": f"{settings.APPLICATIONS[canton]['SHORT_NAME']}_",
                    "canton": canton,
                    "disable": False,
                }
                for canton in get_enabled_cantons_for_module(module_name, True)
            ]
            for module_name in get_all_modules()
        }
