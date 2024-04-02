from functools import wraps
from typing import Callable

from caluma.caluma_workflow.models import Case
from django.conf import settings
from django.db.models import CharField, IntegerField
from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import Cast, Substr
from django.utils import timezone

from camac.core.models import HistoryActionConfig
from camac.core.translations import get_translations
from camac.user.models import User


def generate_sort_key(special_id: str) -> int:
    year, number = special_id.split("-")[-2:]
    # up to 1 million cases a year before it rolls over and causes issues
    return int(year) * 1_000_000 + int(number)


def generate_special_id(special_id_key: str, instance, year: int) -> str:
    max_increment = (
        Case.objects.exclude(pk=instance.case_id if instance else None)
        .filter(**{f"meta__{special_id_key}__startswith": year})
        .annotate(
            # TODO this can be switched to use dossier-number-sort, after everyone has migrated
            # 2020-1234 -> 1234
            increment=Cast(
                Substr(Cast(KeyTextTransform(special_id_key, "meta"), CharField()), 6),
                IntegerField(),
            )
        )
        .order_by("-increment")
        .values_list("increment", flat=True)
        .first()
    ) or 0

    return f"{year}-{max_increment + 1}"


def generate_ebau_nr(instance, year: int) -> str:
    """Generate the next eBau number (Kt. BE)."""
    return generate_special_id("ebau-number", instance, year)


def generate_dossier_nr(instance, year: int) -> str:
    """Generate the next Dossier number (Kt. GR, SO)."""
    return generate_special_id("dossier-number", instance, year)


def assign_ebau_nr(instance, year=None) -> str:
    # TODO: seems to be unnecessary, from an old migration
    existing = instance.case.meta.get("ebau-number")
    if existing:
        return existing

    year = timezone.now().year if year is None else year

    ebau_nr = generate_ebau_nr(instance, year)

    instance.case.meta["ebau-number"] = ebau_nr
    instance.case.save()

    return ebau_nr


def create_history_entry(
    instance,
    user: User,
    text: str,
    text_data: Callable[[str], dict] = lambda language: {},
    history_type: str = HistoryActionConfig.HISTORY_TYPE_STATUS,
    body: str = "",
) -> None:
    # avoid circular import
    from camac.instance.models import HistoryEntry, HistoryEntryT

    """
    Create a multilingual history entry for an instance.

    The parameters `instance`, `user` and `text` are required. Optionally it
    accepts a function `text_data` that takes the language as parameter and
    should return a dictionary of data that will be formatted into the text.
    Also, the `history_type` can be passed if it's anything other than a
    status change.

    >>> create_history_entry(
    ...     instance,
    ...     user,
    ...     gettext_noop("Your text"),
    ...     text_data_function,
    ...     history_type
    ... )
    """

    data = {}
    if not settings.APPLICATION.get("IS_MULTILINGUAL", False):
        data = {"title": text, "body": body}

    history = HistoryEntry.objects.create(
        instance=instance,
        created_at=timezone.now(),
        user=user,
        history_type=history_type,
        **data,
    )

    for language, text in get_translations(text).items():
        HistoryEntryT.objects.create(
            history_entry=history,
            title=text % text_data(language),
            body=body,
            language=language,
        )


def canton_aware(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        canton = settings.APPLICATION["SHORT_NAME"]
        func_name = f"{func.__name__}_{canton}"
        if hasattr(self, func_name):
            return getattr(self, func_name)(*args, **kwargs)

        return func(self, *args, **kwargs)

    return wrapper
