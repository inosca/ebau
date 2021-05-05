import json
import re
from logging import getLogger

from caluma.caluma_form import models as form_models

log = getLogger(__name__)


class Transform:
    @staticmethod
    def yes_if_present(value_prefix):
        def mapper(val):
            if val:
                return f"{value_prefix}-yes"
            return f"{value_prefix}-no"

        return mapper

    @staticmethod
    def static_if_present(value):
        def mapper(val):
            if val:
                return value
            return None

        return mapper

    @staticmethod
    def prepend_proposal():
        def mapper(val, slug, document):
            old_value_map = {
                "23": "An/Aufbau",
                "24": "Zweckänderung",
                "25": "Terrainveränderung",
                "27": "Reklame",
                "28": "Garage",
                "29": "Solaranlage",
                "30": "Fassadensanierung",
                "31": "EFH",
                "32": "MFH",
                "33": "Geschäftshaus",
                "34": "Lagergebäude",
                "35": "Antennenanlage",
                "36": "Unterkellerung",
            }
            values = json.loads(val)

            if "21" in values:
                values.remove("21")
            if "22" in values:
                values.remove("22")
            if "26" in values:
                values.remove("26")
            if values and values != [""]:
                value = map(lambda value: old_value_map[value], values)
                try:
                    ans = document.answers.get(question_id=slug)
                    return f"{', '.join(list(value))}; {ans.value}"
                except form_models.Answer.DoesNotExist:
                    return f"{', '.join(list(value))}"

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
    def join_checkbox(mapping, separator):
        def wrapper(val, document, slug):

            value_list = [mapping.get(v) for v in json.loads(val) if mapping.get(v)]
            try:
                existing_answer = document.answers.get(question=slug)
                value_list.append(existing_answer.value)
            except form_models.Answer.DoesNotExist:
                pass

            return separator.join(value_list)

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
        try:
            factor = 1
            if "mio" in value.lower():
                factor = 1000000

            new_value = re.sub(r"[^0-9\.]", "", str(value))
            if new_value.endswith("."):
                # can happen if input value is "fr 130'000.--"
                new_value = new_value[:-1]
            if new_value.startswith("."):
                # can happen if input value is "fr. 130'000.--"
                new_value = new_value[1:]

            new_value = str(factor * float(new_value))
            return re.sub("\.0*$", "", new_value)
        except ValueError:
            log.critical(f"number could not be extracted from : {value}")
            __import__("pdb").set_trace()  # noqa
            pass

    @staticmethod
    def extract_first_number(value):
        match = re.search(r"\d+", str(value))
        return match.group() if match else None
