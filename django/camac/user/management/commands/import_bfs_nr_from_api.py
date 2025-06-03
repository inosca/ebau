import csv
import re
from datetime import date
from typing import Iterable, TypedDict

import requests
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from camac.user.models import Service


class CommunityData(TypedDict):
    BfsCode: str
    Name: str
    ShortName: str
    Level: int
    Parent: str


class Command(BaseCommand):
    help = """
    Import BfS numbers for municipalities directly from the BFS API.


    The BFS API will return a CSV with in the following format:
        HistoricalCode,BfsCode,ValidFrom,ValidTo,Level,Parent,Name,ShortName,Inscription,Radiation,Rec_Type_fr,Rec_Type_de

    The structure of the data is defined by the Level column.

        Level 1: Canton
            Level 2: District
                Level 3: Municipality

    We are solely interested in the Municipalities and therefore skip the levels except level 3.

    There are municipalies that have a canton identifier appended to the municipality  name
    in the format "Municipality Name (CANTON IDENTIFIER)".

    Examples:
    Kt. Solothurn:
        2425 | Holderbank (SO)
    Kt. Bern:
        310  | Rapperswil (BE)
    Kt. Graubünden:
        3834 | Roveredo (GR)

    The way the name of these municipalities is saved in the camac db differs per canton.

    For some cantons (for example kt. Bern and kt. Graubünden), we save the name of the municipality
    with the canton identifier appended:
        "Gemeinde Rapperswil (BE)", "Gemeinde Roveredo (GR)"

    For other cantons (for example kt. Solothurn), we do NOT save this canton identifier appended to the municipality name:
        "Gemeinde Holderbank"

    For cantons with the latter approach, the command already takes care of stripping the canton identifier per default.
    This is necessary for the service query filtering by municipality full translated name.

    If you want to save the canton identifier within the municipality name add the `--append-identifier` argument.

    Full command example:

    python manage.py import_bfs_nr_from_api  --canton "BE" --append-identifier
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--canton",
            "-c",
            type=str,
            help='Filter results by a specific canton short-name (e.g., "AG", "ZH").',
            required=True,
        )
        parser.add_argument(
            "--append-identifier",
            action="store_true",  # This makes it a boolean flag
            help='If set, appends the canton short-name (e.g., "(BE)") to municipality Name and ShortName. Otherwise, strips it.',
            required=False,
        )

    @transaction.atomic
    def handle(self, *args, **options):
        canton_filter = options["canton"].upper()
        append_identifier = options["append_identifier"]
        today_str = date.today().strftime("%d-%m-%Y")
        api_url = (
            f"https://www.agvchapp.bfs.admin.ch/api/communes/snapshot?date={today_str}"
        )

        self.stdout.write(self.style.NOTICE(f"Fetching data from: {api_url}"))

        try:
            response = requests.get(api_url, stream=True)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise CommandError(f"Error fetching data from API: {e}")

        decoded_content = (line.decode("utf-8") for line in response.iter_lines())
        filtered_list = self._filter_csv(
            decoded_content, canton_filter, append_identifier
        )

        for row in filtered_list:
            name = row["ShortName"]
            if not name:
                break

            service = Service.objects.filter(
                service_group__name="municipality", trans__name__contains=name
            ).first()

            if not service:
                self.stdout.write(
                    self.style.ERROR(
                        f"No municipality with name {name} found -- skipping"
                    )
                )
                continue

            service.external_identifier = row["BfsCode"]
            service.save()

        services_without = Service.objects.filter(
            service_group__name="municipality", external_identifier__isnull=True
        )

        if services_without.exists():
            names = ", ".join([s.get_name() for s in services_without])
            self.stdout.write(
                self.style.SUCCESS(
                    f"There are municipalities without a BfS number: {names}"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("All municipalities have a BfS number")
            )

    def _filter_csv(  # noqa: C901
        self, csv_content: Iterable[str], canton_filter: str, append_identifier: bool
    ) -> list[str | int]:
        """
        Filter the provided CSV list for all level 3 entries under a specified level 1 entry (matching canton identifier).

        The append_identifier argument will determine if the results have a canton identifier appended to thei names or not.
        """
        csv_reader = csv.reader(csv_content)

        header = next(csv_reader)

        try:
            name_idx = header.index("Name")
            short_name_idx = header.index("ShortName")
            level_idx = header.index("Level")
            bfs_code_idx = header.index("BfsCode")
            parent_idx = header.index("Parent")
        except ValueError as e:
            raise CommandError(f"Missing expected column in CSV header: {e}")

        self.stdout.write(
            self.style.NOTICE(f"Processing communities for canton: {canton_filter}...")
        )

        filtered_communities = []
        is_within_target_canton = False

        # Pre-compile the regex for stripping/checking the canton identifier
        canton_identifier_pattern = re.compile(
            rf"\s*\({re.escape(canton_filter)}\)\s*$", re.IGNORECASE
        )

        for i, row in enumerate(csv_reader):
            if not row:
                continue

            if len(row) <= max(name_idx, short_name_idx, level_idx):
                self.stderr.write(
                    self.style.WARNING(f"Skipping malformed row {i + 2}: {row}")
                )
                continue

            try:
                community_name = row[name_idx].strip()
                community_short_name = row[short_name_idx].strip()
                community_level = int(row[level_idx].strip())
            except (ValueError, IndexError) as e:
                self.stderr.write(
                    self.style.WARNING(
                        f"Skipping row {i + 2} due to data parsing error: {e} - Row: {row}"
                    )
                )
                continue

            if community_level == 1:
                # We encountered a Level 1 entry (a Canton)
                if community_short_name.upper() == canton_filter:
                    # This is our target canton, start collecting from here
                    is_within_target_canton = True
                else:
                    # This is a different canton, so if we were previously
                    # collecting, stop now.
                    is_within_target_canton = False
                continue  # Always skip Level 1 entries from the final list

            if is_within_target_canton:
                if community_level == 3:
                    # It's a municipality, so add it to our list

                    modified_name = community_name
                    modified_short_name = community_short_name

                    if append_identifier:
                        if not canton_identifier_pattern.search(community_name):
                            modified_name = f"{community_name} ({canton_filter})"
                        if not canton_identifier_pattern.search(community_short_name):
                            modified_short_name = (
                                f"{community_short_name} ({canton_filter})"
                            )
                    else:
                        modified_name = canton_identifier_pattern.sub(
                            "", community_name
                        ).strip()
                        modified_short_name = canton_identifier_pattern.sub(
                            "", community_short_name
                        ).strip()

                    filtered_communities.append(
                        {
                            "BfsCode": row[bfs_code_idx],
                            "Name": modified_name,
                            "ShortName": modified_short_name,
                            "Level": community_level,
                            "Parent": row[parent_idx],
                        }
                    )

        if not filtered_communities:
            self.stdout.write(
                self.style.WARNING(
                    f"No municipalities found for canton '{canton_filter}' or canton not found."
                )
            )
            return []

        self._print_results(filtered_communities, canton_filter)

        return filtered_communities

    def _print_results(self, communities: list[CommunityData], canton_filter: str):
        """Print the filtered municipality data."""
        self.stdout.write(
            self.style.SUCCESS(
                f"\nFound {len(communities)} municipalities for canton '{canton_filter}':"
            )
        )
        for community in communities:
            self.stdout.write(
                f"BFS Code: {community['BfsCode']}, Name: '{community['Name']}', Short Name: '{community['ShortName']}', Level: {community['Level']}, Parent: {community['Parent']}"
            )
