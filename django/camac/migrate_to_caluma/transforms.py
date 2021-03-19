import json
import re
from logging import getLogger

from caluma.caluma_form import models as form_models

log = getLogger(__name__)

GRUNDNUTZUNG_MAPPING = {
    "W1": "Wohnzone 1",  # Wohnzone 1
    "W2": "Wohnzone 2",  # Wohnzone 2
    "W3": "Wohnzone 3",  # Wohnzone 3
    "W4": "Wohnzone 4",  # Wohnzone 4
    "GE": "Gewerbezone",  # Gewerbezone
    "I": "Industriezone",  # Industriezone
    "WG2": "Wohn- und Gewerbezone 2",  # Wohn- und Gewerbezone 2
    "WG3": "Wohn- und Gewerbezone 3",  # Wohn- und Gewerbezone 3
    "WG4": "Wohn- und Gewerbezone 4",  # Wohn- und Gewerbezone 4
    "K1": "Kernzone 1",  # Kernzone 1
    "K3": "Kernzone 3",  # Kernzone 3
    "BZ": "Bahnhofzone",  # Bahnhofzone
    "OE": "Zone für öffentliche Bauten und Anlagen",  # Zone für öffentliche Bauten und Anlagen
    "FZ": "Freihaltezone",  # Freihaltezone
    "TZ": "Tourismuszone",  # Tourismuszone
    "SF": "Zone für Sport- und Freizeitanlagen",  # Zone für Sport- und Freizeitanlagen
    "VF": "Verkehrsfläche innerhalb Bauzonen",  # Verkehrsfläche innerhalb Bauzonen
    "AB": "Zone für besondere Anlagen und Betriebsstätten",  # Zone für besondere Anlagen und Betriebsstätten
    "L": "Landwirtschaftszone",  # Landwirtschaftszone
    "SL": "Speziallandwirtschaftszone",  # Speziallandwirtschaftszone
    "RB": "Rebbauzone",  # Rebbauzone
    "NSl": "Naturschutzzone lokal",  # Naturschutzzone lokal
    "FZaB": "Freihaltezone ausserhalb Bauzonen",  # Freihaltezone ausserhalb Bauzonen
    "GR": "Gewässerraumzone",  # Gewässerraumzone
    "Ge": "Gewässer",  # Gewässer
    "WZ": "Weilerzone",  # Weilerzone
    "VFaB": "Verkehrsfläche ausserhalb Bauzonen",  # Verkehrsfläche ausserhalb Bauzonen
    "RZ": "Reservezone",  # Reservezone
    "Wa": "Wald",  # Wald
    "D": "Deponiezone",  # Deponiezone
    "A": "Abbauzone",  # Abbauzone
    "AD": "Abbau- und Deponiezone",  # Abbau- und Deponiezone
    "SFG": "Zone für Sport- und Freizeitanlagen Golf",  # Zone für Sport- und Freizeitanlagen Golf
    "RZu": "Reservezone, unproduktiv",  # Reservezone, unproduktiv
    "W2K": "Wohnzone 2 Kirchhügel",  # Wohnzone 2 Kirchhügel
    "W2a": "Wohnzone 2a",  # Wohnzone 2a
    "W2b": "Wohnzone 2b",  # Wohnzone 2b
    "W2c": "Wohnzone 2c",  # Wohnzone 2c
    "WE": "Wohnzone Eggberge",  # Wohnzone Eggberge
    "WL": "Wohnzone im Landschaftsgebiet",  # Wohnzone im Landschaftsgebiet
    "WK": "Wohnzone Kolonie",  # Wohnzone Kolonie
    "WSRütli": "Sonderwohnzone Rütli",  # Sonderwohnzone Rütli
    "WGE": "Wohn- und Gewerbezone Eggberge",  # Wohn- und Gewerbezone Eggberge
    "K2": "Kernzone 2",  # Kernzone 2
    "K4": "Kernzone 4",  # Kernzone 4
    "I1": "Industriezone 1",  # Industriezone 1
    "I2": "Industriezone 2",  # Industriezone 2
    "ABEC": "Zone für besondere Anlage und Betriebsstätte Event-Center",  # Zone für besondere Anlage und Betriebsstätte Event-Center
    "WS": "Sonderwohnzone",  # Sonderwohnzone
    "BZB": "BZ Brüsti",  # BZ Brüsti
    "Eh": "Erholungszone",  # Erholungszone
    "FPZ": "Flugplatzzone",  # Flugplatzzone
    "ABE": "Gewerbesonderzone Eielen",  # Gewerbesonderzone Eielen
    "ABH": "Gewerbesonderzone Harder",  # Gewerbesonderzone Harder
    "ABN": "Niederhofen",  # Niederhofen
    "ABSH": "Sondernutzungszone Holzheizwerk",  # Sondernutzungszone Holzheizwerk
    "SZB": "Sonderzone Baugruppen",  # Sonderzone Baugruppen
    "G1": "Gewerbezone 1",  # Gewerbezone 1
    "G2": "Gewerbezone 2",  # Gewerbezone 2
    "W5": "Wohnzone 5+",  # Wohnzone 5+
    "WG5": "Wohn- und Gewerbezone 5+",  # Wohn- und Gewerbezone 5+
    "K": "Kernzone",  # Kernzone
    "KZE": "Kernzone - Zentrum",  # Kernzone - Zentrum
    "LW": None,  # Value not in answerlist
    "R": None,  # Value not in answerlist
    "W": None,  # Value not in answerlist
    "KZ": None,  # Value not in answerlist
    "KS": None,  # Value not in answerlist
    "ViB": None,  # Value not in answerlist
    "T": None,  # Value not in answerlist
    "G": None,  # Value not in answerlist
    "O": None,  # Value not in answerlist
    "VaB": None,  # Value not in answerlist
    "F": None,  # Value not in answerlist
    "FaB": None,  # Value not in answerlist
    "B": None,  # Value not in answerlist
    "U": None,  # Value not in answerlist
    "": None,  # Empty value in answerslist
}

UEBERLAGERTE_NUTZUNG_MAP = {
    "OS": "Ortsbildschutzzone",  # Ortsbildschutzzone
    "SOK": "Schutzobjekt in Kernzonen",  # Schutzobjekt in Kernzonen
    "Arch": "Archäologisches Funderwartungsgebiet",  # Archäologisches Funderwartungsgebiet
    "NSlü": "Naturschutzzone lokal, überlagert",  # Naturschutzzone lokal, überlagert
    "LSl": "Landschaftsschutzzone lokal",  # Landschaftsschutzzone lokal
    "LpB": "Gebiet mit landschaftsprägenden Bauten",  # Gebiet mit landschaftsprägenden Bauten
    "TrS": "Gebiet mit traditioneller Streubauweise",  # Gebiet mit traditioneller Streubauweise
    "GRü": "Gewässerraumzone, überlagert",  # Gewässerraumzone, überlagert
    "GZr": "Gefahrenzone rot",  # Gefahrenzone rot
    "GZb": "Gefahrenzone blau",  # Gefahrenzone blau
    "GZg": "Gefahrenzone gelb",  # Gefahrenzone gelb
    "ZW": "Zone für Wintersport",  # Zone für Wintersport
    "Dü": "Deponiezone, überlagert",  # Deponiezone, überlagert
    "Aü": "Abbauzone, überlagert",  # Abbauzone, überlagert
    "ABü": "Zone für besondere Anlagen und Betriebsstätten, überlagert",  # Zone für besondere Anlagen und Betriebsstätten, überlagert
    "ZBG": "Zone für Bauten in Gewässern",  # Zone für Bauten in Gewässern
    "SFü": "Zone für Sport- und Freizeitanlagen, überlagert",  # Zone für Sport- und Freizeitanlagen, überlagert
    "QPr": "Bereich rechtsgültiger Quartierplan",  # Bereich rechtsgültiger Quartierplan
    "QGPr": "Bereich rechtsgültiger Quartiergestaltungsplan",  # Bereich rechtsgültiger Quartiergestaltungsplan
    "QPp": "Zone mit Quartierplanpflicht",  # Zone mit Quartierplanpflicht
    "QGPp": "Zone mit Quartiergestaltungsplanpflicht",  # Zone mit Quartiergestaltungsplanpflicht
    "NvI": "Nutzungsvorbehalt Immissionsschutz",  # Nutzungsvorbehalt Immissionsschutz
    "GvRR": "Genehmigungsvorbehalt RR",  # Genehmigungsvorbehalt RR
    "wfF": "weitere flächenbezogene Festlegung",  # weitere flächenbezogene Festlegung
    "BLS": "Baulinie Strasse",  # Baulinie Strasse
    "BLG": "Baulinie Gewässer",  # Baulinie Gewässer
    "BLI": "Baulinie Immissionsschutz",  # Baulinie Immissionsschutz
    "BL": "weitere Baulinie (gem. Art. 49 PBG)",  # weitere Baulinie (gem. Art. 49 PBG)
    "NOll": "Naturobjekt lokal, linear",  # Naturobjekt lokal, linear
    "KOll": "Kulturobjekt lokal, linear",  # Kulturobjekt lokal, linear
    "NOl": "Naturobjekt lokal",  # Naturobjekt lokal
    "KOl": "Kulturobjekt lokal",  # Kulturobjekt lokal
    "EO": "Einzelobjekt in Kern- und Schutzzonen",  # Einzelobjekt in Kern- und Schutzzonen
    "KOIIGM": "Geschützte Mauer",  # Geschützte Mauer
    "NOIEB": "Einzelbaum",  # Einzelbaum
    "EOSG": "Schutzwürdige Gebäude",  # Schutzwürdige Gebäude
    "VB": "Gebiet mit verdichteter Bauweise",  # Gebiet mit verdichteter Bauweise
    "QRPr": "Bereich rechtsgültiger Quartierrichtplan",  # Bereich rechtsgültiger Quartierrichtplan
    "AR": "Abfahrtsrouten",  # Abfahrtsrouten
    "F": "Fernsprenganlagen",  # Fernsprenganlagen
    "PA": "Parkanlagen",  # Parkanlagen
    "SUB": "Seeuferbereich, überlagert",  # Seeuferbereich, überlagert
    "E": "Schutzbereich",  # Schutzbereich
    "KOIIwG": "wichtige Gasse",  # wichtige Gasse
    "QRPp": "Zone mit Quartierrichtplanpflicht",  # Zone mit Quartierrichtplanpflicht
    "ABüH": "Gewerbesonderzone Harder, überlagert",  # Gewerbesonderzone Harder, überlagert
    "PB": "Projektierungsbereich",  # Projektierungsbereich
    "GSZ": "Grundwasserschutzzone",
    "GSZp": "Grundwasserschutzzonen provisorisch",
    "GSA": "Grundwasserschutzareale",
    "GSAp": "Grundwasserschutzareale provisorisch",
    "GG": "Gefahrengebiet",
    "WRZ": "Wildruhezone",
    "WR": "Waldreservat",
    "NSrn": "Naturschutzzone regional / national",
    "FM": "Flachmoor",
    "LSrn": "Landschaftsschutzzone regional / national",
    "GmsB": "Gebiete mit schützenswerter Bausubstanz",
    "NOrnl": "Naturobjekt regional / national, linear",
    "NOrn": "Naturobjekt regional / national, punktförmig",
    "KOrnl": "Kulturobjekt regional / national, linear",
    "KOrn": "Kulturobjekt regional / national, punktförmig",
    "FFF": "Fruchtfolgefläche",
    "GRu": None,  # Value not in answerlist
    "WS": None,  # Value not in answerlist
    "NSlu": None,  # Value not in answerlist
    "SFu": None,  # Value not in answerlist
    "": None,  # Empty value in answerslist
}


class Transform:
    @staticmethod
    def yes_if_present(value_prefix):
        def mapper(val):
            if val:
                return f"{value_prefix}-yes"
            return f"{value_prefix}-no"

        return mapper

    @staticmethod
    def checkbox(value_mapping):
        """Return a question transform for camac-style checkbox.

        Takes a parameter with the camac values as keys, and the caluma values as values
        """

        def mapper(val, old_question, slug, is_retry=False):
            try:
                old_values = json.loads(val)
            except json.decoder.JSONDecodeError:
                # Some older versions of Camac stored values not as JSON lists, but
                # as comma-separated (?) value lists
                old_values = val.split(",")
            try:
                new_values = [value_mapping[key] for key in old_values]
            except TypeError:
                __import__("pdb").set_trace()  # noqa
            except KeyError as exc:
                log.debug(
                    f"Mapping for {old_question} -> {slug}: couldn't find mapping for {str(exc)}"
                )
                if is_retry:
                    log.error(
                        f"Mapping for {old_question} -> {slug}: couldn't find mapping for '{str(exc)}'"
                    )
                    raise
                else:
                    # Retry by using the names instead of the values (easier to configure)
                    old_values_mapped = list(
                        old_question.answerlist.filter(
                            value__in=old_values
                        ).values_list("name", flat=True)
                    )
                    return mapper(
                        json.dumps(old_values_mapped), old_question, slug, is_retry=True
                    )

            # Some values are mapped to nothing (for completeness). Don't output those.
            return [val for val in new_values if val is not None]

        return mapper

    @staticmethod
    def select_as_checkbox(value_mapping):
        def wrapper(val):
            return [Transform.select(value_mapping)(val)]

        return wrapper

    @staticmethod
    def join_values(separator):
        def wrapper(val):
            return separator.join(val)

        return wrapper

    @staticmethod
    def join_multi_values_grundnutzung(separator):
        def wrapper(val):
            return separator.join(
                [
                    GRUNDNUTZUNG_MAPPING.get(v)
                    for v in json.loads(val)
                    if GRUNDNUTZUNG_MAPPING.get(v)
                ]
            )

        return wrapper

    @staticmethod
    def join_multi_values_ueberlagerte_nutzung(separator):
        def wrapper(val, document, slug):

            try:
                existing_answer = document.answers.get(question=slug)
                value_list = [
                    UEBERLAGERTE_NUTZUNG_MAP.get(v)
                    for v in json.loads(val)
                    if UEBERLAGERTE_NUTZUNG_MAP.get(v)
                ]
                value_list.append(existing_answer.value)
                return separator.join(value_list)
            except form_models.Answer.DoesNotExist:
                return separator.join(
                    [
                        UEBERLAGERTE_NUTZUNG_MAP.get(v)
                        for v in json.loads(val)
                        if UEBERLAGERTE_NUTZUNG_MAP.get(v)
                    ]
                )

        return wrapper

    @staticmethod
    def join_multiple_values():
        def wrapper(val, document, slug):

            try:
                existing_answer = document.answers.get(question=slug)
                values = f"{existing_answer.value}; {val}"
                return values
            except form_models.Answer.DoesNotExist:
                return val

        return wrapper

    @staticmethod
    def select(value_mapping):
        """Return a question transform for camac-style select/dropdown.

        Takes a parameter with the camac values as keys, and the caluma values as values
        """

        def mapper(val):
            new_value = value_mapping.get(val, None)
            return new_value

        return mapper

    @staticmethod
    def none(val, slug, old_question):
        """Transform to be used if the old value can be migrated without change."""
        target = form_models.Question.objects.get(pk=slug.split(".")[-1])
        if target.type not in [
            form_models.Question.TYPE_INTEGER,
            form_models.Question.TYPE_FLOAT,
            form_models.Question.TYPE_TEXT,
            form_models.Question.TYPE_TEXTAREA,
        ]:
            # choice questions MUST have a mapping, so can't just
            # pass without transform
            old_values = old_question.answerlist.all()
            if target.data_source:
                __import__("pdb").set_trace()  # noqa
                # evaluate data source, then list options
                pass
            new_values = target.options.all()
            __import__("pdb").set_trace()  # noqa
            raise RuntimeError(
                f"Question {old_question} of type {old_question.question_type.name} "
                f"(id={old_question.pk}) maps to {slug} which "
                f"is of type {target.type}. Must be transformed! "
                f"old values: {old_values} "
                f"new values: {new_values} "
            )
        return val

    @staticmethod
    def TODO_MANUAL():
        raise NotImplementedError("Value mapper not configured")

    def extract_name_part(part):
        # TODO: if there's ANY ambiguity, return nothing for the
        # first name and everything as the last name.

        # assumption: single-word firstname followed by last
        # name (which can be multiple words such as "von Gunten")
        def the_transform(old_val):
            if not isinstance(old_val, str):
                return None
            # remove some common name prefixes (from live data):
            old_val = re.sub(r"^c/o\s*", "", old_val, flags=re.IGNORECASE)
            log.debug(f"Extracting {part} name form '{old_val}'")

            try:
                first, last = old_val.split(maxsplit=1)
            except ValueError:
                # single word, using the same value for all parts
                return old_val

            out = {"first": first, "last": last}
            return out[part]

        return the_transform

    @staticmethod
    def append_text(separator="; "):
        def the_transform(old_val, slug, document):
            try:
                ans = document.answers.get(question_id=slug)
                return ans.value + separator + old_val
            except form_models.Answer.DoesNotExist:
                return old_val

        return the_transform

    @staticmethod
    def extract_from_city(part):
        # TODO: if there's ANY ambiguity, return nothing for the
        # zip and everything as the last name.

        # Assumption: swiss city names and zip formats / locations:
        # 1234 city name
        def the_transform(old_val):
            if not isinstance(old_val, str):
                return None
            try:
                zip, city = old_val.split(maxsplit=1)
                out = {"zip": zip, "city": city}
                return out[part]
            except ValueError:
                # could not split. Assuming city name without zip
                return "" if part == "zip" else old_val

        return the_transform

    @staticmethod
    def extract_number(value):
        new_value = re.sub(r"[^0-9\.]", "", str(value))
        if new_value.endswith("."):
            # can happen if input value is "fr 130'000.--"
            new_value = new_value[:-1]
        if new_value.startswith("."):
            # can happen if input value is "fr. 130'000.--"
            new_value = new_value[1:]

        return new_value
