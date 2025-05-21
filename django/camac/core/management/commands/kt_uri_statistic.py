import csv

from caluma.caluma_workflow.models import Case
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from camac.caluma.api import CalumaApi

CATEGORIES = {
    "Hochbau": ("category", "category-hochbaute"),
    "Beheizte oder gekühlte Neu- und Umbauten": (
        "das-vorhaben-betrifft",
        "das-vorhaben-betrifft-beheizte-oder-gekuehlte-neu-und-umbauten",
    ),
    "Die Änderung der Gebäudehülle beheizter oder gekühlter Bauten": (
        "das-vorhaben-betrifft",
        "das-vorhaben-betrifft-aenderung-beheizter-oder-gekuehlter-bauten",
    ),
    "Die Installation / Änderung gebäudetechnischer Anlagen (Heizung, Lüftung, Klima- und / oder Kälteanlage)": (
        "das-vorhaben-betrifft",
        "das-vorhaben-betrifft-installation-technischer-anlagen",
    ),
}

BUILDING_TYPES = {
    "Einfamilienhaus freistehend": "art-der-hochbaute-einfamilienhaus",
    "Einfamilienhaus angebaut": "art-der-hochbaute-doppeleinfamilienhaus",
    "Mehrfamilienhaus": "art-der-hochbaute-mehrfamilienhaus",
    "Wohn- und Geschäftshaus": "art-der-hochbaute-wohn-und-geschaftshaus",
    "Industrie und Gewerbebaute": "art-der-hochbaute-industrie",
    "Kaufhaus, Geschäftsgebäude": "geschaftshaus",
    "Garage / Einstellhallen im Zusammenhang mit Wohngebäuden": "garage-oder-carport",
    "Parkhaus": "parkhaus",
    "Hotel, Restaurant, Beherbergungsbetrieb": "bauten-und-anlagen-gastgewerbe",
    "Heim mit Unterkunft, Pflegedienst und Betreuung": "heim-mit-unterkunft",
    "Wohnheim ohne Pflegedienste und Betreuung": "wohnheim-ohne-pflege",
    "Spital": "spital",
    "Schulen": "schulen",
    "Sporthallen, Sportplätze": "sporthallen",
    "Freizeit- und Tourismusanlagen": "tourismusanlagen",
    "Kirchen und Sakralbauten": "kirchen",
    "Kulturbauten, Museen, etc.": "kulturbauten",
    "Landwirtschaftliche Ökonomiegebäude mit Tierhaltung": "oekonomie-mit-tieren-mit-tieren",
    "Landwirtschaftliche Ökonomiegebäude ohne Tierhaltung": "oekonomiegebaude",
    "Landwirtschaftliche Betriebsgebäude mit Wohnteil": "landwirtschaft-betrieb-wohnteil",
    "Forstwirtschaftliche Bauten und Anlagen": "forstwirtschaft",
    "Energieholzlager": "energieholzlager",
    "Materiallager": "materiallager",
    "Brennstofflager": "brennstofflager",
    "Silo / Zisterne": "silo",
    "Reklamebauten": "reklamebauten",
    "Kommunikationsanlagen (Mobilfunk-, Richtfunkanlagen)": "kommunikationsanlagen",
    "Kehrichtentsorgungsanlagen": "kehrichtentsorgungsanlagen",
    "Andere": "andere",
}

PROPOSALS = {
    "Neubau": "proposal-neubau",
    "Umbau": "proposal-umbau-erneuerung-sanierung",
    "Abbruch": "abbruch-rueckbau",
}

RECONSTRUCTION = {
    "Energetische Sanierung": "umbau-energetische-sanierung",
    "Sanierung Heizsystem": "umbau-sanierung-des-heizsystems",
    "Photovoltaische Solaranlage": "umbau-photovoltaische-solaranlage",
}

BAB_TYPE_OF_MEASURE = {
    "Neubau (BaB)": "neubau",
    "Umbau / Anbau (BaB)": "umbau-anbau",
    "Sanierung (BaB)": "sanierung",
    "Zweckänderung (BaB)": "zweckaenderung",
    "Abbruch (BaB)": "abbruch",
    "Andere (BaB)": "andere",
    "Abparzellierung Veräusserung Betriebsübergabe (BaB)": "abparzellierung",
    "Ersatzneubau (BaB)": "ersatzneubau",
}

BAB_TYPE_OF_OBJECT = {
    "Wohnbaute (BaB)": "wohnbaute",
    "Wohn- / Ökonomiebaute (BaB)": "wohn-oekonomiebaute",
    "Gewerbebaute mit Arbeitsplätzen (BaB)": "gewerbebaute-mit-arbeitsplaetzen",
    "Gewerbebaute ohne Arbeitsplätzen (BaB)": "gewerbebaute-ohne-arbeitsplaetzen",
    "Ökonomiebaute mit Tierhaltung (BaB)": "oekonomiebaute-mit-tierhaltung",
    "Ökonomiebaute ohne Tierhaltung (BaB)": "oekonomiebaute-ohne-tierhaltung",
    "Terrainveränderung (BaB)": "terrainveraenderung",
    "Viehtriebweg (BaB)": "viehtriebweg",
    "Bewirtschaftungsweg (BaB)": "bewirtschaftungsweg",
    "Hof- / Gütererschliessung (BaB)": "hof-guetererschliessung",
    "Andere (BaB)": "andere",
    "Fahrnisbauten (BaB)": "fahrnisbauten",
    "Wanderweg (BaB)": "wanderweg",
    "Betrieb Gewerbe Liegenschaften (BaB)": "betrieb-gewerbe-liegenschaften",
}

BAB_LEGAL_BASIS = {
    "Innerhalb Bauzone (BaB)": "innerhalb-bauzone",
    "RPG 16a RPV 34 1 Ökonomiebauten für die bodenabhängige Landwirtschaft (BaB)": "oekonomiebauten",
    "RPG 16a 1 RPV 34 2 Landwirtschaftliche Bauten: Aufbereitung Lagerung und Verkauf (BaB)": "landwirtschaftliche-bauten",
    "RPG 16a 1 RPV 34 3 Wohnbauten für landwirtschaftliche Gewerbe (BaB)": "wohnbauten",
    "RPG 16a RPV 35 Gemeinschaftliche Stallbauten (BaB)": "stallbauten",
    "RPG 16a 2 RPV 36 Innere Aufstockung Tierhaltung (Schweineställe, Geflügelhallen) (BaB)": "tierhaltung",
    "RPG 16a 2 RPV 37 Innere Aufstockung Gemüse- und Pflanzenbau (Gewächshäuser) (BaB)": "gewaechshaeuser",
    "RPG 16a 3 RPV 38 Bauten und Anlagen in Speziallandwirtschaftszonen (BaB)": "speziallandwirtschaftszonen",
    "RPG 16a 1 RPV 34a Gewinnung von Energie aus Biomasse (BaB)": "biomasse",
    "RPG 17 allgemein, Zonenkonforme Bauten und Anlagen in Schutzzonen (BaB)": "zonenkonform",
    "RPG 18 allgemein, Zonenkonforme Bauten und Anlagen in Spezialzonen (Deponie, Sport, u.ä. ohne Weiler, Erhaltungszonen) (BaB)": "spezialzonen",
    "RPG 18 RPV 33 Zonenkonforme Bauten und Anlagen in Weiler- oder Erhaltungszonen u.ä. (BaB)": "erhaltungszonen",
    "RPG 18a Solaranlagen (BaB)": "solaranlagen",
    "RPG 22 allgemein zonenkonform (BaB)": "allgemein-zonenkonform",
    "RPG 24 Standortgebundene Bauten und Anlagen (BaB)": "standortgebunden",
    "RPG 24 RPV 39 1 Vollständige Zweckänderung von Bauten in Streusiedlungsgebieten (BaB)": "streusiedlungsgebiet",
    "RPG 24 RPV 39 2 Vollständige Zweckänderung landschaftsprägender Bauten (BaB)": "landschaftspraegende-bauten",
    "RPG 24a Zweckänderung ohne bauliche Massnahmen (BaB)": "ohne-bauliche-massnahmen",
    "RPG 24b 1 Nichtlandwirtschaftliche Nebenbetriebe zur Existenzsicherung (BaB)": "existenzsicherung",
    "RPG 24b 1 bis Nichtlandw. Nebenbetriebe mit engem Bezug zu landw. Gewerbe (BaB)": "nebenbetriebe",
    "RPG 24b 1 ter Nichtlandw. Nebenbetriebe in temporären Betriebszentren (BaB)": "temp-betriebszentren",
    "RPG 24c RPV 42 Änderung zonenwidrig gewordener Bauten und Anlagen (BaB)": "zonenwidrig",
    "RPG 24d 1 RPV 42a Änderungen an ehemals landwirtschaftlich genutzten Wohnbauten (BaB)": "landwirtschaftliche-wohnbauten",
    "RPG 24e 1 Hobbymässige Tierhaltung in nahe bei der Bauzone gelegenen Gebäuden (BaB)": "hobby-tierhaltung-bauzone",
    "RPG 24e 2-4 Aussenanlagen zur hobbymässigen Tierhaltung (BaB)": "hobby-tierhaltung-aussenanlagen",
    "RPG 24d 2 Vollständige Zweckänderung geschützter Bauten (BaB)": "geschuetzte-bauten",
    "RPV 32c Standortgebundene Solaranlagen ausserhalb der Bauzonen (BaB)": "solaranlagen-ausserhalb-bauzone",
    "RPG 37a RPV 43 Änderung zonenwidrig gewordener gewerblicher Bauten (BaB)": "zonenwidrige-gewerbliche-bauten",
    "BGBB 4a VBB Abparzellierung von Bauten und Anlagen, Feststellungsverfügung (BaB)": "abparzellierung",
    "Andere Dossiers (BaB)": "andere-dossiers",
}

BAB_TYPE_OF_CLIENT = {
    "SBB (Schweizerische Bundesbahnen) (BaB)": "sbb",
    "VBS (Eidg. Departement für Verteidigung, Bevölkerungsschutz und Sport) (BaB)": "vbs",
    "BBL (Bundesamt für Bauten und Logistik) (BaB)": "bbl",
    "ASTRA (Bundesamt für Strassen) (BaB)": "astra",
    "Swisscom (BaB)": "swisscom",
    "Die Post (BaB)": "post",
    "Kanton (z.B. ARE BD, ohne öffentliche Unternehmen) (BaB)": "kanton-nicht-oeffentlich",
    "Kanton (öffentliche Unternehmen des Kantons, z.B. Spital) (BaB)": "kanton-oeffentlich",
    "Gemeinden (inkl. Korporationen Bürgergemeinden und Alpgenossenschaften) (BaB)": "gemeinde-inkl-kooperationen",
    "Gemeinden (öffentliche Unternehmen Gemeinde, z.B. Wasserwerke, Elektrizitästwerke) (BaB)": "gemeinden-oeffentlich",
    "Versicherungsgesellschaften (BaB)": "versicherungsgesellschaften",
    "Personalfürsorgestiftungen (Pensionskassen) (BaB)": "personalfuersorgestiftungen",
    "Krankenkassen, SUVA (BaB)": "krankenkassen",
    "Banken (BaB)": "banken",
    "Elektrizitätswerke (ausgenommen gemeindeeigene Werke) (BaB)": "elektrizitaetswerke",
    "Gaswerke (BaB)": "gaswerke",
    "Privatbahnen (BaB)": "privatbahnen",
    "Immobilienbranche (AG, GmbH, Genossenschaft) (BaB)": "immobilienbranche",
    "Privatpersonen (inkl. Erbengemeinschaften) (BaB)": "privatpersonen",
    "Einzelfirmen oder Personengesellschaften (BaB)": "einzelfirmen",
    "Kapitalgesellschaften (AG, GmbH, Genossenschaft) (BaB)": "kapitalgesellschaft",
    "Andere private Auftraggeber (z.B. SAC Sektionen, Kirchgemeinden, Stiftungen, Vereine) (BaB)": "andere-private-auftraggeber",
    "Internationale Organisationen, Botschaften (BaB)": "internationale-organisationen",
    "Immobilienbranche (Einzelpersonen oder Personengesellschaften) (BaB)": "immobilienbranche",
    "Immobilienbranche (Wohnbaugenossenschaften) (BaB)": "immobilienbranche",
    "Bundesamt für Umweltschutz (BaB)": "bundesamt-fuer-umweltschutz",
}


class Command(BaseCommand):
    help = """Create a csv with statistics about instances"""

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        cases = Case.objects.filter(
            Q(**{"meta__submit-date__isnull": False})
            & Q(instance__isnull=False)
            & Q(instance__location__isnull=False)
        )

        data = []
        for counter, case in enumerate(cases):
            flat_answers = case.document.flat_answer_map()
            table_answer = flat_answers.get("gebaeude")

            entry = {
                "Jahr": case.meta["submit-date"][:4],
                "Gemeinde": case.instance.location.name,
                "Umschreibung Bauprojekt": CalumaApi().get_answer_value(
                    "proposal-description", case.instance
                ),
            }

            for name, (key, expected) in CATEGORIES.items():
                entry[name] = (
                    1
                    if flat_answers.get(key) and expected in flat_answers.get(key)
                    else ""
                )

            if table_answer and table_answer[0]:
                self.get_amount_of_answers(
                    entry, BUILDING_TYPES, table_answer[0], "art-der-hochbaute"
                )
                self.get_amount_of_answers(
                    entry, PROPOSALS, table_answer[0], "proposal"
                )
                self.get_amount_of_answers(
                    entry, RECONSTRUCTION, table_answer[0], "umbau"
                )

            bab_work_item = case.work_items.filter(task_id="bab").first()
            if not bab_work_item:
                continue
            bab_answers = bab_work_item.document.answers

            self.get_amount_of_answers_bab(
                entry, BAB_TYPE_OF_MEASURE, bab_answers, "bab-art-der-massnahme"
            )
            self.get_amount_of_answers_bab(
                entry, BAB_TYPE_OF_OBJECT, bab_answers, "bab-objektart"
            )
            self.get_amount_of_answers_bab(
                entry, BAB_LEGAL_BASIS, bab_answers, "bab-bewilligungsgrund"
            )
            self.get_amount_of_answers_bab(
                entry, BAB_TYPE_OF_CLIENT, bab_answers, "bab-typ-der-auftraggeber"
            )

            self.stdout.write(f"Prepared {counter} query")
            data.append(entry)
        self.generate_csv(data)

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def generate_csv(self, data):
        with open("statistic.csv", "w", newline="") as csvfile:
            fieldnames = [
                "Jahr",
                "Gemeinde",
                "Umschreibung Bauprojekt",
                "Hochbau",
                "Beheizte oder gekühlte Neu- und Umbauten",
                "Die Änderung der Gebäudehülle beheizter oder gekühlter Bauten",
                "Die Installation / Änderung gebäudetechnischer Anlagen (Heizung, Lüftung, Klima- und / oder Kälteanlage)",
                "Einfamilienhaus freistehend",
                "Einfamilienhaus angebaut",
                "Mehrfamilienhaus",
                "Wohn- und Geschäftshaus",
                "Industrie und Gewerbebaute",
                "Kaufhaus, Geschäftsgebäude",
                "Garage / Einstellhallen im Zusammenhang mit Wohngebäuden",
                "Parkhaus",
                "Hotel, Restaurant, Beherbergungsbetrieb",
                "Heim mit Unterkunft, Pflegedienst und Betreuung",
                "Wohnheim ohne Pflegedienste und Betreuung",
                "Spital",
                "Schulen",
                "Sporthallen, Sportplätze",
                "Freizeit- und Tourismusanlagen",
                "Kirchen und Sakralbauten",
                "Kulturbauten, Museen, etc.",
                "Landwirtschaftliche Ökonomiegebäude mit Tierhaltung",
                "Landwirtschaftliche Ökonomiegebäude ohne Tierhaltung",
                "Landwirtschaftliche Betriebsgebäude mit Wohnteil",
                "Forstwirtschaftliche Bauten und Anlagen",
                "Energieholzlager",
                "Materiallager",
                "Brennstofflager",
                "Silo / Zisterne",
                "Reklamebauten",
                "Kommunikationsanlagen (Mobilfunk-, Richtfunkanlagen)",
                "Kehrichtentsorgungsanlagen",
                "Andere",
                "Neubau",
                "Umbau",
                "Abbruch",
                "Energetische Sanierung",
                "Sanierung Heizsystem",
                "Photovoltaische Solaranlage",
                "Neubau (BaB)",
                "Umbau / Anbau (BaB)",
                "Sanierung (BaB)",
                "Zweckänderung (BaB)",
                "Abbruch (BaB)",
                "Andere (BaB)",
                "Abparzellierung Veräusserung Betriebsübergabe (BaB)",
                "Ersatzneubau (BaB)",
                "Wohnbaute (BaB)",
                "Wohn- / Ökonomiebaute (BaB)",
                "Gewerbebaute mit Arbeitsplätzen (BaB)",
                "Gewerbebaute ohne Arbeitsplätzen (BaB)",
                "Ökonomiebaute mit Tierhaltung (BaB)",
                "Ökonomiebaute ohne Tierhaltung (BaB)",
                "Terrainveränderung (BaB)",
                "Viehtriebweg (BaB)",
                "Bewirtschaftungsweg (BaB)",
                "Hof- / Gütererschliessung (BaB)",
                "Andere (BaB)",
                "Fahrnisbauten (BaB)",
                "Wanderweg (BaB)",
                "Betrieb Gewerbe Liegenschaften (BaB)",
                "Innerhalb Bauzone (BaB)",
                "RPG 16a RPV 34 1 Ökonomiebauten für die bodenabhängige Landwirtschaft (BaB)",
                "RPG 16a 1 RPV 34 2 Landwirtschaftliche Bauten: Aufbereitung Lagerung und Verkauf (BaB)",
                "RPG 16a 1 RPV 34 3 Wohnbauten für landwirtschaftliche Gewerbe (BaB)",
                "RPG 16a RPV 35 Gemeinschaftliche Stallbauten (BaB)",
                "RPG 16a 2 RPV 36 Innere Aufstockung Tierhaltung (Schweineställe, Geflügelhallen) (BaB)",
                "RPG 16a 2 RPV 37 Innere Aufstockung Gemüse- und Pflanzenbau (Gewächshäuser) (BaB)",
                "RPG 16a 3 RPV 38 Bauten und Anlagen in Speziallandwirtschaftszonen (BaB)",
                "RPG 16a 1 RPV 34a Gewinnung von Energie aus Biomasse (BaB)",
                "RPG 17 allgemein, Zonenkonforme Bauten und Anlagen in Schutzzonen (BaB)",
                "RPG 18 allgemein, Zonenkonforme Bauten und Anlagen in Spezialzonen (Deponie, Sport, u.ä. ohne Weiler, Erhaltungszonen) (BaB)",
                "RPG 18 RPV 33 Zonenkonforme Bauten und Anlagen in Weiler- oder Erhaltungszonen u.ä. (BaB)",
                "RPG 18a Solaranlagen (BaB)",
                "RPG 22 allgemein zonenkonform (BaB)",
                "RPG 24 Standortgebundene Bauten und Anlagen (BaB)",
                "RPG 24 RPV 39 1 Vollständige Zweckänderung von Bauten in Streusiedlungsgebieten (BaB)",
                "RPG 24 RPV 39 2 Vollständige Zweckänderung landschaftsprägender Bauten (BaB)",
                "RPG 24a Zweckänderung ohne bauliche Massnahmen (BaB)",
                "RPG 24b 1 Nichtlandwirtschaftliche Nebenbetriebe zur Existenzsicherung (BaB)",
                "RPG 24b 1 bis Nichtlandw. Nebenbetriebe mit engem Bezug zu landw. Gewerbe (BaB)",
                "RPG 24b 1 ter Nichtlandw. Nebenbetriebe in temporären Betriebszentren (BaB)",
                "RPG 24c RPV 42 Änderung zonenwidrig gewordener Bauten und Anlagen (BaB)",
                "RPG 24d 1 RPV 42a Änderungen an ehemals landwirtschaftlich genutzten Wohnbauten (BaB)",
                "RPG 24e 1 Hobbymässige Tierhaltung in nahe bei der Bauzone gelegenen Gebäuden (BaB)",
                "RPG 24e 2-4 Aussenanlagen zur hobbymässigen Tierhaltung (BaB)",
                "RPG 24d 2 Vollständige Zweckänderung geschützter Bauten (BaB)",
                "RPV 32c Standortgebundene Solaranlagen ausserhalb der Bauzonen (BaB)",
                "RPG 37a RPV 43 Änderung zonenwidrig gewordener gewerblicher Bauten (BaB)",
                "BGBB 4a VBB Abparzellierung von Bauten und Anlagen, Feststellungsverfügung (BaB)",
                "Andere Dossiers (BaB)",
                "SBB (Schweizerische Bundesbahnen) (BaB)",
                "VBS (Eidg. Departement für Verteidigung, Bevölkerungsschutz und Sport) (BaB)",
                "BBL (Bundesamt für Bauten und Logistik) (BaB)",
                "ASTRA (Bundesamt für Strassen) (BaB)",
                "Swisscom (BaB)",
                "Die Post (BaB)",
                "Kanton (z.B. ARE BD, ohne öffentliche Unternehmen) (BaB)",
                "Kanton (öffentliche Unternehmen des Kantons, z.B. Spital) (BaB)",
                "Gemeinden (inkl. Korporationen Bürgergemeinden und Alpgenossenschaften) (BaB)",
                "Gemeinden (öffentliche Unternehmen Gemeinde, z.B. Wasserwerke, Elektrizitästwerke) (BaB)",
                "Versicherungsgesellschaften (BaB)",
                "Personalfürsorgestiftungen (Pensionskassen) (BaB)",
                "Krankenkassen, SUVA (BaB)",
                "Banken (BaB)",
                "Elektrizitätswerke (ausgenommen gemeindeeigene Werke) (BaB)",
                "Gaswerke (BaB)",
                "Privatbahnen (BaB)",
                "Immobilienbranche (AG, GmbH, Genossenschaft) (BaB)",
                "Privatpersonen (inkl. Erbengemeinschaften) (BaB)",
                "Einzelfirmen oder Personengesellschaften (BaB)",
                "Kapitalgesellschaften (AG, GmbH, Genossenschaft) (BaB)",
                "Andere private Auftraggeber (z.B. SAC Sektionen, Kirchgemeinden, Stiftungen, Vereine) (BaB)",
                "Internationale Organisationen, Botschaften (BaB)",
                "Immobilienbranche (Einzelpersonen oder Personengesellschaften) (BaB)",
                "Immobilienbranche (Wohnbaugenossenschaften) (BaB)",
                "Bundesamt für Umweltschutz (BaB)",
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def get_amount_of_answers(self, entry, mapping, table_answer, slug):
        for name, key in mapping.items():
            entry[name] = (
                1 if table_answer.get(slug) and key in table_answer.get(slug) else ""
            )

    def get_amount_of_answers_bab(self, entry, mapping, answers, slug):
        for name, key in mapping.items():
            entry[name] = 1 if answers.filter(value=f"{slug}-{key}") else ""
