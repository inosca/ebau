import datetime
from typing import Dict, List, Tuple

from caluma.caluma_form.models import Answer, Document
from caluma.caluma_workflow.models import WorkItem
from django.db.models import Avg, Count, IntegerField, OuterRef, QuerySet, Subquery
from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import Cast

from camac.instance.master_data import MasterData
from camac.instance.models import Instance


def _get_previously_rejected_instance(instance: Instance):
    return Instance.objects.filter(
        case__document__source=instance.case.document,
        instance_state__name="finished",
        previous_instance_state__name="rejected",
    ).first()


def _get_rejected_instance_cycletime(rejected_instance: Instance) -> int:
    """
    As of now there are two methods to get a previously rejected application's cycle time.

     a. from the InstanceLog that would require us to filter a potentially enourmous list of strings formed
     `{"INSTANCE_STATE_ID":80000,"PREVIOUS_INSTANCE_STATE_ID":20001,"MODIFICATION_DATE":"2018-07-16 16:14:09+02:00"}`
        Probably a bad path.

     b. from the HistoryEntry that is created on rejection.
       Problems are that we rely on the exact phrasing of an entry's title that is also translated and potentially
       subject to change.

    @param rejected_instance:
    @return:
    """
    end_date = (
        rejected_instance.history.filter(
            # CAVEAT: when changing translation this must be updated to reflect the changes
            trans__language="de",
            trans__title="Dossier zurückgewiesen",
        )
        .order_by("-created_at")
        .first()
    )
    start_date = rejected_instance.creation_date
    return (end_date or 0) and (end_date.created_at - start_date).days


def _compute_total_idle_days(
    sorted_durations: List[Tuple[datetime.datetime, datetime.datetime]]
) -> int:
    """
    Compute total idle days from a set of durations that may encompass and overlap one another.

    Overlaps should be counted only once.

    The argument `sorted_durations` is a list of tuples holding a datetime object for the beginning and
    the end of a duration respectively

    Returns the total idle time in days as an integer
    """

    merged_ranges = []
    elim = []
    for i in range(len(sorted_durations)):
        if i in elim:
            continue
        start, end = sorted_durations[i]
        while True:
            try:
                next_start, next_end = sorted_durations[i + 1]
            except IndexError:
                break
            if next_start < end:
                if next_end < end:
                    elim.append(i + 1)
                    i += 1
                else:
                    end = next_end
                    i += 1
                    elim.append(i)
            else:
                # apparently this is not explicitly covered anymore but it still
                # breaks the loop as expected, is this a change in python 3.8?
                break  # pragma: no cover
        merged_ranges.append((start, end))
    return sum(map(lambda duration: (duration[1] - duration[0]).days, merged_ranges))


def _retrieve_waiting_periods(
    instance: Instance,
) -> List[Tuple[datetime.datetime, datetime.datetime]]:
    """
    Retrieve a list of waiting periods from an Instance's claims.

    A claim is an answer document in the answer table `nfd-tabelle`

    Returns the list sorted ASC by start time of the duration
    """

    rows = Document.objects.filter(
        form_id="nfd-tabelle",
        family__work_item__task_id="nfd",
        family__work_item__case=instance.case,
    )

    try:
        decision_date = Answer.objects.get(
            question_id="decision-date",
            document__work_item__case__instance=instance,
            document__work_item__status=WorkItem.STATUS_COMPLETED,
        ).date
    except Answer.DoesNotExist:
        decision_date = None

    results = []
    for row in rows.iterator():
        request_answer = row.answers.filter(
            question_id="nfd-tabelle-datum-anfrage"
        ).first()
        response_answer = row.answers.filter(
            question_id="nfd-tabelle-datum-antwort"
        ).first()
        if (request_answer and request_answer.date) is None or (
            response_answer and response_answer.date
        ) is None:
            continue
        if response_answer.date > decision_date:
            continue
        results.append((request_answer.date, response_answer.date))
    return sorted(results, key=lambda pair: pair[0])


def _get_cycle_time(instance: Instance) -> Tuple[int]:
    extra_time = _get_rejected_instance_cycletime(instance)
    # If predating instance has no duration it's pointless to calculate waiting periods
    if not extra_time:
        return 0, 0
    idle_time = _compute_total_idle_days(_retrieve_waiting_periods(instance))
    return extra_time, idle_time


def _rejected_instances(instance) -> List[Instance]:
    flat_list = []
    previous_rejected = _get_previously_rejected_instance(instance)
    while previous_rejected:
        flat_list.append(previous_rejected)
        previous_rejected = _get_previously_rejected_instance(previous_rejected)
    return flat_list


def compute_cycle_time(instance: Instance) -> Dict:
    master_data = MasterData(instance.case)
    cycle_start = master_data.paper_submit_date or master_data.submit_date
    decision_date = master_data.decision_date

    if not decision_date or not cycle_start or cycle_start.date() > decision_date:
        return {}

    cumulated_extra_time = (decision_date - cycle_start.date()).days

    cumulated_idle_time = _compute_total_idle_days(_retrieve_waiting_periods(instance))

    for inst in _rejected_instances(instance):
        extra_time, idle_time = _get_cycle_time(inst)
        cumulated_extra_time += extra_time
        cumulated_idle_time += idle_time

    return {
        "total-cycle-time": cumulated_extra_time,
        "net-cycle-time": cumulated_extra_time - cumulated_idle_time,
    }


def aggregate_cycle_times(instances: QuerySet) -> Dict:
    # Categorize by year and aggregate (AVG) instances's cycle times.
    return (
        instances.annotate(
            year=Subquery(
                Answer.objects.filter(
                    question_id="decision-date",
                    document__work_item__case__instance=OuterRef("pk"),
                )
                .exclude(
                    document__work_item__status=WorkItem.STATUS_CANCELED,
                )
                .values("date__year")[:1]
            )
        )
        .values("year")
        .annotate(
            avg_total_cycle_time=Cast(
                Avg(
                    Cast(
                        KeyTextTransform("total-cycle-time", "case__meta"),
                        output_field=IntegerField(),
                    )
                ),
                output_field=IntegerField(),
            ),
            avg_net_cycle_time=Cast(
                Avg(
                    Cast(
                        KeyTextTransform("net-cycle-time", "case__meta"),
                        output_field=IntegerField(),
                    )
                ),
                output_field=IntegerField(),
            ),
            count=Count("pk"),
        )
    )
