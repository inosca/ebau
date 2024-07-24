import json
import sys
from collections import defaultdict
from logging import getLogger
from pathlib import Path

import texttable
from django.conf import settings
from django.core.management.base import BaseCommand

from camac.settings.modules import permissions as permissions_settings

log = getLogger(__name__)


class Command(BaseCommand):
    """List all currently defined permissions."""

    help = "List all currently defined permissions"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.structure = defaultdict(lambda: {"levels": set(), "irs": set()})
        self.all_cantons = False
        self.list_irs = False
        self.table = None
        self.app_name = None

    def add_arguments(self, parser):
        parser.add_argument(
            "--all-cantons",
            help="List permissions across all cantons",
            action="store_true",
        )
        parser.add_argument(
            "--canton",
            help="Inspect config of the given canton only",
            type=str,
        )

        parser.add_argument(
            "--list-irs",
            help="List the instance resources (IRs) that use the given permission",
            action="store_true",
        )

    def handle(self, *args, **options):
        self.all_cantons = options.get("all_cantons")
        self.list_irs = options.get("list_irs")

        if self.all_cantons:
            for app_name in permissions_settings.PERMISSIONS:
                self._build_structure(app_name)
        elif canton := options.get("canton"):
            if not canton.startswith("kt_"):
                canton = f"kt_{canton}"
            self.app_name = canton.replace("kt_", "")
            self._build_structure(canton)
        else:
            self._build_structure(settings.APPLICATION_NAME)
            self.app_name = settings.APPLICATION_NAME.replace("kt_", "")

        self.show()

    def _build_structure(self, app_name):
        try:
            module_settings = permissions_settings.PERMISSIONS[app_name]
        except KeyError:
            print(f"Canton config '{app_name}' does not exist!")
            print(f"Available are: {', '.join(permissions_settings.PERMISSIONS)}")
            sys.exit(1)

        if app_name in ("default", "demo"):
            return
        for access_level, permissions in module_settings["ACCESS_LEVELS"].items():
            for perm, _cond in permissions:
                self.structure[perm]["levels"].add(
                    (access_level, app_name.replace("kt_", ""))
                )

        if self.list_irs:
            self._build_ir_structure(app_name)

    def _build_ir_structure(self, app_name):
        json_file = Path(settings.ROOT_DIR) / app_name / "config/core.json"
        translations = defaultdict(dict)
        with json_file.open() as fh_json:
            core_json = json.load(fh_json)
            ir_data = [
                model
                for model in core_json
                if model["model"] == "core.instanceresource"
                and model["fields"]["require_permission"]
            ]
            for model in core_json:
                if model["model"] == "core.instanceresourcet":
                    ir_id = model["fields"]["instance_resource"]
                    lang = model["fields"]["language"]

                    translations[ir_id][lang] = model["fields"]["name"]

        for model in ir_data:
            ir_id = model["pk"]
            perm = model["fields"]["require_permission"]
            name = model["fields"]["name"] or translations[ir_id]["de"]

            self.structure[perm]["irs"].add(
                (app_name.replace("kt_", ""), name, model["pk"])
            )

    def show(self):
        # Set max width to 0, so we can do our own wrapping.
        # This allows us to make pretty lists inside the table cells
        self.table = texttable.Texttable(max_width=0)

        suffix = f" ({self.app_name})" if self.app_name else ""

        headers = ["Permission", f"Access Level{suffix}"]
        if self.list_irs:
            headers.append(f"Instance Resources{suffix}")
        self.table.header(headers)

        for perm in sorted(self.structure):
            self._render_perm(perm, self.structure[perm])
        print(self.table.draw())

    def _get_levels(self, perm, where):
        consolidated_where = defaultdict(set)
        if self.all_cantons:
            for level, canton in where:
                consolidated_where[level].add(canton)
            level_labels = [
                f"{level} ({', '.join(sorted(cantons))})"
                for level, cantons in consolidated_where.items()
            ]
            access_levels = "\n".join(sorted(level_labels))

        else:
            access_levels = "\n".join(sorted(set(level for level, _c in where)))
        return access_levels

    def _get_irs(self, perm, where: set[tuple[str, str, int]]):
        where = sorted(where)
        if self.all_cantons:
            return "\n".join(
                [f"{name} (IR {irid}, {app})" for app, name, irid in where]
            )
        # only current canton - drop the canton field for brevity
        return "\n".join([f"{name} (IR {irid})" for app, name, irid in where])

    def _render_perm(self, perm, where):
        levels = self._get_levels(perm, where["levels"])
        row = [perm, levels]

        if self.list_irs:
            row.append(self._get_irs(perm, where["irs"]))

        self.table.add_row(row)
