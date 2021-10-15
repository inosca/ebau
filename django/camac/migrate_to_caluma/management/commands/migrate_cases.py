import codecs
import inspect
import itertools
import json
import re
from collections import defaultdict
from datetime import datetime
from logging import getLogger
from pprint import pprint

from caluma.caluma_form import models as form_models
from caluma.caluma_workflow import models as workflow_models
from caluma.caluma_workflow.jexl import GroupJexl
from django.core.management.base import BaseCommand
from django.core.validators import EMPTY_VALUES
from django.db import transaction
from django.db.models import F, Value
from django.db.models.expressions import CombinedExpression, Func
from django.utils.timezone import now

from camac.constants import kt_uri as uri_constants
from camac.core.models import Answer, ChapterPage
from camac.instance.domain_logic import CreateInstanceLogic
from camac.instance.models import Instance, JournalEntry
from camac.migrate_to_caluma import question_map
from camac.user.models import Location, User

log = getLogger(__name__)

# ADMIN_USER_ID = 1 # sycloud, production
ADMIN_USER_ID = 3240  # local

DOSSIER_NUMBER_QUESTION_ID = 6


class DryRun(BaseException):
    """Used to jump out of atomic block to implement dryrun."""

    pass


def evaluate_assigned_groups(task):
    if task.address_groups:
        return GroupJexl().evaluate(task.address_groups)

    return []


def get_addressed_groups(task):
    addressed_groups = [evaluate_assigned_groups(task)]
    if task.is_multiple_instance:
        addressed_groups = [[x] for x in addressed_groups[0]]
    return addressed_groups


def extract_parcels(parcel_string):
    numbers = re.findall(r"[0-9]+", parcel_string)
    filtered_numbers = [
        int(number) for number in numbers if int(number) not in range(1201, 1221)
    ]
    return filtered_numbers


class Command(BaseCommand):
    """Migrate dossiers from old Camac to Caluma/Camac-NG."""

    help = "Migrate dossiers from old Camac to Caluma/Camac-NG."

    def get_caluma_form(self, form_id):
        mapping = {
            "building-permit": [41, 44, 47, 293, 294],
            "preliminary-clarification": [21, 61],
            "commercial-permit": [121, 249],
            "solar-declaration": [141],
            "proposal-declaration": [290, 295],
            "cantonal-territory-usage": [247, 291],
            "oereb": [
                261,
                281,
                282,
                284,
                285,
                101,
                102,
                103,
                104,
                105,
                106,
                107,
                108,
            ],
            "mitbericht-kanton": [
                42,
                43,
                45,
                46,
                161,
                181,
                201,
                221,
                222,
                223,
                224,
                225,
                241,
                242,
                243,
                245,
                246,
                248,
                251,
                252,
                253,
                254,
                255,
                256,
                257,
                258,
                259,
                260,
                286,
                287,
                288,
                289,
            ],
            "mitbericht-bund": [244, 250, 292],
        }
        return [key for key, value in mapping.items() if form_id in value][0]

    QUESTION_MAP_BY_FORM = {
        "building-permit": question_map.QUESTION_MAP_BAUGESUCH,
        "preliminary-clarification": question_map.QUESTION_MAP_BAUGESUCH,
        "commercial-permit": question_map.QUESTION_MAP_REKLAME,
        "proposal-declaration": question_map.QUESTION_MAP_MELDUNG_VORHABEN,
        "solar-declaration": question_map.QUESTION_MAP_MELDUNG_SOLARANLAGE,
        "mitbericht-kanton": question_map.QUESTION_MAP_MITBERICHT_KANTON,
        "mitbericht-bund": question_map.QUESTION_MAP_MITBERICHT_BUND,
        "cantonal-territory-usage": question_map.QUESTION_MAP_BENUETZUNG_KANTONSGEBIET,
        "oereb": question_map.QUESTION_MAP_OEREB_VERFAHREN,
    }

    IGNORE_QUESTIONS = question_map.IGNORE_QUESTIONS
    IGNORE_CHAPTERS = question_map.IGNORE_CHAPTERS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._no_more = False
        self._dry_run = False
        self._single_step = False
        self._dev_mode = False
        self._validated_maps = set()

    def add_arguments(self, parser):
        parser.add_argument(
            "--single", help="Single-Step migration", action="store_true"
        )
        parser.add_argument(
            "--dry", help="Dry-run migration (don't commit DB)", action="store_true"
        )
        parser.add_argument(
            "--dev",
            help="Development mode (don't abort on unknown questions/answers)",
            action="store_true",
        )

    def _ask_next(self, inst):
        if not self._single_step:
            return (inst, False)

        if self._no_more:
            return (False, False)
        answer = None
        while answer is None:
            question = (
                "Migrate dossier %s (State: %s)? (yes, no, debugger, quit) [Y|n|d|q]"
                % (inst.instance_id, inst.instance_state.get_name())
            )
            answer = input(question)
            if answer.lower() in ("y", ""):
                return (inst, False)
            elif answer.lower() in ("n"):
                return (False, False)
            elif answer.lower() in ("d"):
                return (inst, True)
            elif answer.lower() in ("q"):
                self._no_more = True
                return (False, False)
            print("Huh? '%s'" % answer)
            answer = None

    def _has_case(self, inst):
        has_case = workflow_models.Case.objects.filter(
            **{"meta__camac-instance-id": inst.instance_id}
        ).exists()
        if has_case:
            log.info(
                "Not importing instance %s - case already exists" % inst.instance_id
            )
        return has_case

    def _instances(self):
        instances = (
            (inst, need_debugger)
            for inst, need_debugger in (
                self._ask_next(inst)
                for inst in Instance.objects.all()
                if not self._has_case(inst)
            )
            if inst
        )
        return instances

    def _setup(self, options):
        self._single_step = options.get("single", False)
        self._dry_run = options.get("dry", False)
        self._dev_mode = options.get("dev", False)

        verbosity = int(options.get("verbosity", 0))
        log.setLevel(max(10, 40 - (verbosity * 10)))

    def handle(self, *args, **options):
        self._setup(options)

        for instance, need_debugger in self._instances():
            try:
                self.migrate_instance(instance, need_debugger)
            except DryRun:
                log.info("Dry run: rolling back migration")
            except KeyboardInterrupt:
                log.fatal("User-requested stop. Current instance will not be saved")
                return
            except RuntimeError as exc:
                log.error(str(exc))
                # TODO: abort instance or whole migration?
                break

    def _make_case(self, inst, document):
        workflow = workflow_models.Workflow.objects.get(pk="building-permit")

        inst_user = inst.user.username

        state_id = inst.instance_state_id
        # Following instance state ids exist:
        # id   | Name       | Sort | Description
        #  1   | new        |    0 |
        # 21   | comm       |    1 |
        # 22   | ext        |    2 |
        # 23   | circ       |    4 |
        # 24   | redac      |    5 |
        # 25   | done       |    6 |
        # 26   | arch       |    8 |
        # 27   | del        |    9 |
        # 28   | new_portal |   10 |
        # 29   | nfd        |   11 |
        # 30   | subm       |   12 |
        # 31   | rej        |   13 |
        # 32   | ext_gem    |    3 |
        # 33   | old        |   14 | Archivdossier
        # 34   | control    |    7 |
        submitted = state_id not in (1, 28)

        case_status = (
            workflow_models.Case.STATUS_COMPLETED
            if submitted
            else workflow_models.Case.STATUS_RUNNING
        )
        item_status = (
            workflow_models.WorkItem.STATUS_COMPLETED
            if submitted
            else workflow_models.WorkItem.STATUS_READY
        )
        try:
            dossier_number = Answer.objects.get(
                instance_id=inst.instance_id, question_id=DOSSIER_NUMBER_QUESTION_ID
            )
        except Answer.DoesNotExist:
            dossier_number = None

        case = workflow_models.Case.objects.create(
            workflow=workflow,
            meta={
                "camac-instance-id": inst.instance_id,
                "migrated_from_old_camac": True,
                "dossier-number": dossier_number.answer if dossier_number else None,
                # TODO extract submit date from somewhere?
            },
            document=document,
            created_at=inst.creation_date,
            created_by_user=inst_user,
            created_by_group=None,
            status=case_status,
        )

        tasks = workflow.start_tasks.all()
        work_items = itertools.chain(
            *[
                [
                    workflow_models.WorkItem(
                        addressed_groups=groups,
                        task_id=task.pk,
                        deadline=task.calculate_deadline(),
                        document=form_models.Document.objects.create_document_for_task(
                            task, inst_user
                        ),
                        case=case,
                        status=item_status,
                        created_at=inst.creation_date,
                        created_by_user=inst_user,
                        created_by_group=None,
                    )
                    for groups in get_addressed_groups(task)
                ]
                for task in tasks
            ]
        )
        workflow_models.WorkItem.objects.bulk_create(work_items)
        return case

    def _make_document(self, inst):
        inst_user = inst.user.username
        document = form_models.Document.objects.create(
            form_id=self.get_caluma_form(inst.form_id),
            created_by_user=inst_user,
            created_by_group=None,
        )
        return document

    def _get_camac_answers(self, inst):
        ans = Answer.objects.filter(instance=inst).order_by(
            "chapter_id", "question_id", "item"
        )
        return ans

    def _get_row_doc(self, ind, *, root, index, table_ans, path_so_far_str):
        ans_doc = form_models.AnswerDocument.objects.filter(
            sort=index, answer=table_ans
        )

        if ans_doc.exists():
            return ans_doc.get().document
        else:
            document = form_models.Document.objects.create(
                family=root,
                form=table_ans.question.row_form,
                created_by_group=root.created_by_group,
                created_by_user=root.created_by_user,
            )
            form_models.AnswerDocument.objects.create(
                sort=index, answer=table_ans, document=document
            )
            log.debug(f"{ind}Creating table document {path_so_far_str} (row {index})")
            return document

    def _mark_table(self, slug):
        path = slug.split(".")

        if "*" in path:
            asterisk = path.index("*")
            # Mark the element before the asterisk, so we can get "warned"
            # early enough in the path traversal.
            path[asterisk - 1] = "*" + path[asterisk - 1]
        return path

    def _save_answer(self, document, slug, cqi, new_value, old_ans):
        root = document

        path = self._mark_table(slug)

        question_slug = path.pop()

        table_ans = None

        path_so_far = []

        for element in path:
            path_so_far.append(element)
            path_so_far_str = ".".join(path_so_far)
            ind = "  " * len(path_so_far)
            if element == "*" and table_ans:
                document = self._get_row_doc(
                    ind,
                    root=root,
                    path_so_far_str=path_so_far_str,
                    index=int(re.sub(r".*i", "", cqi)),
                    table_ans=table_ans,
                )

            elif element.startswith("*"):
                element = element[1:]

                # table_ans will be carried over to the next iteration
                table_ans, created = document.answers.get_or_create(question_id=element)
                if created:
                    log.debug(f"{ind}Creating table answer {path_so_far_str}")

            elif not document.answers.filter(question__slug=element).exists():
                log.error(
                    f"{ind}Form Subdocument '{path_so_far_str}' ({cqi}) is missing, "
                    f"questions below wont't be migrated"
                )
                return
            else:
                document = document.answers.get(question__slug=element).value_document

        ind = "  " * (len(path) + 1)
        try:
            self._create_and_store_answer(
                document,
                question_slug,
                new_value,
                ind=ind,
                cqi=cqi,
                slug=slug,
                root=root,
                old_ans=old_ans,
            )
        except Exception as exc:  # noqa
            log.exception(exc)
            __import__("pdb").set_trace()  # noqa
            pass

    def _create_and_store_answer(  # noqa
        self, document, question_slug, new_value, ind, cqi, slug, root, old_ans
    ):
        answer, created = document.answers.get_or_create(question_id=question_slug)
        if answer.meta is None or "migration_info" not in answer.meta:
            answer.meta = {"migrated_from_answerid": [], "migrated_from_questionid": []}

        answer.meta["migrated_from_answerid"].append(old_ans.pk)
        answer.meta["migrated_from_questionid"].append(old_ans.question_id)
        if answer.question.type == answer.question.TYPE_INTEGER:
            try:
                # some mild sanitizing
                value = re.sub("\.0*$", "", new_value)
                value = re.sub("['`]", "", value)
                if "price" in slug and "." in value:
                    # prices in francs is enough
                    value = re.sub(r"\.[0-9]+$", "", value)
                if value == "":
                    value = None
                if "." in value:
                    answer.value = float(value)
                else:
                    answer.value = int(value)
            except ValueError:
                log.critical(
                    f"{ind}Integer answer {slug} contains non-integer value: {new_value}"
                )
                __import__("pdb").set_trace()  # noqa
                pass
        elif answer.question.type == answer.question.TYPE_FLOAT:
            try:
                # some minimal sanitizing that doesn't affect the actual value
                answer.value = float(new_value.replace(",", "."))
            except ValueError:
                log.warning(
                    f"{ind}Float answer {slug} contains non-float value: {new_value}"
                )
                __import__("pdb").set_trace()  # noqa
                pass
        elif answer.question.type == answer.question.TYPE_DATE:
            try:
                answer.date = datetime.strptime(new_value, "%d.%m.%Y").date()
            except ValueError:
                __import__("pdb").set_trace()  # noqa
        else:
            answer.value = new_value
        answer.save()

        if created:
            log.debug(f"{ind}Migrated {cqi} to {slug} = '{new_value}'")

        if not created and new_value != answer.value:
            # multiple sources writing the same answer, but differing values - WTF
            log.warning(
                f"{ind}Question {slug}: {cqi} would overwrite existing value '{answer.value}' with '{new_value}'"
            )
            log.warning(
                f"{ind}Please check instance {root.case.meta['camac-instance-id']} for inconsistency"
            )

    def _camac_ans_cqi(self, ans):
        return "c%dq%di%d" % (ans.chapter_id, ans.question_id, ans.item)

    def _copy_answers(self, inst, document):
        question_map = self.QUESTION_MAP_BY_FORM[document.form_id]
        self._validate_map(question_map, document.form)

        camac_answers = self._get_camac_answers(inst)

        transform_by_cqi = defaultdict(list)
        for cqi, slug, transform in question_map:
            transform_by_cqi[cqi].append((slug, transform))

        count = 0
        for ans in camac_answers:
            try:
                cqi = self._camac_ans_cqi(ans)
                lookup = re.sub(r"i\d+$", "", cqi) + "i1"
                slugs_and_transforms = transform_by_cqi[lookup]

            except KeyError:
                if cqi in self.IGNORE_QUESTIONS:
                    continue
                chapter_prefix = re.sub(r"q.*$", "", cqi)
                if chapter_prefix in self.IGNORE_CHAPTERS:
                    continue

                self._log_missing_map(cqi=cqi, ans=ans)

                if self._dev_mode:
                    continue
                raise RuntimeError(
                    "Failed in answer migration of instance %d" % inst.instance_id
                )

            old_value = ans.answer
            for slug, transform in slugs_and_transforms:
                new_value = self._apply_transform(
                    transform,
                    old_value,
                    old_question=ans.question,
                    slug=slug,
                    document=document,
                    cqi=cqi,
                )
                if new_value not in EMPTY_VALUES:
                    # not only exclude None, but empty lists as well (for checkbox/multiselect answers)
                    self._save_answer(document, slug, cqi, new_value, old_ans=ans)
                    count += 1
        return count

    def _log_missing_map(self, cqi, ans):

        log.error("CAMAC -> Caluma Transform not found: %s" % cqi)
        log.error(
            "  Pages:    %s"
            % [
                cp.page.get_name()
                for cp in ChapterPage.objects.filter(chapter=ans.chapter)
            ]
        )
        log.error("  Chapter:  %s" % ans.chapter.get_name())
        log.error("  Question: %s" % ans.question.get_name())
        log.error("  Item:     %s" % ans.item)

        # Find and show candidates that could be used to fix config
        best_matches = form_models.Question.objects.annotate(
            match=Func(
                CombinedExpression(F("label"), "->", Value("de")),
                Value(ans.question.get_name()),
                function="similarity",
            )
        ).order_by("-match")[:5]

        had_matches = False
        for match in best_matches:
            if match.match < 0.4:
                log.error(
                    "  (no further useful matches found)"
                    if had_matches
                    else "  (no useful matches found)"
                )
                break
            had_matches = True
            log.error(
                f"  Possible Match ({match.match:.2f}): slug='{match.slug}' - {match.label.de}"
            )

    def _apply_transform(self, transform, old_value, **kwargs):
        # todo decide if transform supports kwargs

        if transform is None:
            raise RuntimeError(f"Transform {transform} incompatible")

        argspec = inspect.getfullargspec(transform)

        if len(argspec.kwonlyargs) + len(argspec.args) == 1:
            # "traditional" transform
            return transform(old_value)
        elif len(argspec.args) == 0:
            raise RuntimeError(f"Transform {transform} incompatible")

        return transform(
            old_value,
            **{
                arg: argval
                for arg, argval in kwargs.items()
                if arg in argspec.kwonlyargs or arg in argspec.args
            },
        )

    def _make_doc_slug(self, cat_name):
        # First, transliterate to get rid of umlauts
        question_slug = codecs.encode(
            "doc-" + cat_name.lower().replace(" ", "-"), "translit/long"
        )
        # Second, shorten / remove common words
        question_slug = re.sub(r"[,;\.]", "", question_slug)
        question_slug = re.sub(
            r"\b(einen|fuer|eine|oder|dass|der|und|die|das|um|dem|mit|des|wird)\b",
            "",
            question_slug,
        )
        question_slug = re.sub(r"\bbewilligung\b", "bew", question_slug)
        question_slug = re.sub(r"\bnachweis\b", "nachw", question_slug)
        question_slug = re.sub(r"\bhydrologisch\w*\b", "hyrol", question_slug)
        question_slug = re.sub(r"\b\w*gesuch\b", "ges", question_slug)
        question_slug = re.sub(r"\b\w*kapazitaet\b", "kap", question_slug)
        question_slug = re.sub(r"\b\w*bewilligung\b", "bew", question_slug)
        question_slug = re.sub(r"-+", "-", question_slug).strip("-")

        # last, strip word by word until short enough
        while len(question_slug) > 47:
            # max slug lenght is 50, we need some space for "-ja" suffix
            question_slug = "-".join(question_slug.split("-")[:-1])
        return question_slug

    def _matching_caluma_question(self, cat_name):
        EXCEPTION_MAP = {
            # "… Kann durch den Gesuchsteller / Behörde selber betitelt werden": "selber-betitelt-dokument",
            "… Kann durch den Gesuchsteller / Behörde selber betitelt werden": "andere-dokument",
            "Andere Dokumente": "andere-dokument",
            "Weitere Dokumente": "andere-dokument",
        }
        try:
            return form_models.Question.objects.get(
                label__de=cat_name, forms__in=["6-dokumente"]
            ).slug
        except form_models.Question.DoesNotExist:
            log.debug(
                "Question for category not found, checking outside of form '6-dokumente'"
            )
            if cat_name in EXCEPTION_MAP:
                return EXCEPTION_MAP[cat_name]
            question_slug = self._make_doc_slug(cat_name)
            question, created = form_models.Question.objects.get_or_create(
                type=form_models.Question.TYPE_CHOICE,
                slug=question_slug,
                defaults={"label": {"de": cat_name}},
            )
            if created:
                log.warning(
                    f"New document question in Caluma: slug={question_slug}, label={cat_name}"
                )
                option_yes = form_models.Option.objects.create(
                    slug=f"{question_slug}-ja", label={"de": cat_name}
                )
                form_models.QuestionOption.objects.create(
                    question=question, option=option_yes, sort=1
                )
            return question.slug
        except Exception:  # noqa
            __import__("pdb").set_trace()  # noqa

    @transaction.atomic
    def migrate_instance(self, inst, need_debugger):
        camac_form_name = inst.form.get_name()
        caluma_form = self.get_caluma_form(inst.form_id)

        log.info(
            f"Begin importing instance {inst.instance_id}: {camac_form_name} -> {caluma_form}"
        )
        self.stdout.write(
            f"Begin importing instance {inst.instance_id}: {camac_form_name} -> {caluma_form}"
        )

        if need_debugger:
            __import__("pdb").set_trace()  # noqa
        # first, create a case/document structure of the right type
        document = self._make_document(inst)
        self._make_case(inst, document)

        num_answers = self._copy_answers(inst, document)
        self._copy_address_data(inst, document)
        self._set_permit_type(inst, document)
        self._fill_checkbox_if_answer_exists(
            document, "umbauter-raum", "category", "category-hochbaute"
        )
        self._fill_checkbox_if_answer_exists(
            document, "purpose-description", "purpose", "purpose-andere"
        )
        self._fill_checkbox_if_answer_exists(
            document,
            "veranstaltung-andere-beschreibung",
            "veranstaltung-art",
            "veranstaltung-art-andere",
        )
        self._set_migrated_question(document)
        self._fill_journal_entries(document, inst)
        self._set_municipality(document, inst)
        self._extract_parcel_number(document, inst)
        if (
            inst.instance_state.name == "subm"
            and not document.case.meta["dossier-number"]
        ):
            document.case.meta[
                "dossier-number"
            ] = CreateInstanceLogic.generate_identifier(inst)
            document.case.save()

        log.info(
            f"Finished instance form for {inst.instance_id}, transferred {num_answers} answers"
        )
        self.stdout.write(
            f"Finished instance form for {inst.instance_id}, transferred {num_answers} answers"
        )

        if self._dry_run:
            raise DryRun()

    def _set_permit_type(self, inst, document):
        question = form_models.Question.objects.get(pk="form-type")
        caluma_form_mapping = {}
        for form_id, slug in uri_constants.CALUMA_FORM_MAPPING.items():
            caluma_form_mapping[form_id] = f"form-type-{slug}"

        try:
            value = caluma_form_mapping[inst.form.form_id]
        except KeyError as exc:
            print(f"Missing map for {exc}")
            print(question.options.all())
            raise

        if value:
            ans, _ = document.answers.get_or_create(question=question, value=value)

    def _set_municipality(self, document, inst):
        try:
            location = Location.objects.get(location_id=inst.location_id)
            question = form_models.Question.objects.get(slug="municipality")

            form_models.Answer.objects.get_or_create(
                value=str(location.pk),
                document=document,
                question=question,
            )
        except (form_models.Answer.DoesNotExist, Location.DoesNotExist):
            pass

    def _extract_parcel_number(self, document, inst):
        try:
            parcel_string = Answer.objects.get(question_id=91, instance=inst).answer
            street = Answer.objects.get(question_id=93, instance=inst).answer
            numbers = extract_parcels(parcel_string)
            table_ans, _ = document.answers.get_or_create(question_id="parcels")
            for (index, number) in enumerate(numbers):
                row_doc = self._get_row_doc(
                    "",
                    root=document,
                    index=index,
                    table_ans=table_ans,
                    path_so_far_str="",
                )
                form_models.Answer.objects.create(
                    question_id="parcel-number", document=row_doc, value=number
                )
                form_models.Answer.objects.create(
                    question_id="parcel-street", document=row_doc, value=street
                )

        except Answer.DoesNotExist:
            pass

    def _fill_journal_entries(self, document, inst):
        """Fill communication questions into journal entries."""

        admin_user = User.objects.get(pk=ADMIN_USER_ID)
        try:
            cantonal_audit_answer = Answer.objects.get(
                question_id=4, instance_id=inst.pk
            )
            cantonal_audit_answer_values = json.loads(cantonal_audit_answer.answer)
            answer_map = {
                "abm": "Brandschutz (ABM)",
                "afe": "Energienachweis",
                "qgp": "Sondernutzungsplanung (QGP / QP)",
                "nhsdenkmal": "kommunales Kulturobjekt (NHS Denkmalpflege)",
                "nhsschutz": "kommunales Schutzobjekt /-gebiet (NHS)",
            }
            value = map(lambda answer: answer_map[answer], cantonal_audit_answer_values)

            JournalEntry.objects.create(
                instance=inst,
                user=admin_user,
                text=f"Prüfung Gemeindeaufgaben durch kantonale Fachstellen (migriert): {', '.join(list(value))}",
                creation_date=now(),
                modification_date=now(),
                visibility="authorities",
            )
        except Answer.DoesNotExist:
            pass

        mitteilung_questions_map = [
            (1, "Mitteilung der Gemeinde (migriert): "),
            (181, "Mitteilung der zuständigen Koordinationsstelle (migriert): "),
            (256, "Mitteilung an Bürger (migriert): "),
        ]

        for question_id, value in mitteilung_questions_map:
            try:
                mitteilung_answer = Answer.objects.get(
                    question_id=question_id, instance_id=inst.pk
                )
                JournalEntry.objects.create(
                    instance=inst,
                    user=admin_user,
                    text=f"{value}{mitteilung_answer.answer}",
                    creation_date=now(),
                    modification_date=now(),
                    visibility="authorities",
                )
            except Answer.DoesNotExist:
                pass

    def _fill_checkbox_if_answer_exists(
        self, document, answer_to_check, checkbox_to_fill, answer_slug
    ):
        """Fill checkbox_to_fill with a given answer_slug if answer_to_check exists."""

        if not document.answers.filter(question_id=answer_to_check).exists():
            return

        if document.answers.filter(question_id=checkbox_to_fill).exists() and (
            answer_slug not in document.answers.get(question_id=checkbox_to_fill).value
        ):
            answer = document.answers.get(question_id=checkbox_to_fill)
            answer.value.append(answer_slug)
            answer.save()

        elif not document.answers.filter(question_id=checkbox_to_fill).exists():
            document.answers.create(
                question_id=checkbox_to_fill, document=document, value=answer_slug
            )

    def _set_migrated_question(self, document):
        question = form_models.Question.objects.get(slug="migrated-from-camac")
        document.answers.create(
            question=question, document=document, value="migrated-from-camac-yes"
        )

    def _copy_address_data(self, inst, document):
        applicant_table = document.answers.filter(question_id="applicant").first()
        if not applicant_table:
            # no applicant data, so we can't copy it's data to the other
            # entries.
            return
        applicant = applicant_table.documents.first()
        if not applicant:
            # We have the applicant table, but no row document.
            return

        involved_people_question = form_models.Question.objects.get(
            slug="more-people-involved"
        )
        answers = self._get_camac_answers(inst).filter(item=1, chapter=1)

        personal_data_config = [
            (68, [69], "invoice-recipient"),
            (79, [71, 222], "project-author"),
            (80, [82, 223], "landowner"),
        ]

        people_to_copy = [
            (qid, qids, value)
            for (qid, qids, value) in personal_data_config
            if answers.filter(question=qid).exists()
            and answers.get(question=qid).answer == "1"
        ]

        additional_people = [
            (qid, qids, value)
            for (qid, qids, value) in personal_data_config
            if any([answers.filter(question=q) for q in qids])
        ] + people_to_copy

        additional_people_answer = list(
            set(
                [
                    "more-people-involved-" + value
                    for (qid, qids, value) in additional_people
                ]
            )
        )

        form_models.Answer.objects.create(
            value=additional_people_answer,
            document=document,
            question=involved_people_question,
        )

        for (qid, qids, slug) in people_to_copy:
            table_ans, _ = document.answers.get_or_create(
                question_id=slug,
                question__type=form_models.Question.TYPE_TABLE,
            )
            table_ans.documents.add(applicant.copy())

    def _validate_map(self, question_map, form):  # noqa
        """Validate the question map.

        Check whether the target questions in Caluma actually exist and
        are of the correct type (structure wise): Are normal quesitons
        either in the top form, or a subform via form questions? And are
        table-questions actually found in the corresponding table?

        Print out the mapped structure of the target form, along with any
        errors, if any.
        """
        if id(question_map) in self._validated_maps:
            return
        questions = [
            caluma_question.split(".") for _, caluma_question, _ in question_map
        ]
        # make it into a tree
        map_tree = {}
        for q in questions:
            ptr = map_tree
            for fragment in q:
                ptr = ptr.setdefault(fragment, dict())

        # make tree structure from actual form
        def build_structure(frm, root, is_table):
            if is_table:
                root = {}
            if not frm.questions:
                __import__("pdb").set_trace()  # noqa
            for question in frm.questions.all():
                root[question.slug] = {}
                if question.type == question.TYPE_FORM:
                    # return irrelevant, updating root
                    build_structure(question.sub_form, root, False)
                elif question.type == question.TYPE_TABLE:
                    root[question.slug]["*"] = build_structure(
                        question.row_form, root, True
                    )
            return root

        form_tree = {}
        build_structure(form, form_tree, False)
        pprint(form_tree)

        def check(map_tree, form_tree, ind=""):
            status = True
            for question, tablemap in map_tree.items():
                status = status and question in form_tree
                result = "OK" if question in form_tree else "FAIL"
                if question == "*":
                    print(f"{ind}(table): {result}")
                else:
                    print(f"{ind}{question}: {result}")

                if tablemap:
                    status = status and check(
                        tablemap, form_tree[question], ind=ind + "   "
                    )
            return status

        if not check(map_tree, form_tree, ""):
            raise RuntimeError("Map structure invalid!")
        self._validated_maps.add(id(question_map))
