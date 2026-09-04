import datetime
import logging
import os
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import Any

import openpyxl
from caluma.caluma_form import calc_questions, structure
from caluma.caluma_form.models import Answer, Document, FormQuestion, Question
from caluma.caluma_form.validators import DocumentValidator
from django.core.management.base import BaseCommand
from django.db import connections, transaction
from django.db.models import Exists, OuterRef, Q
from rest_framework import exceptions

from camac.alexandria_migration.domain_logic.annotate_documents import (
    SynchronousExecutor,
)
from camac.instance.models import Instance
from camac.instance.utils import get_municipality
from camac.user.models import Group, Service

log = logging.getLogger(__name__)


@dataclass
class LogEntry:
    level: str
    message: str
    args: list[str] = field(default_factory=list)


@dataclass
class RecalcInfo:
    name: str
    hidden: bool
    before: float | None
    after: float | None
    event: str


@dataclass
class StatsEntry:
    municipality: str
    instance: str
    recalculations: list[RecalcInfo] = field(default_factory=list)


class Command(BaseCommand):
    EXCLUDE_STATES_FOR_VALIDATION = [
        # matches InstanceState.name, which in BE is the untranslated internal name
        # "new",  # applicants will see errors before submission and can correct themselves
        # "correction",  # in correction - municipality will see the validation errors
        # # dossiers that are not being processed anymore don't need to be fixed either
        # "rejected",
        # "finished",
        # "finished_internal",
    ]

    EXCLUDE_STATES_FOR_MISCALCULATION = [
        # Here, we do need the new, and in "correction" dossiers as well
        # dossiers that are not being processed anymore don't need to be fixed either
        # as discussed - we need to look at all states
        # "rejected",
        # "finished",
        # "finished_internal",
    ]

    EXCLUDE_STATES_FOR_FIXING = [
        # ... none - for now
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # there won't be another command while this one's
        # running, so don't worry about that
        type(self).pid = os.getpid()

        # municipality -> instance -> list[fixes]
        self.stats = defaultdict(lambda: defaultdict(list))

        type(self)._user = SimpleNamespace(
            username="Admin",
            # caluma user - expects group to be a service ¯\_(ツ)_/¯
            group=Group.objects.filter(trans__name="Admin").distinct().get().service,
        )

    def add_arguments(self, parser):
        parser.add_argument(
            "--parallel",
            action="store_true",
            dest="parallel",
            help="Check in parallel. Uses as many CPUs as available",
            required=False,
            default=False,
        )
        parser.add_argument(
            "--dev",
            action="store_true",
            dest="dev_mode",
            help="Dev mode: Only select ~100 instances to check",
            required=False,
            default=False,
        )
        parser.add_argument(
            "--analyze-only",
            type=str,
            dest="analyze_only",
            help=(
                "Instead of going through all calc questions, only look for "
                "the given one and the ones depending on it. Can be a "
                "comma-separated list of question slugs"
            ),
            required=False,
            default=None,
        )
        parser.add_argument(
            "--search-only",
            type=str,
            dest="search_only",
            help=(
                "Find dossiers with existing answers to the given question "
                "only, instead of all dossiers with calc fields"
            ),
            required=False,
            default=None,
        )

        parser.add_argument(
            "--check-recalc",
            action="store_true",
            dest="do_recalc",
            help="Enable recalculation checks",
            required=False,
            default=False,
        )
        parser.add_argument(
            "--check-validation",
            action="store_true",
            dest="do_validate",
            help="Enable form validation checks",
            required=False,
            default=False,
        )

        parser.add_argument(
            "--fix-calculation",
            action="store_true",
            dest="do_fix_calc",
            help="Recalculate incorrect answers and save changes to DB",
            required=False,
            default=False,
        )
        parser.add_argument(
            "--commit",
            action="store_true",
            dest="do_commit",
            help="Commit changes to DB. Only has an effect together with --fix-calculation",
            required=False,
            default=False,
        )
        parser.add_argument(
            "--excel-out",
            type=str,
            dest="excel_out",
            help="Specify excel filename for detailled output",
            required=False,
        )

    def handle(self, *args, **options):
        self.configure_logging(options["verbosity"])

        chosen_executor = (
            ProcessPoolExecutor if options["parallel"] else SynchronousExecutor
        )
        self.verbosity = options["verbosity"]

        do_validate = options["do_validate"]
        do_recalc = options["do_recalc"]
        do_fix_calculation = options["do_fix_calc"]
        do_commit = options["do_commit"]
        self.excel_out = options["excel_out"]
        self.dev_mode = options["dev_mode"]
        self.analyze_only = (
            options["analyze_only"].split(",") if options["analyze_only"] else None
        )
        self.search_only = options["search_only"]

        started_at = datetime.datetime.now()

        if not do_commit:
            log.info("Pretend mode active: Changes will not be committed to DB")

        with chosen_executor() as executor:
            try:
                if do_validate:
                    log.info("Collecting instances for validation checks")
                    total, qs = self.iter_instances_for_validation()
                    self._schedule(
                        "Validation check", executor, self.check_validation, total, qs
                    )

                if do_recalc:
                    if self.analyze_only:
                        log.info(
                            "Collecting instances for miscalculation checks (only questions "
                            f"{', '.join(self.analyze_only)} and dependents)"
                        )
                    else:
                        log.info(
                            "Collecting instances for miscalculation checks "
                            "(checking ALL calc questions)"
                        )
                    total, instances = self.iter_instances_for_miscalculation()
                    self._schedule(
                        "Recalculation check",
                        executor,
                        self.check_miscalculation,
                        total,
                        instances,
                        analyze_only=self.analyze_only,
                        fix_calculation=do_fix_calculation,
                        do_commit=do_commit,
                    )

            except KeyboardInterrupt:
                log.error("User triggered stop, shutting down")
                executor.shutdown(wait=True, cancel_futures=True)
            except Exception as exc:
                log.error("Some error happened, stopping: %s", str(exc))
                executor.shutdown(wait=True, cancel_futures=True)

        self.log_stats()
        if self.excel_out:
            self.log_to_excel(
                start_time=started_at,
                committed_to_db=do_commit,
                did_fixes=do_fix_calculation,
            )

    def log_to_excel(self, start_time, committed_to_db, did_fixes):

        book = openpyxl.Workbook()

        info_sheet = book.create_sheet("Info")
        ana_sheet = book.create_sheet("Analysis")
        fix_sheet = book.create_sheet("Fixes")
        stats_sheet = book.create_sheet("Statistics")

        info_sheet.column_dimensions["A"].width = 30
        info_sheet.column_dimensions["B"].width = 40
        info_sheet["A1"] = "Started at"
        info_sheet["B1"] = start_time
        info_sheet["B1"].alignment = openpyxl.styles.Alignment(horizontal="left")

        info_sheet["A2"] = "Completed at"
        info_sheet["B2"] = datetime.datetime.now()
        info_sheet["B2"].alignment = openpyxl.styles.Alignment(horizontal="left")

        info_sheet["A3"] = "Recalculation mode"
        info_sheet["B3"] = (
            f"Check only {', '.join(self.analyze_only)} and dependents"
            if self.analyze_only
            else "Check full form"
        )
        info_sheet["B3"].alignment = openpyxl.styles.Alignment(horizontal="left")

        info_sheet["A4"] = "Fix mode"
        info_sheet["B4"] = "Enabled" if did_fixes else "Disabled"
        info_sheet["B4"].alignment = openpyxl.styles.Alignment(horizontal="left")
        info_sheet["A5"] = "Note about significance"
        info_sheet["B5"] = (
            "Significant change means: Numeric difference of non-zero, in a visible field.\n"
            "Changes in a hidden field are always minor, as are changes from 0 to empty and vice versa"
        )

        if did_fixes:
            # only useful if we did fixes - otherwise, DB is not updated anyway
            info_sheet["A6"] = "Changes written to DB"
            info_sheet["B6"] = (
                "Yes, DB updated" if committed_to_db else "No, pretend mode was run"
            )
            info_sheet["B6"].alignment = openpyxl.styles.Alignment(horizontal="center")

        # delete any default sheets
        for name in book.sheetnames:
            if name not in ("Info", "Analysis", "Fixes", "Statistics"):
                book.remove(book[name])

        hdr_font = openpyxl.styles.Font(color="101030", bold=True, size=13)

        # info sheet formatting: first column = labels
        for hdr_row in info_sheet["A1:A30"]:
            for cell in hdr_row:
                cell.font = hdr_font

        ana_rows, fix_rows = self._collect_logs_for_excel(ana_sheet, fix_sheet)
        self._collect_stats_for_excel(stats_sheet)

        for sheet in ana_sheet, fix_sheet, stats_sheet:
            for hdr_row in sheet["A1:Z1"]:
                for cell in hdr_row:
                    cell.font = hdr_font

        if not fix_rows:
            # easier to add and remove than to check for it in every iteration
            book.remove_sheet(fix_sheet)

        book.save(self.excel_out)

    def _collect_logs_for_excel(self, ana_sheet, fix_sheet):
        ana_rows = 0
        fix_rows = 0

        header = [
            "Municipality or Applicant",
            "Instance",
            "Field",
            "Value before",
            "Value after",
        ]

        ana_header = header + ["Significant"]

        ana_sheet.append(ana_header)
        fix_sheet.append(header)

        ana_widths = [len(t) for t in ana_header]
        fix_widths = [len(t) for t in header]

        for mun, instance_data in self.stats.items():
            for instance, recs in instance_data.items():
                recs: list[RecalcInfo]
                fixed = [r for r in recs if r.event == "fixed"]
                detected = [r for r in recs if r.event == "detected"]

                for det in detected:
                    name = f"{det.name}{' (hidden)' if det.hidden else ''}"
                    row = [
                        mun,
                        instance,
                        name,
                        det.before,
                        det.after,
                        "yes"
                        if self._is_significant(det.before, det.after, det.hidden)
                        else "no",
                    ]
                    ana_sheet.append(row)
                    ana_rows += 1

                    # precalc widths for formatting later
                    widths = [len(str(c)) for c in row]
                    ana_widths = [
                        max(a, b) for a, b in zip(ana_widths, widths, strict=True)
                    ]

                for fix in fixed:
                    row = [mun, instance, fix.name, fix.before, fix.after]
                    fix_sheet.append(row)
                    fix_rows += 1

                    # precalc widths for formatting later
                    widths = [len(str(c)) for c in row]
                    fix_widths = [
                        max(a, b) for a, b in zip(fix_widths, widths, strict=True)
                    ]
        ana_filters = ana_sheet.auto_filter
        ana_filters.ref = f"A1:F{ana_rows + 1}"

        fix_filters = fix_sheet.auto_filter
        fix_filters.ref = f"A1:E{fix_rows + 1}"

        self._adjust_excel_cols(ana_sheet, ana_widths)
        self._adjust_excel_cols(fix_sheet, fix_widths)
        return ana_rows, fix_rows

    def _adjust_excel_cols(self, sheet, widths):
        for colindex, width in enumerate(widths, start=1):
            sheet.column_dimensions[
                openpyxl.utils.get_column_letter(colindex)
            ].width = width

    @classmethod
    def _is_significant(cls, a, b, hidden):
        if hidden:
            return False
        acceptable = {(0.0, None), (None, 0.0)}
        return (a, b) not in acceptable

    def _collect_stats_for_excel(self, stats_sheet):

        header = [
            "Municipality or applicant",
            "Significant miscalculations",
            "Minor miscalculations",
        ]

        stats_sheet.append(header)
        stat_widths = [len(t) for t in header]

        counter = defaultdict(lambda: {"sig": 0, "minor": 0})

        for mun, instance_data in self.stats.items():
            for recs in instance_data.values():
                recs: list[RecalcInfo]
                detected = [r for r in recs if r.event == "detected"]
                if not detected:
                    continue

                detected_sig = any(
                    r
                    for r in detected
                    if self._is_significant(r.before, r.after, r.hidden)
                )
                if detected_sig:
                    counter[mun]["sig"] += 1
                else:
                    counter[mun]["minor"] += 1

        for mun in sorted(counter.keys()):
            data = counter[mun]
            row = [mun, data["sig"], data["minor"]]
            widths = [len(str(c)) for c in row]
            stat_widths = [max(a, b) for a, b in zip(stat_widths, widths, strict=True)]
            stats_sheet.append(row)
        self._adjust_excel_cols(stats_sheet, stat_widths)

        stats_filters = stats_sheet.auto_filter
        stats_filters.ref = f"A1:C{len(counter) + 1}"

    def log_stats(self):
        """
        Log statistics about the detection or fix in this run.

        Note: We explicitly only log statistics - for details, check the log itself.
        """

        for mun, instance_data in self.stats.items():
            log.info("%s: %d instances affected", mun, len(instance_data))
            if self.verbosity >= 1:
                for instance, recs in instance_data.items():
                    recs: list[RecalcInfo]

                    fixed = len([r for r in recs if r.event == "fixed"])
                    detected = [r for r in recs if r.event == "detected"]

                    detected_sig = len(
                        [
                            r
                            for r in detected
                            if self._is_significant(r.before, r.after, r.hidden)
                        ]
                    )

                    if fixed:
                        log.info("   %s: fixed %d miscalculations", instance, fixed)
                    elif detected:
                        # Only log detection if we don't have anything to fix
                        # (no fix mode). If fixes were made, it's implicitly
                        # clear that there was a detection

                        # detection stops at the first miscalc, so there's normally
                        # only one, despite multiple possible miscalculations
                        if detected_sig:
                            log.info(
                                "   %s: detected at least one significant miscalculation",
                                instance,
                            )
                        else:
                            log.info(
                                "   %s: detected at least one minor miscalculation",
                                instance,
                            )

    def _schedule(self, progress_label, executor, task, total, instances, **kwargs):
        for i, inst in enumerate(instances, start=1):
            progressinfo = f"[{progress_label} {i}/{total}]"
            fut = executor.submit(task, progressinfo, inst.pk, **kwargs)
            fut.add_done_callback(self._log_result)

    def _log_result(self, logdata):
        result = logdata.result()
        assert isinstance(result, list)
        for entry in result:
            match entry:
                case LogEntry(level, message, args):
                    log.log(level, message, *args)

                case StatsEntry(municipality, instance, recalculations):
                    self.stats[municipality][instance].extend(recalculations)
                case _:
                    raise RuntimeError(f"Unknown result received: {result}")

    def configure_logging(self, verbosity):
        """Configure logging to the commandline's verbosity level."""

        if verbosity > 2:
            level = logging.DEBUG
        elif verbosity == 2:
            level = logging.INFO
        else:
            level = logging.WARNING

        log.setLevel(level)

        def _config_handler(logger):
            for handler in logger.handlers:
                if isinstance(handler, logging.StreamHandler):
                    # only stream handlers - don't wanna send every debug line
                    # to the admins
                    handler.setLevel(level)
            if logger.propagate and logger.parent:
                # parent handlet needs level set as well
                _config_handler(logger.parent)

        _config_handler(log)

    @classmethod
    def check_validation(cls, progressinfo, inst_id):
        """Check the given instance for validation issues.

        Validate the main form of the given instance, and give a warning
        if anything is found.

        Return a loggable tuple, so it can be logged in the main process
        """
        cls._clean_env()
        inst = Instance.objects.prefetch_related("case", "case__document").get(
            pk=inst_id
        )

        struc = cls._struc(inst)
        validator = DocumentValidator()

        mun = cls._municipality(inst)

        try:
            validator.validate(
                struc._document, user=cls._user, validation_context=struc
            )
        except exceptions.ValidationError as exc:
            return [
                LogEntry(
                    logging.WARNING,
                    "%s Instance %s (%s) for %s: Invalid form found (%s)",
                    [
                        progressinfo,
                        inst.pk,
                        inst.instance_state.get_name(),
                        mun,
                        exc,
                    ],
                )
            ]
        except Exception as exc:
            return [
                LogEntry(
                    logging.WARNING,
                    "%s Instance %s (%s) for %s: Error during validation (%s)",
                    [
                        progressinfo,
                        inst.pk,
                        inst.instance_state.get_name(),
                        mun,
                        exc,
                    ],
                )
            ]
        return [
            LogEntry(
                logging.DEBUG,
                "%s Instance %s (%s) for %s: Validation seems OK",
                [
                    progressinfo,
                    inst.pk,
                    str(inst.instance_state.get_name()),
                    mun,
                ],
            )
        ]

    @staticmethod
    def _struc(instance) -> structure.FieldSet:
        """Return the Caluma form structure for the given instance."""

        struc = structure.FieldSet(instance.case.document)
        return struc

    @classmethod
    def _all_calc_fields(cls, struc):
        return calc_questions.DependencyList(
            *(
                field
                for field in struc.get_all_fields()
                if field.question.type == Question.TYPE_CALCULATED_FLOAT
            )
        )

    @classmethod
    def _municipality(cls, inst):
        try:
            return get_municipality(inst).get_name()
        except (Service.DoesNotExist, Answer.DoesNotExist):
            # Most likely a new dossier - fetch applicant instead
            return cls._first_applicant(inst) or "?? Unknown"

    @classmethod
    def _first_applicant(cls, inst: Instance):
        first_applicant = inst.involved_applicants.filter(user__isnull=False).first()
        if not first_applicant:
            return
        user = first_applicant.user
        return f"Applicant {user.surname}, {user.name} ({user.email})"

    @classmethod
    def check_miscalculation(
        cls,
        progressinfo: str,
        inst_id: int,
        analyze_only: list[str],
        fix_calculation: bool,
        do_commit: bool,
    ) -> list[LogEntry | StatsEntry]:
        """Check the given instance for miscalculation issues.

        If user requested only checking a specific question (via
        `analyze_only`), we find said question and it's dependents, then
        check these. If not, we check the full form for miscalculations.

        Return a loggable tuple, so it can be logged in the main process
        """
        cls._clean_env()
        inst = Instance.objects.prefetch_related("case", "case__document").get(
            pk=inst_id
        )
        struc = cls._struc(inst)

        acceptable_mismatches: set[tuple[Any, Any]] = {
            # For safety, we only accept mismatches where the *new* value is
            # None. Any other mismatch, even None->0.0 is problematic
            # as it could trigger downstream miscalculations, at least in the
            # backend
            (0.0, None),
        }

        if analyze_only:
            # only "interesting" ones
            check_list = calc_questions.DependencyList(
                *[struc.get_field(f) for f in analyze_only]
            )
        else:
            # Full scan - is about 50% slower
            check_list = cls._all_calc_fields(struc)

        municipality_name = cls._municipality(inst)

        miscalculation_in_hidden_fields = 0

        logdata = []

        instance_state = str(inst.instance_state.get_name())

        found_error = False

        for fld in check_list:
            fld: structure.BaseField
            if fld.question.type == Question.TYPE_CALCULATED_FLOAT:
                fld: structure.ValueField
                value = fld.get_value(ignore_hidden=True)
                new_value = fld.calculate()

                if (
                    value != new_value
                    and (value, new_value) not in acceptable_mismatches
                ):
                    info = RecalcInfo(
                        name=fld.get_path(),
                        hidden=fld.is_hidden(),
                        before=value,
                        after=new_value,
                        event="detected",
                    )
                    logdata.append(
                        StatsEntry(
                            municipality_name, f"{inst_id} ({instance_state})", [info]
                        )
                    )

                    if not fld.is_visible():
                        # Field is hidden, so recalculation errors do not matter
                        miscalculation_in_hidden_fields += 1
                        continue

                    # miscalculation in visible field - log warning and remember to fix
                    # if fix mode is active
                    found_error = True

                    logdata.append(
                        LogEntry(
                            logging.WARNING,
                            "%s Instance %s (%s) for %s: Miscalculation found in %s (current value %s, calculated %s)",
                            [
                                progressinfo,
                                inst.pk,
                                instance_state,
                                str(municipality_name),
                                str(fld.get_path()),
                                value,
                                new_value,
                            ],
                        )
                    )
                    if cls._is_significant(value, new_value, fld.is_hidden()):
                        # We found a *significant* miscalculation, don't need to find more here.
                        # The fix code will fix all subsequent miscalculations
                        # anyway.
                        # We don't break on *insignificant* ones: We still want
                        # to collect stats and *know* if there's a significant
                        # miscalculation downstream even if we detected a problem already
                        break

        if not found_error:
            # No miscalculation found in *visible* fields, but maybe in hidden?
            miscalc_info = ""
            level = logging.DEBUG
            if miscalculation_in_hidden_fields:
                # Some hidden fields had miscalculations. Report as such
                miscalc_info = (
                    f" ({miscalculation_in_hidden_fields} "
                    "hidden fields had inconsistent calculations)"
                )
                level = logging.INFO

                # Note: We do *not* report miscalculations in hidden fields
                # for the statistics - only for visible ones. The recalculation
                # will still take place though (if activated)

            logdata.append(
                LogEntry(
                    level,
                    "%s Instance %s: OK, no problematic miscalculations found%s",
                    [
                        progressinfo,
                        inst.pk,
                        miscalc_info,
                    ],
                )
            )

        if fix_calculation and (found_error or miscalculation_in_hidden_fields):
            # Fix mode is active: We recalculate if ANY miscalculation
            # was found (`found_error` means it was found in a visible field,
            # `miscalculation_in_hidden_fields` is of course in hidden fields)
            logdata.extend(
                cls._recalculate(
                    municipality_name,
                    inst=f"{inst_id} ({instance_state})",
                    struc=struc,
                    do_commit=do_commit,
                )
            )

        return logdata

    @classmethod
    def _recalculate(
        cls, municipality: str, inst: str, struc: structure.FieldSet, do_commit: bool
    ):
        before_values = {
            fld.get_path(): fld.get_value(ignore_hidden=True)
            for fld in cls._all_calc_fields(struc)
        }
        recalc_log = [
            LogEntry(logging.INFO, "    Instance %s: Recalculating fields", [inst])
        ]

        with transaction.atomic():
            savepoint = transaction.savepoint()
            calc_questions.recalculate_all_calc_fields(struc)
            after_values = {
                fld.get_path(): (fld.is_hidden(), fld.get_value(ignore_hidden=True))
                for fld in cls._all_calc_fields(struc)
            }

            recalcs = []

            for path, value_before in before_values.items():
                after_is_hidden, after_value = after_values[path]
                hiddenstate = "hidden " if after_is_hidden else ""

                if value_before != after_value:
                    recalc_log.append(
                        LogEntry(
                            logging.DEBUG,
                            "    Instance %s: %sfield %s was recalculated (old: %s, new: %s)",
                            [inst, hiddenstate, path, value_before, after_value],
                        )
                    )
                    recalcs.append(
                        RecalcInfo(
                            name=path,
                            hidden=after_is_hidden,
                            before=value_before,
                            after=after_value,
                            event="fixed",
                        )
                    )

            if recalcs:
                recalc_log.append(StatsEntry(municipality, inst, recalcs))
            if not do_commit:
                recalc_log.append(
                    LogEntry(
                        logging.DEBUG,
                        "    Rolling back changes, pass --commit to save permanently",
                        [],
                    )
                )

                transaction.savepoint_rollback(savepoint)
        return recalc_log

    def _all_forms_with_calc_questions(self) -> list[str]:
        """Return list of form slugs that contain calculated fields in the structure."""

        seen = set()

        def _collect_forms(questions):

            forms = (
                FormQuestion.objects.filter(question__in=questions)
                .exclude(form__in=seen)
                .values_list("form_id", flat=True)
            )

            yield from forms
            seen.update(forms)

            parent_q = Question.objects.filter(
                Q(row_form__in=forms) | Q(sub_form__in=forms)
            )
            if parent_q.count():
                yield from _collect_forms(parent_q)

        return sorted(
            set(
                _collect_forms(
                    Question.objects.filter(type=Question.TYPE_CALCULATED_FLOAT)
                )
            )
        )

    def _base_qs(self):
        """Build a base queryset for fetching affected instances."""
        if self.search_only:
            log.info(f"Collecting all instances with an answer to {self.search_only}")
            return Instance.objects.all().filter(
                Exists(
                    Answer.objects.filter(
                        question_id=self.search_only,
                        document__case__pk=OuterRef("case"),
                    )
                )
            )

        else:
            forms = self._all_forms_with_calc_questions()
            log.info(
                f"Collecting all instances whose form contains "
                f"collected fields: {', '.join(forms)}"
            )
            return Instance.objects.all().filter(
                Exists(
                    Document.objects.filter(
                        form__in=forms,
                        case__pk=OuterRef("case"),
                    )
                )
            )

    def iter_instances_for_validation(self):
        """Build an iterator for validation checks.

        Return a 2-tuple, with the total number of records as the first value,
        and a queryset iterator as the second value.
        """

        qs = self._base_qs().exclude(
            instance_state__name__in=self.EXCLUDE_STATES_FOR_VALIDATION
        )
        if self.dev_mode:
            qs = qs[:100]

        return qs.count(), qs.iterator(chunk_size=200)

    def iter_instances_for_miscalculation(self):
        """Build an iterator for miscalculation checks.

        Return a 2-tuple, with the total number of records as the first value,
        and a queryset iterator as the second value.
        """
        qs = (
            self._base_qs()
            .exclude(instance_state__name__in=self.EXCLUDE_STATES_FOR_MISCALCULATION)
            # order by random to get an early sampling of all situations
            .order_by("?")
        )
        if self.dev_mode:
            qs = qs[:100]

        return (qs.count(), qs.iterator(chunk_size=200))

    @classmethod
    def _clean_env(cls):
        """
        Clean system environment.

        Make sure subprocess workers have their own DB connection
        """

        if hasattr(cls, "worker_pid"):
            # already cleaned (or in a single-proc runtime)
            return
        cls.worker_pid = os.getpid()

        # Disconnect / Reconnect django DB connection as we don't want
        # to share the DB connection with the other workers
        # ... but only if we're actually in a subprocess

        if cls.worker_pid != cls.pid:
            connections["default"].connection = None
