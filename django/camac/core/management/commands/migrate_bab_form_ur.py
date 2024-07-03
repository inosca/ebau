from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Answer as CalumaAnswer, Document, Question
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.core.models import Answer, BabUsage
from camac.instance.models import Instance
from camac.user.models import Service

QUESTION_MAP = [
    {
        "camac_question_id": 261,
        "caluma_question_slug": "bab-art-der-massnahme",
        "label": "Art der Massnahme",
    },
    {
        "camac_question_id": 262,
        "caluma_question_slug": "bab-objektart",
        "label": "Objektart",
    },
    {
        "camac_question_id": 263,
        "caluma_question_slug": "bab-nutzung-nach-rpg",
        "label": "Nutzung nach RPG",
    },
    {
        "camac_question_id": 264,
        "caluma_question_slug": "bab-bewilligungsgrund",
        "label": "Bewilligungsgrund - Rechtliche Grundlage",
    },
    {
        "camac_question_id": 265,
        "caluma_question_slug": "bab-entscheid",
        "label": "Entscheid",
    },
    {
        "camac_question_id": 267,
        "caluma_question_slug": "bab-typ-der-auftraggeber",
        "label": "Typ der Auftraggeber - Gesuchsteller",
    },
    {
        "camac_question_id": 268,
        "caluma_question_slug": "bab-flaechenbedarf-fruchtfolgeflaechen",
    },
    {
        "camac_question_id": 269,
        "caluma_question_slug": "bab-kompensation-fruchtfolgeflaechen",
    },
]

ANSWER_MAP = {
    261: {
        "abbruch": "bab-art-der-massnahme-abbruch",
        "sanierung": "bab-art-der-massnahme-sanierung",
        "umbau": "bab-art-der-massnahme-umbau-anbau",
        "Ersatzneubau": "bab-art-der-massnahme-ersatzneubau",
        "neubau": "bab-art-der-massnahme-neubau",
        "zweck": "bab-art-der-massnahme-zweckaenderung",
        "bgbb": "bab-art-der-massnahme-abparzellierung",
        "andere": "bab-art-der-massnahme-andere",
    },
    262: {
        "wohnbaute": "bab-objektart-wohnbaute",
        "wohnökonomie": "bab-objektart-wohn-oekonomiebaute",
        "gewerbemitap": "bab-objektart-gewerbebaute-mit-arbeitsplaetzen",
        "gewerbeohneap": "bab-objektart-gewerbebaute-ohne-arbeitsplaetzen",
        "ökonomie_tier": "bab-objektart-oekonomiebaute-mit-tierhaltung",
        "ökonomie": "bab-objektart-oekonomiebaute-ohne-tierhaltung",
        "terrain": "bab-objektart-terrainveraenderung",
        "Wanderweg": "bab-objektart-wanderweg",
        "viehtriebweg": "bab-objektart-viehtriebweg",
        "bewirtschaftungsweg": "bab-objektart-bewirtschaftungsweg",
        "hofgüter": "bab-objektart-hof-guetererschliessung",
        "Befristet": "bab-objektart-fahrnisbauten",
        "Betrieb Hof": "bab-objektart-betrieb-gewerbe-liegenschaften",
        "andere": "bab-objektart-andere",
    },
    263: {
        "zonenkonform": "bab-nutzung-nach-rpg-zonenkonform",
        "ausnahme": "bab-nutzung-nach-rpg-ausnahmebewilligung",
        "andere": "bab-nutzung-nach-rpg-andere",
    },
    264: {
        "5000": "bab-bewilligungsgrund-innerhalb-bauzone",
        "5001": "bab-bewilligungsgrund-oekonomiebauten",
        "5002": "bab-bewilligungsgrund-landwirtschaftliche-bauten",
        "5003": "bab-bewilligungsgrund-wohnbauten",
        "5004": "bab-bewilligungsgrund-stallbauten",
        "5005": "bab-bewilligungsgrund-tierhaltung",
        "5006": "bab-bewilligungsgrund-gewaechshaeuser",
        "5007": "bab-bewilligungsgrund-speziallandwirtschaftszonen",
        "5008": "bab-bewilligungsgrund-biomasse",
        "5009": "bab-bewilligungsgrund-zonenkonform",
        "5011": "bab-bewilligungsgrund-spezialzonen",
        "5012": "bab-bewilligungsgrund-erhaltungszonen",
        "5015": "bab-bewilligungsgrund-solaranlagen",
        "5021": "bab-bewilligungsgrund-standortgebunden",
        "5022": "bab-bewilligungsgrund-streusiedlungsgebiet",
        "5023": "bab-bewilligungsgrund-landschaftspraegende-bauten",
        "5031": "bab-bewilligungsgrund-ohne-bauliche-massnahmen",
        "5041": "bab-bewilligungsgrund-existenzsicherung",
        "5043": "bab-bewilligungsgrund-nebenbetriebe",
        "5044": "bab-bewilligungsgrund-temp-betriebszentren",
        "5051": "bab-bewilligungsgrund-zonenwidrig",
        "5061": "bab-bewilligungsgrund-landwirtschaftliche-wohnbauten",
        "5062": "bab-bewilligungsgrund-geschuetzte-bauten",
        "5063": "bab-bewilligungsgrund-hobby-tierhaltung-aussenanlagen",
        "5064": "bab-bewilligungsgrund-hobby-tierhaltung-bauzone",
        "5071": "bab-bewilligungsgrund-zonenwidrige-gewerbliche-bauten",
        "1 Kein GWR Code": "bab-bewilligungsgrund-allgemein-zonenkonform",
        "2 Kein GWR Code": "bab-bewilligungsgrund-abparzellierung",
        "3 Kein GWR Code": "bab-bewilligungsgrund-andere-dossiers",
        "4 Kein GWR Code": "bab-bewilligungsgrund-solaranlagen-ausserhalb-bauzone",
        "andere": "bab-bewilligungsgrund-andere-dossiers",
        "24": "bab-bewilligungsgrund-standortgebunden",
        "16a": "bab-bewilligungsgrund-stallbauten",
        "22": "bab-bewilligungsgrund-allgemein-zonenkonform",
        "24c": "bab-bewilligungsgrund-zonenwidrig",
    },
    265: {
        "positiv": "bab-entscheid-positiv",
        "negativ": "bab-entscheid-negativ",
        "andere": "bab-entscheid-andere",
    },
    267: {
        "6101": "bab-typ-der-auftraggeber-sbb",
        "6103": "bab-typ-der-auftraggeber-vbs",
        "6104": "bab-typ-der-auftraggeber-bbl",
        "6105": "bab-typ-der-auftraggeber-astra",
        "6107": "bab-typ-der-auftraggeber-swisscom",
        "6108": "bab-typ-der-auftraggeber-post",
        "6110": "bab-typ-der-auftraggeber-kanton-nicht-oeffentlich",
        "6111": "bab-typ-der-auftraggeber-kanton-oeffentlich",
        "6115": "bab-typ-der-auftraggeber-gemeinde-inkl-kooperationen",
        "6116": "bab-typ-der-auftraggeber-gemeinden-oeffentlich",
        "6121": "bab-typ-der-auftraggeber-versicherungsgesellschaften",
        "6122": "bab-typ-der-auftraggeber-personalfuersorgestiftungen",
        "6123": "bab-typ-der-auftraggeber-krankenkassen",
        "6124": "bab-typ-der-auftraggeber-banken",
        "6131": "bab-typ-der-auftraggeber-elektrizitaetswerke",
        "6132": "bab-typ-der-auftraggeber-gaswerke",
        "6133": "bab-typ-der-auftraggeber-privatbahnen",
        "6143": "bab-typ-der-auftraggeber-immobilienbranche",
        "6161": "bab-typ-der-auftraggeber-privatpersonen",
        "6151": "bab-typ-der-auftraggeber-einzelfirmen",
        "6152": "bab-typ-der-auftraggeber-kapitalgesellschaft",
        "6162": "bab-typ-der-auftraggeber-andere-private-auftraggeber",
        "6163": "bab-typ-der-auftraggeber-internationale-organisationen",
        "6141": "bab-typ-der-auftraggeber-immobilienbranche-einzelpersonen",
        "6142": "bab-typ-der-auftraggeber-immobilienbranche-wohnbaugenossenschaften",
        "BAFU": "bab-typ-der-auftraggeber-bundesamt",
        "privat": "bab-typ-der-auftraggeber-privatpersonen",
        "gemeinschaft": "bab-typ-der-auftraggeber-privatpersonen",
        "gemeinde": "bab-typ-der-auftraggeber-gemeinden-oeffentlich",
        "kanton": "bab-typ-der-auftraggeber-kanton-nicht-oeffentlich",
        "andere": "bab-typ-der-auftraggeber-andere-private-auftraggeber",
    },
}

BAB_USAGE_MAPPING = {
    "0": "bab-grundnutzung-landwirtschaftszone",
    "1": "bab-grundnutzung-reservezone",
    "2": "bab-grundnutzung-wald",
    "3": "bab-grundnutzung-weilerzone",
    "4": "bab-grundnutzung-freihaltezone",
    "5": "bab-grundnutzung-verkehrsflaechen-abz",
    "6": "bab-grundnutzung-andere",
}


class Command(BaseCommand):
    help = """Migrate the old camac form 'BaB Datenerfassung' in the new caluma form"""

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        instances = Instance.objects.filter(
            case__work_items__task_id="complete-check",
            case__work_items__status=WorkItem.STATUS_COMPLETED,
        ).distinct()

        count = 0
        for instance in instances:
            addressed_groups = [
                str(service.pk)
                for service in Service.objects.filter(
                    name=settings.APPLICATION["CALUMA"]["BAB_MUNICIPALITY_MAPPING"][
                        instance.location_id
                    ]
                )
            ]
            previous_work_item = instance.case.work_items.filter(
                task_id="complete-check"
            )

            work_item, _ = instance.case.work_items.get_or_create(
                task_id="bab",
                status=WorkItem.STATUS_READY,
                name="BaB Datenerfassung",
                previous_work_item=previous_work_item.first()
                if previous_work_item
                else None,
                addressed_groups=addressed_groups,
                document=Document.objects.create(form_id="bab"),
            )

            self._migrate_answers(instance, work_item)
            self._migrate_php_table_answer(instance, work_item)
            count += 1
            self.stdout.write(f"BaB answers of instance {instance.pk} were migrated")
        self.stdout.write(f"The answers of {count} instances were migrated")

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def _migrate_answers(self, instance, work_item):
        for question in QUESTION_MAP:
            answer = Answer.objects.filter(
                instance=instance,
                chapter_id=104,
                question_id=question["camac_question_id"],
                item=1,
            ).first()

            if not answer:
                return

            save_answer(
                document=work_item.document,
                question=Question.objects.get(slug=question["caluma_question_slug"]),
                value=ANSWER_MAP[answer.question_id][answer.answer]
                if answer.question_id in ANSWER_MAP.keys()
                else int(answer.answer),
            )

    def _migrate_php_table_answer(self, instance, work_item):
        bab_usages = BabUsage.objects.filter(instance=instance)

        if bab_usages:
            row_answer, _ = CalumaAnswer.objects.get_or_create(
                document_id=work_item.document.pk,
                question_id="bab-lage-flaechenbedarf-tabelle",
            )

            for answer in bab_usages:
                row_document = Document.objects.create(
                    form_id="bab-lage-flaechenbedarf-form", family=work_item.document
                )

                CalumaAnswer.objects.bulk_create(
                    [
                        CalumaAnswer(
                            question_id="bab-flaechenbedarf-grundnutzung",
                            document=row_document,
                            value=answer.usage,
                        ),
                        CalumaAnswer(
                            question_id="bab-grundnutzung",
                            document=row_document,
                            value=BAB_USAGE_MAPPING[str(answer.usage_type)],
                        ),
                    ],
                )
                row_answer.documents.add(row_document)
