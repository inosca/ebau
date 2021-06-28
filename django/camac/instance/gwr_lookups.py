from django.conf import settings

from camac.core.models import WorkflowEntry
from camac.user.models import Location


def get_answer_value(key, queryset):
    answer_slugs = settings.APPLICATION["GWR"].get("ANSWER_SLUGS", {})
    if not answer_slugs.get(key, None):
        return None
    value = queryset.filter(question__slug=answer_slugs.get(key)).first().value
    if isinstance(value, list):
        return value[0]
    return value


def get_answer_value_from_list(key, queryset):
    answer_slugs = settings.APPLICATION["GWR"].get("ANSWER_SLUGS", {})
    if not answer_slugs.get(key):
        return None
    return queryset.filter(question__slug__in=answer_slugs.get(key, "")).first().value


def get_mapped_answer_value(key, queryset):
    value = get_answer_value(key, queryset)
    if not value:
        return None
    return settings.APPLICATION["GWR"].get("ANSWER_MAPPING", {}).get(value, None)


def get_municipality_answer_value(key, queryset):
    value = get_answer_value(key, queryset)
    if not value:
        return None
    return Location.objects.get(pk=value).name


def get_dossier_number(case):
    if case.meta.get("dossier-number", None):
        return case.meta["dossier-number"]


def get_submit_date(pk, case, answer_slugs):
    submit_date = settings.APPLICATION["GWR"].get("SUBMIT_DATE", {})
    if submit_date.get("TASK"):
        return case.work_items.get(task_id=submit_date["TASK"]).closed_at
    elif submit_date.get("WORKFLOW_ENTRY"):
        return WorkflowEntry.objects.get(
            instance_id=int(pk), workflow_item_id__in=submit_date["WORKFLOW_ENTRY"]
        ).workflow_date.strftime("%Y-%m-%d")
