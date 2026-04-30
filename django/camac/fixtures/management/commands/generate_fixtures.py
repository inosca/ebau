import inspect
import os
from importlib import import_module

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from factory.base import FactoryMetaClass
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
        self.check_only = options.get("check", False)

        self.generate_settings_fixtures()
        self.generate_external_factories()

    def generate_settings_fixtures(self):
        default_fixture_config = [
            {"prefix": "", "canton": None, "disable": False},
            {"prefix": "disable_", "canton": None, "disable": True},
        ]

        modules = {
            settings_name: [
                {
                    "module_name": settings_name.lower(),
                    "import_path": import_path,
                    **conf,
                }
                for conf in default_fixture_config
            ]
            + [
                {
                    "prefix": f"{settings.APPLICATIONS[canton]['SHORT_NAME']}_",
                    "canton": canton,
                    "disable": False,
                    "module_name": settings_name.lower(),
                    "import_path": import_path,
                }
                for canton in get_enabled_cantons_for_module(import_path, True)
            ]
            for settings_name, import_path in get_all_modules().items()
        }

        template = self.engine.get_template("settings_fixtures.py.j2")
        content = template.render(modules=modules)

        self.write_or_check_file(
            os.path.join(OUTPUT_DIR, "settings_fixtures.py"), content
        )

    def generate_external_factories(self):
        imports = []
        classes = []

        for path, import_name, prefix in settings.EXTERNAL_FACTORY_MODULES:
            path_parts = path.split(".")
            imports.append(
                {
                    "path": ".".join(path_parts[:-1]),
                    "name": path_parts[-1],
                    "alias": import_name,
                }
            )

            for name, cls in inspect.getmembers(import_module(path), inspect.isclass):
                if (
                    isinstance(cls, FactoryMetaClass)  # Only factories
                    and not cls._meta.abstract  # No abstract factories
                    and cls.__module__ == path  # Ignore imported factories
                ):
                    classes.append(
                        {"name": name, "path": import_name, "prefix": prefix}
                    )

        template = self.engine.get_template("external_factories.py.j2")
        content = template.render(
            imports=imports,
            classes=classes,
        )

        self.write_or_check_file(
            os.path.join(OUTPUT_DIR, "external_factories.py"), content
        )

    def write_or_check_file(self, file: str, content: str):
        content = content.strip() + "\n"

        if self.check_only:
            with open(file, "r") as f:
                if f.read() != content:
                    raise CommandError(
                        f"The generated file `{file}` does not match the "
                        "current configuration. Please run `./manage.py "
                        "generate_fixtures` and commit the changes."
                    )
        else:
            with open(file, "w") as f:
                f.write(content)
