from datetime import datetime, timedelta

from caluma.caluma_form.models import Document
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from reversion.models import Version

from camac.core.translations import get_translations
from camac.instance.models import HistoryEntry, Instance, InstanceState
from camac.instance.serializers import SUBMIT_DATE_FORMAT
from camac.timelines.models import FormTimeline


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--commit", dest="commit", action="store_true", default=False
        )
        parser.add_argument("--force", dest="force", action="store_true", default=False)
        parser.add_argument(
            "-i",
            "--instance",
            type=int,
            default=None,
            dest="instance_id",
            help="Target instance for the migration",
            required=False,
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.init(options)
        sid = transaction.savepoint()

        instances = Instance.objects.order_by("pk")
        if self.filter_instance_id:
            instances = instances.filter(pk=self.filter_instance_id)

        if self.force:
            FormTimeline.objects.filter(instance__in=instances).delete()
            if self.verbosity >= 2:
                self.stdout.write(
                    self.style.WARNING(
                        f"== Deleted existing timelines for {instances.count()} instance(s) due to --force flag"
                    )
                )

        instances = instances.exclude(
            pk__in=FormTimeline.objects.values_list("instance_id", flat=True)
        )
        count_instances = 0
        count_timelines = 0
        all_timelines = []
        for instance in instances.iterator(chunk_size=250):
            count_instances += 1
            new_timelines = self._migrate_instance(instance=instance)
            all_timelines.extend(new_timelines)
            count_timelines += len(new_timelines)

        if count_timelines > 0:
            FormTimeline.objects.bulk_create(all_timelines)

        if options["commit"]:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Committing changes to database, {count_instances} instances migrated with {count_timelines} timelines"
                )
            )
            transaction.savepoint_commit(sid)
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"{count_instances} instances would have been changed with {count_timelines} timelines"
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    "Not committing changes to database. Run again with --commit to actually apply changes"
                )
            )
            transaction.savepoint_rollback(sid)

    def init(self, options):
        self.verbosity = options.get("verbosity", 1)
        self.force = options.get("force", False)
        self.filter_instance_id = options.get("instance_id", None)
        instance_state_correction = InstanceState.objects.get(
            name=settings.CORRECTION["INSTANCE_STATE"]
        )
        self.correction_state_id = str(instance_state_correction.pk)

    def _migrate_instance(self, instance):
        timelines = []

        created_date = self._get_document_created_date(instance)
        submit_date = self._get_submit_date(instance)

        last_date = created_date
        original_instance = instance.copy_source
        if original_instance:
            if submit_date:
                last_date = submit_date

            was_rejected = (
                original_instance.instance_state.name == "rejected"
                or original_instance.previous_instance_state.name == "rejected"
            )
            timeline_type = (
                FormTimeline.Type.PROJECT_CHANGE.value
                if not was_rejected
                else FormTimeline.Type.SUBMIT_AFTER_REJECTION.value
            )
            timelines.append(
                FormTimeline(
                    instance=instance,
                    timeline_type=timeline_type,
                    start_date=created_date,
                    end_date=submit_date,
                )
            )

        for start_date, end_date in self._get_corrections(instance, last_date):
            timelines.append(
                FormTimeline(
                    instance=instance,
                    timeline_type=FormTimeline.Type.CORRECTION.value,
                    start_date=start_date,
                    end_date=end_date,
                )
            )

        self._output_timelines(instance, timelines)

        return timelines

    def _offset_date(self, dte):
        """Add 1 second to/from a datetime."""
        return dte + timedelta(seconds=1)

    def _get_submit_date(self, instance):
        """Get the submit date from the instance.

        If no submit date exists on the case meta we ignore it.

        Otherwise, offset the end-result by +1 second to start the diff right after
        the submit date.
        """
        meta_submit_date = instance.case.meta.get("submit-date", None)
        if not meta_submit_date:
            return None

        return self._offset_date(
            datetime.strptime(meta_submit_date, SUBMIT_DATE_FORMAT)
        )

    def _get_document_created_date(self, instance):
        """Get the created date of the instance's document.

        If the instance has no source document, return the document's created date.

        Otherwise, return the date of the first document modification (~) history
        entry of the document, which indicates when the source answers were copied
        into the instance's document.

        Or fallback to the document's created date if no such history entry exists.

        Offset the end-result by +1 second to not include the timestamp in
        the timeline.
        """
        if not instance.case.document.source:
            return instance.case.document.created_at

        document_history_entry = (
            Document.history.filter(id=instance.case.document.pk, history_type="~")
            .order_by("history_date")
            .first()
        )

        return self._offset_date(
            document_history_entry.history_date
            if document_history_entry
            else instance.case.document.created_at
        )

    def _get_corrections(
        self, instance, last_date
    ) -> list[tuple[datetime, datetime | None]]:
        """Get correction periods for the instance.

        First try to get them from reversion versions. If no versions are found,
        fall back to HistoryEntries.
        """
        reversion_versions = Version.objects.get_for_object(instance).order_by(
            "revision__date_created"
        )

        return (
            self._get_corrections_from_reversion(instance, reversion_versions)
            if reversion_versions.exists()
            else self._get_corrections_from_historyentries(instance, last_date)
        )

    def _get_corrections_from_reversion(
        self,
        instance,
        versions,
    ) -> list[tuple[datetime, datetime | None]]:
        """Parse reversion versions to extract correction periods.

        Each time the instance_state changes to the correction state, a correction
        period starts. When the instance_state changes back to any other state, the
        correction period ends.

        If the instance is still in correction state at the end of the versions, an
        open correction period is appended.
        """
        corrections = []
        correction_start = None

        for version in versions:
            version_instancestate = str(version.field_dict.get("instance_state_id"))

            # if the state changed to correction, we start the correction period.
            if (
                not correction_start
                and version_instancestate == self.correction_state_id
            ):
                correction_start = version.revision.date_created

            # if we were in correction and the state changed back, we close the period.
            if correction_start and version_instancestate != self.correction_state_id:
                corrections.append((correction_start, version.revision.date_created))
                correction_start = False

        # add open correction period if instance is still in correction state.
        if (
            correction_start
            and str(instance.instance_state.pk) == self.correction_state_id
        ):
            corrections.append((correction_start, None))

        return corrections

    def _get_corrections_from_historyentries(
        self,
        instance,
        last_date,
    ) -> list[tuple[datetime, datetime | None]]:
        """Fallback method to parse HistoryEntries for correction periods.

        Each HistoryEntry with the correction message indicates the end of a correction
        period. The start of the correction period is the end date of the previous
        correction period, or the dossier start date for the first correction period.
        """
        corrections = []
        corrected_translations = set(get_translations("Dossier corrected").values())

        entries = (
            HistoryEntry.objects.filter(instance=instance)
            .filter(trans__title__in=corrected_translations)
            .order_by("created_at")
            .distinct()
        )

        loop_date = last_date
        for entry in entries:
            start_date = loop_date
            end_date = entry.created_at
            corrections.append((start_date, end_date))
            loop_date = end_date

        # add open correction period if instance is still in correction state.
        if str(instance.instance_state.pk) == self.correction_state_id:
            corrections.append((loop_date, None))

        return corrections

    def _output_skipped(self, message):
        """Output utility for skipped instances based on verbosity level."""
        if self.verbosity >= 2:
            self.stdout.write(self.style.WARNING(message))

    def _output_timelines(self, instance, timelines):
        """Output created timelines based on verbosity level."""
        if self.verbosity >= 2:
            if len(timelines) == 0:
                self.stdout.write(
                    self.style.WARNING(
                        f" x Dossier {instance.pk}: no timelines created"
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f" + Dossier {instance.pk}: created {len(timelines)} timeline(s)"
                    )
                )
                for tl in timelines:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"      - {tl.timeline_type}: {tl.start_date} - {tl.end_date}"
                        )
                    )
