import csv

from caluma.caluma_workflow.models import Case
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from camac.caluma.api import CalumaApi

caluma_api = CalumaApi()

SINGLE_CHOICE_QUESTIONS = {
    # Art der Massnahme
    "Art der Massnahme: Neubau": (
        "bab-art-der-massnahme",
        "bab-art-der-massnahme-neubau",
    ),
    "Art der Massnahme: Umbau / Anbau": (
        "bab-art-der-massnahme",
        "bab-art-der-massnahme-umbau-anbau",
    ),
    "Art der Massnahme: Sanierung": (
        "bab-art-der-massnahme",
        "bab-art-der-massnahme-sanierung",
    ),
    "Art der Massnahme: Zweckänderung": (
        "bab-art-der-massnahme",
        "bab-art-der-massnahme-zweckaenderung",
    ),
    "Art der Massnahme: Abbruch": (
        "bab-art-der-massnahme",
        "bab-art-der-massnahme-abbruch",
    ),
    "Art der Massnahme: Andere": (
        "bab-art-der-massnahme",
        "bab-art-der-massnahme-andere",
    ),
    "Art der Massnahme: Abparzellierung Veräusserung Betriebsübergabe": (
        "bab-art-der-massnahme",
        "bab-art-der-massnahme-abparzellierung",
    ),
    "Art der Massnahme: Ersatzneubau": (
        "bab-art-der-massnahme",
        "bab-art-der-massnahme-ersatzneubau",
    ),
    # Objektart
    "Objektart: Wohnbaute": ("bab-objektart", "bab-objektart-wohnbaute"),
    "Objektart: Wohn- / Ökonomiebaute": (
        "bab-objektart",
        "bab-objektart-wohn-oekonomiebaute",
    ),
    "Objektart: Gewerbebaute mit Arbeitsplätzen": (
        "bab-objektart",
        "bab-objektart-gewerbebaute-mit-arbeitsplaetzen",
    ),
    "Objektart: Gewerbebaute ohne Arbeitsplätzen": (
        "bab-objektart",
        "bab-objektart-gewerbebaute-ohne-arbeitsplaetzen",
    ),
    "Objektart: Ökonomiebaute mit Tierhaltung": (
        "bab-objektart",
        "bab-objektart-oekonomiebaute-mit-tierhaltung",
    ),
    "Objektart: Ökonomiebaute ohne Tierhaltung": (
        "bab-objektart",
        "bab-objektart-oekonomiebaute-ohne-tierhaltung",
    ),
    "Objektart: Terrainveränderung": (
        "bab-objektart",
        "bab-objektart-terrainveraenderung",
    ),
    "Objektart: Viehtriebweg": ("bab-objektart", "bab-objektart-viehtriebweg"),
    "Objektart: Bewirtschaftungsweg": (
        "bab-objektart",
        "bab-objektart-bewirtschaftungsweg",
    ),
    "Objektart: Hof- / Gütererschliessung": (
        "bab-objektart",
        "bab-objektart-hof-guetererschliessung",
    ),
    "Objektart: Objektart Andere": ("bab-objektart", "bab-objektart-andere"),
    "Objektart: Fahrnisbauten": ("bab-objektart", "bab-objektart-fahrnisbauten"),
    "Objektart: Wanderweg": ("bab-objektart", "bab-objektart-wanderweg"),
    "Objektart: Betrieb Gewerbe Liegenschaften": (
        "bab-objektart",
        "bab-objektart-betrieb-gewerbe-liegenschaften",
    ),
    # Nutzung nach RPG
    "Nutzung nach RPG: Zonenkonform": (
        "bab-nutzung-nach-rpg",
        "bab-nutzung-nach-rpg-zonenkonform",
    ),
    "Nutzung nach RPG: Ausnahmebewilligung": (
        "bab-nutzung-nach-rpg",
        "bab-nutzung-nach-rpg-ausnahmebewilligung",
    ),
    "Nutzung nach RPG: Andere": ("bab-nutzung-nach-rpg", "bab-nutzung-nach-rpg-andere"),
    # Bewilligungsgrund - Rechtliche Grundlage
    "Bewilligungsgrund - Rechtliche Grundlage: Innerhalb Bauzone": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-innerhalb-bauzone",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 16a RPV 34 1 Ökonomiebauten für die bodenabhängige Landwirtschaft": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-oekonomiebauten",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 16a 1 RPV 34 2 Landwirtschaftliche Bauten: Aufbereitung Lagerung und Verkauf": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-landwirtschaftliche-bauten",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 16a 1 RPV 34 3 Wohnbauten für landwirtschaftliche Gewerbe": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-wohnbauten",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 16a RPV 35 Gemeinschaftliche Stallbauten": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-stallbauten",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 16a 2 RPV 36 Innere Aufstockung Tierhaltung (Schweineställe, Geflügelhallen)": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-tierhaltung",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 16a 2 RPV 37 Innere Aufstockung Gemüse- und Pflanzenbau (Gewächshäuser)": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-gewaechshaeuser",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 16a 3 RPV 38 Bauten und Anlagen in Speziallandwirtschaftszonen": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-speziallandwirtschaftszonen",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 16a 1 RPV 34a Gewinnung von Energie aus Biomasse": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-biomasse",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 17 allgemein, Zonenkonforme Bauten und Anlagen in Schutzzonen": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-zonenkonform",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 18 allgemein, Zonenkonforme Bauten und Anlagen in Spezialzonen (Deponie, Sport, u.ä. ohne Weiler, Erhaltungszonen)": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-spezialzonen",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 18 RPV 33 Zonenkonforme Bauten und Anlagen in Weiler- oder Erhaltungszonen u.ä.": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-erhaltungszonen",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 18a Solaranlagen": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-solaranlagen",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 22 allgemein zonenkonform": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-allgemein-zonenkonform",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 24 Standortgebundene Bauten und Anlagen": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-standortgebunden",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 24 RPV 39 1 Vollständige Zweckänderung von Bauten in Streusiedlungsgebieten": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-streusiedlungsgebiet",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 24 RPV 39 2 Vollständige Zweckänderung landschaftsprägender Bauten": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-landschaftspraegende",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 24a Zweckänderung ohne bauliche Massnahmen": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-ohne-bauliche-massnahmen",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 24b 1 Nichtlandwirtschaftliche Nebenbetriebe zur Existenzsicherung": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-existenzsicherung",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 24b 1 bis Nichtlandw. Nebenbetriebe mit engem Bezug zu landw. Gewerbe": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-nebenbetriebe",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 24b 1 ter Nichtlandw. Nebenbetriebe in temporären Betriebszentren": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-temp-betriebszentren",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 24c RPV 42 Änderung zonenwidrig gewordener Bauten und Anlagen": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-zonenwidrig",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 24d 1 RPV 42a Änderungen an ehemals landwirtschaftlich genutzten Wohnbauten": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-landwirtschaftliche",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 24e 1 Hobbymässige Tierhaltung in nahe bei der Bauzone gelegenen Gebäuden": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-hobby-tierhaltung-bauzone",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 24e 2-4 Aussenanlagen zur hobbymässigen Tierhaltung": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-hobby-tierhaltung-aussenanlagen",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 24d 2 Vollständige Zweckänderung geschützter Bauten": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-geschuetzte-bauten",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPV 32c Standortgebundene Solaranlagen ausserhalb der Bauzonen": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-solaranlagen-ausserhalb-bauzone",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: RPG 37a RPV 43 Änderung zonenwidrig gewordener gewerblicher Bauten": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-zonenwidrige-gewerbliche-bauten",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: BGBB 4a VBB Abparzellierung von Bauten und Anlagen, Feststellungsverfügung": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-abparzellierung",
    ),
    "Bewilligungsgrund - Rechtliche Grundlage: Andere Dossiers": (
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-andere-dossiers",
    ),
    # Entscheid
    "Entscheid: Positiv": ("bab-entscheid", "bab-entscheid-positiv"),
    "Entscheid: Negativ": ("bab-entscheid", "bab-entscheid-negativ"),
    "Entscheid: Andere": ("bab-entscheid", "bab-entscheid-andere"),
    # Typ der Auftraggeber - Gesuchsteller
    "Typ der Auftraggeber - Gesuchsteller: SBB (Schweizerische Bundesbahnen)": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-sbb",
    ),
    "Typ der Auftraggeber - Gesuchsteller: VBS (Eidg. Departement für Verteidigung, Bevölkerungsschutz und Sport)": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-vbs",
    ),
    "Typ der Auftraggeber - Gesuchsteller: BBL (Bundesamt für Bauten und Logistik)": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-bbl",
    ),
    "Typ der Auftraggeber - Gesuchsteller: ASTRA (Bundesamt für Strassen)": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-astra",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Swisscom": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-swisscom",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Die Post": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-post",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Kanton (z.B. ARE BD, ohne öffentliche Unternehmen)": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-kanton-nicht-oeffentlich",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Kanton (öffentliche Unternehmen des Kantons, z.B. Spital)": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-kanton-oeffentlich",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Gemeinden (inkl. Korporationen Bürgergemeinden und Alpgenossenschaften)": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-gemeinde-inkl-kooperationen",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Gemeinden (öffentliche Unternehmen Gemeinde, z.B. Wasserwerke, Elektrizitästwerke)": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-gemeinden-oeffentlich",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Versicherungsgesellschaften": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-versicherungsgesellschaften",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Personalfürsorgestiftungen (Pensionskassen)": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-personalfuersorgestiftungen",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Krankenkassen, SUVA": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-krankenkassen",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Banken": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-banken",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Elektrizitätswerke (ausgenommen gemeindeeigene Werke)": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-elektrizitaetswerke",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Gaswerke": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-gaswerke",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Privatbahnen": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-privatbahnen",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Immobilienbranche (AG, GmbH, Genossenschaft)": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-immobilienbranche",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Privatpersonen (inkl. Erbengemeinschaften)": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-privatpersonen",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Einzelfirmen oder Personengesellschaften": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-einzelfirmen",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Kapitalgesellschaften (AG, GmbH, Genossenschaft)": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-kapitalgesellschaft",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Andere private Auftraggeber (z.B. SAC Sektionen, Kirchgemeinden, Stiftungen, Vereine)": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-andere-private-auftraggeber",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Internationale Organisationen, Botschaften": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-internationale-organisationen",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Immobilienbranche (Einzelpersonen oder Personengesellschaften)": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-immobilienbranche-einzelpersonen",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Immobilienbranche (Wohnbaugenossenschaften)": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-immobilienbranche-wohnbaugenossenschaften",
    ),
    "Typ der Auftraggeber - Gesuchsteller: Bundesamt für Umweltschutz": (
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-bundesamt-fuer-umweltschutz",
    ),
    # Stabilisierungsziel
    "Stabilisierungsziel: Nicht relevant (Tourismus und Landwirtschaft)": (
        "bab-stabilisierungsziel",
        "bab-stabilisierungsziel-nicht-relevant",
    ),
    "Stabilisierungsziel: Relevant": (
        "bab-stabilisierungsziel",
        "bab-stabilisierungsziel-relevant",
    ),
    "Stabilisierungsziel: Nicht relevant (Bauten / Flächen altrechtlich bestehend)": (
        "bab-stabilisierungsziel",
        "bab-stabilisierungsziel-altrechtlich-bestehend",
    ),
    "Stabilisierungsziel: Nicht relevant (keine neuen ver- oder entsiegelten Flächen)": (
        "bab-stabilisierungsziel",
        "bab-stabilisierungsziel-keine-neuen-ver-oder-entsiegelten-flaechen",
    ),
}

GRUNDNUTZUNG = {
    "Landwirtschaftszone": "bab-grundnutzung-landwirtschaftszone",
    "Reservezone": "bab-grundnutzung-reservezone",
    "Wald": "bab-grundnutzung-wald",
    "Weilerzone": "bab-grundnutzung-weilerzone",
    "Freihaltezone": "bab-grundnutzung-freihaltezone",
    "Verkehrsflächen aBZ": "bab-grundnutzung-verkehrsflaechen-abz",
    "Andere": "bab-grundnutzung-andere",
}

ART_DER_VERSIEGELUNG = {
    "Neue versiegelte Flächen (Gebäude)": "neu-versiegelt-gebaeude",
    "Neue versiegelte Flächen (Umgebung)": "neu-versiegelt-umgebung",
    "Neue versiegelte Flächen (Erschliessung)": "neu-versiegelt-erschliessung",
    "Entsiegelte / renaturierte Flächen (Gebäude)": "entsiegelt-gebaeude",
    "Entsiegelte / renaturierte Flächen (Umgebung)": "entsiegelt-umgebung",
    "Entsiegelte / renaturierte Flächen (Erschliessung)": "entsiegelt-erschliessung",
}

NUTZUNG_DER_VERSIEGELTEN_FLAECHEN = {
    "Landwirtschaft": "landwirtschaft",
    "Tourismus": "tourismus",
    "Energie": "energie",
    "Verkehr (kantonale und nationale Projekte)": "verkehr",
    "Wald (Projekte für die Waldbewirtschaftung)": "wald",
    "Andere": "andere",
}

TEXT_QUESTIONS_OR_INTEGER_QUESTIONS = [
    ("Beschrieb der Massnahme", "beschrieb-der-massnahme"),
    ("Objektbeschrieb", "objektbeschrieb"),
    ("Flächenbedarf Fruchtfolgeflächen (m²)", "bab-flachenbedarf-fruchtfolgeflaechen"),
    ("Kompensation Fruchtfolgeflächen (m²)", "bab-kompensation-fruchtfolgeflaechen"),
    ("Anzahl neue Gebäude", "bab-neue-gebaeude"),
    ("Anzahl Gebäude die abgebrochen werden", "bab-gebaeude-abbruch"),
]


class Command(BaseCommand):
    help = """Create a csv with bab statistics about instances"""

    @transaction.atomic
    def handle(self, *args, **options):
        cases = Case.objects.filter(
            Q(**{"meta__submit-date__isnull": False})
            & Q(instance__isnull=False)
            & Q(instance__location__isnull=False)
            & Q(work_items__task_id="bab")
        )

        data = []
        for counter, case in enumerate(cases):
            flat_answers = (
                case.work_items.filter(task_id="bab").first().document.flat_answer_map()
            )
            space_requirement_table_answer = flat_answers.get(
                "bab-lage-flaechenbedarf-tabelle"
            )
            sealed_space_table_answer = flat_answers.get(
                "versiegelte-entsiegelte-flaechen"
            )

            entry = {
                "Instance": case.instance.pk,
                "Jahr": case.meta["submit-date"][:4],
                "Gemeinde": case.instance.location.name,
            }

            for name, (key, expected) in SINGLE_CHOICE_QUESTIONS.items():
                entry[name] = (
                    1
                    if flat_answers.get(key) and expected in flat_answers.get(key)
                    else ""
                )

            for label, slug in TEXT_QUESTIONS_OR_INTEGER_QUESTIONS:
                entry[label] = flat_answers.get(slug)

            if space_requirement_table_answer and space_requirement_table_answer[0]:
                for i, row in enumerate(space_requirement_table_answer):
                    self.get_amount_of_single_choice_answers(
                        entry, GRUNDNUTZUNG, row, "bab-grundnutzung", "Grundnutzung", i
                    )

                self.get_total_int_and_str_table_values(
                    entry,
                    space_requirement_table_answer,
                    "bab-flaechenbedarf-grundnutzung",
                    "Flächenbedarf nach Grundnutzung (m²)",
                )

            if sealed_space_table_answer and sealed_space_table_answer[0]:
                for i, row in enumerate(sealed_space_table_answer):
                    self.get_amount_of_single_choice_answers(
                        entry,
                        ART_DER_VERSIEGELUNG,
                        row,
                        "bab-art-versiegelung",
                        "Art der Ver- bzw. Entsiegelung",
                        i,
                    )
                    self.get_amount_of_single_choice_answers(
                        entry,
                        NUTZUNG_DER_VERSIEGELTEN_FLAECHEN,
                        row,
                        "bab-nutzung-versiegelte-flaeche",
                        "Nutzung der versiegelten Flächen",
                        i,
                    )

                self.get_total_int_and_str_table_values(
                    entry,
                    sealed_space_table_answer,
                    "bab-versiegelung-flaeche",
                    "Fläche (m²)",
                )
                self.get_total_int_and_str_table_values(
                    entry,
                    sealed_space_table_answer,
                    "bab-beschreibung-nutzung-versiegelte-flaeche-andere",
                    "Beschreibung",
                )

            self.stdout.write(f"Prepared {counter} query")
            data.append(entry)
        self.generate_csv(data)

    def generate_csv(self, data):
        with open("bab_statistic.csv", "w", newline="") as csvfile:
            fieldnames = [
                "Instance",
                "Jahr",
                "Gemeinde",
                # Art der Massnahme
                "Art der Massnahme: Neubau",
                "Art der Massnahme: Umbau / Anbau",
                "Art der Massnahme: Sanierung",
                "Art der Massnahme: Zweckänderung",
                "Art der Massnahme: Abbruch",
                "Art der Massnahme: Andere",
                "Art der Massnahme: Abparzellierung Veräusserung Betriebsübergabe",
                "Art der Massnahme: Ersatzneubau",
                "Beschrieb der Massnahme",
                # Objektart
                "Objektart: Wohnbaute",
                "Objektart: Wohn- / Ökonomiebaute",
                "Objektart: Gewerbebaute mit Arbeitsplätzen",
                "Objektart: Gewerbebaute ohne Arbeitsplätzen",
                "Objektart: Ökonomiebaute mit Tierhaltung",
                "Objektart: Ökonomiebaute ohne Tierhaltung",
                "Objektart: Terrainveränderung",
                "Objektart: Viehtriebweg",
                "Objektart: Bewirtschaftungsweg",
                "Objektart: Hof- / Gütererschliessung",
                "Objektart: Objektart Andere",
                "Objektart: Fahrnisbauten",
                "Objektart: Wanderweg",
                "Objektart: Betrieb Gewerbe Liegenschaften",
                "Objektbeschrieb",
                # Nutzung nach RPG
                "Nutzung nach RPG: Zonenkonform",
                "Nutzung nach RPG: Ausnahmebewilligung",
                "Nutzung nach RPG: Andere",
                # Bewilligungsgrund - Rechtliche Grundlage
                "Bewilligungsgrund - Rechtliche Grundlage: Innerhalb Bauzone",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 16a RPV 34 1 Ökonomiebauten für die bodenabhängige Landwirtschaft",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 16a 1 RPV 34 2 Landwirtschaftliche Bauten: Aufbereitung Lagerung und Verkauf",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 16a 1 RPV 34 3 Wohnbauten für landwirtschaftliche Gewerbe",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 16a RPV 35 Gemeinschaftliche Stallbauten",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 16a 2 RPV 36 Innere Aufstockung Tierhaltung (Schweineställe, Geflügelhallen)",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 16a 2 RPV 37 Innere Aufstockung Gemüse- und Pflanzenbau (Gewächshäuser)",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 16a 3 RPV 38 Bauten und Anlagen in Speziallandwirtschaftszonen",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 16a 1 RPV 34a Gewinnung von Energie aus Biomasse",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 17 allgemein, Zonenkonforme Bauten und Anlagen in Schutzzonen",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 18 allgemein, Zonenkonforme Bauten und Anlagen in Spezialzonen (Deponie, Sport, u.ä. ohne Weiler, Erhaltungszonen)",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 18 RPV 33 Zonenkonforme Bauten und Anlagen in Weiler- oder Erhaltungszonen u.ä.",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 18a Solaranlagen",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 22 allgemein zonenkonform",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 24 Standortgebundene Bauten und Anlagen",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 24 RPV 39 1 Vollständige Zweckänderung von Bauten in Streusiedlungsgebieten",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 24 RPV 39 2 Vollständige Zweckänderung landschaftsprägender Bauten",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 24a Zweckänderung ohne bauliche Massnahmen",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 24b 1 Nichtlandwirtschaftliche Nebenbetriebe zur Existenzsicherung",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 24b 1 bis Nichtlandw. Nebenbetriebe mit engem Bezug zu landw. Gewerbe",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 24b 1 ter Nichtlandw. Nebenbetriebe in temporären Betriebszentren",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 24c RPV 42 Änderung zonenwidrig gewordener Bauten und Anlagen",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 24d 1 RPV 42a Änderungen an ehemals landwirtschaftlich genutzten Wohnbauten",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 24e 1 Hobbymässige Tierhaltung in nahe bei der Bauzone gelegenen Gebäuden",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 24e 2-4 Aussenanlagen zur hobbymässigen Tierhaltung",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 24d 2 Vollständige Zweckänderung geschützter Bauten",
                "Bewilligungsgrund - Rechtliche Grundlage: RPV 32c Standortgebundene Solaranlagen ausserhalb der Bauzonen",
                "Bewilligungsgrund - Rechtliche Grundlage: RPG 37a RPV 43 Änderung zonenwidrig gewordener gewerblicher Bauten",
                "Bewilligungsgrund - Rechtliche Grundlage: BGBB 4a VBB Abparzellierung von Bauten und Anlagen, Feststellungsverfügung",
                "Bewilligungsgrund - Rechtliche Grundlage: Andere Dossiers",
                # Entscheid
                "Entscheid: Positiv",
                "Entscheid: Negativ",
                "Entscheid: Andere",
                # Typ der Auftraggeber - Gesuchsteller
                "Typ der Auftraggeber - Gesuchsteller: SBB (Schweizerische Bundesbahnen)",
                "Typ der Auftraggeber - Gesuchsteller: VBS (Eidg. Departement für Verteidigung, Bevölkerungsschutz und Sport)",
                "Typ der Auftraggeber - Gesuchsteller: BBL (Bundesamt für Bauten und Logistik)",
                "Typ der Auftraggeber - Gesuchsteller: ASTRA (Bundesamt für Strassen)",
                "Typ der Auftraggeber - Gesuchsteller: Swisscom",
                "Typ der Auftraggeber - Gesuchsteller: Die Post",
                "Typ der Auftraggeber - Gesuchsteller: Kanton (z.B. ARE BD, ohne öffentliche Unternehmen)",
                "Typ der Auftraggeber - Gesuchsteller: Kanton (öffentliche Unternehmen des Kantons, z.B. Spital)",
                "Typ der Auftraggeber - Gesuchsteller: Gemeinden (inkl. Korporationen Bürgergemeinden und Alpgenossenschaften)",
                "Typ der Auftraggeber - Gesuchsteller: Gemeinden (öffentliche Unternehmen Gemeinde, z.B. Wasserwerke, Elektrizitästwerke)",
                "Typ der Auftraggeber - Gesuchsteller: Versicherungsgesellschaften",
                "Typ der Auftraggeber - Gesuchsteller: Personalfürsorgestiftungen (Pensionskassen)",
                "Typ der Auftraggeber - Gesuchsteller: Krankenkassen, SUVA",
                "Typ der Auftraggeber - Gesuchsteller: Banken",
                "Typ der Auftraggeber - Gesuchsteller: Elektrizitätswerke (ausgenommen gemeindeeigene Werke)",
                "Typ der Auftraggeber - Gesuchsteller: Gaswerke",
                "Typ der Auftraggeber - Gesuchsteller: Privatbahnen",
                "Typ der Auftraggeber - Gesuchsteller: Immobilienbranche (AG, GmbH, Genossenschaft)",
                "Typ der Auftraggeber - Gesuchsteller: Privatpersonen (inkl. Erbengemeinschaften)",
                "Typ der Auftraggeber - Gesuchsteller: Einzelfirmen oder Personengesellschaften",
                "Typ der Auftraggeber - Gesuchsteller: Kapitalgesellschaften (AG, GmbH, Genossenschaft)",
                "Typ der Auftraggeber - Gesuchsteller: Andere private Auftraggeber (z.B. SAC Sektionen, Kirchgemeinden, Stiftungen, Vereine)",
                "Typ der Auftraggeber - Gesuchsteller: Internationale Organisationen, Botschaften",
                "Typ der Auftraggeber - Gesuchsteller: Immobilienbranche (Einzelpersonen oder Personengesellschaften)",
                "Typ der Auftraggeber - Gesuchsteller: Immobilienbranche (Wohnbaugenossenschaften)",
                "Typ der Auftraggeber - Gesuchsteller: Bundesamt für Umweltschutz",
                # Grundnutzung
                "Grundnutzung: Landwirtschaftszone",
                "Grundnutzung: Reservezone",
                "Grundnutzung: Wald",
                "Grundnutzung: Weilerzone",
                "Grundnutzung: Freihaltezone",
                "Grundnutzung: Verkehrsflächen aBZ",
                "Grundnutzung: Andere",
                # Flächenbedarf nach Grundnutzung (m²)
                "Flächenbedarf nach Grundnutzung (m²)",
                "Flächenbedarf Fruchtfolgeflächen (m²)",
                "Kompensation Fruchtfolgeflächen (m²)",
                "Anzahl neue Gebäude",
                "Anzahl Gebäude die abgebrochen werden",
                # Art der Ver- bzw. Entsiegelungen
                "Art der Ver- bzw. Entsiegelung: Neue versiegelte Flächen (Gebäude)",
                "Art der Ver- bzw. Entsiegelung: Neue versiegelte Flächen (Umgebung)",
                "Art der Ver- bzw. Entsiegelung: Neue versiegelte Flächen (Erschliessung)",
                "Art der Ver- bzw. Entsiegelung: Entsiegelte / renaturierte Flächen (Gebäude)",
                "Art der Ver- bzw. Entsiegelung: Entsiegelte / renaturierte Flächen (Umgebung)",
                "Art der Ver- bzw. Entsiegelung: Entsiegelte / renaturierte Flächen (Erschliessung)",
                "Fläche (m²)",
                # Nutzung der versiegelten Flächen
                "Nutzung der versiegelten Flächen: Landwirtschaft",
                "Nutzung der versiegelten Flächen: Tourismus",
                "Nutzung der versiegelten Flächen: Energie",
                "Nutzung der versiegelten Flächen: Verkehr (kantonale und nationale Projekte)",
                "Nutzung der versiegelten Flächen: Wald (Projekte für die Waldbewirtschaftung)",
                "Nutzung der versiegelten Flächen: Andere",
                "Beschreibung",
                # Stabilisierungsziel
                "Stabilisierungsziel: Nicht relevant (Tourismus und Landwirtschaft)",
                "Stabilisierungsziel: Relevant",
                "Stabilisierungsziel: Nicht relevant (Bauten / Flächen altrechtlich bestehend)",
                "Stabilisierungsziel: Nicht relevant (keine neuen ver- oder entsiegelten Flächen)",
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def get_amount_of_single_choice_answers(
        self, entry, mapping, table_answer, slug, prefix, index
    ):
        for name, key in mapping.items():
            entry[f"{prefix}: {name}"] = (
                1 + index
                if table_answer.get(slug) and key in table_answer.get(slug)
                else ""
            )

    def get_total_int_and_str_table_values(self, entry, table_answer, slug, name):
        total_amount = []
        for answer in table_answer:
            amount = answer.get(slug)

            if amount:
                total_amount.append(amount)
        if total_amount and type(total_amount[0]) is str:
            entry[name] = ", ".join(total_amount)
        elif total_amount and type(total_amount[0]) is int:
            entry[name] = sum(total_amount)
