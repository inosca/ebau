from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Callable

from caluma.caluma_workflow.models import Case
from django.conf import settings
from django.db.models import CharField, IntegerField, Value
from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import Cast, Replace
from django.utils import timezone

from camac.core.models import HistoryActionConfig
from camac.core.translations import get_translations

if TYPE_CHECKING:  # pragma: no cover
    from camac.instance.models import Instance
    from camac.user.models import User


def generate_sort_key(special_id: str) -> int:
    """Generate a sortable integer key from a dossier number.

    This function splits the dossier number (which can have different formats)
    by dashes and concatenates all integer parts to a number. However, the last
    part is always the index - in order to provide reliable sorting, that index
    is being zero padded to six digits before being concatenated to the rest.

    A few examples:

    - BE / GR ([YYYY]-[N]): 2023-1 => 2023000001
    - SO ([BfS]-[YYYY]-[N]): 2601-2023-1 => 26012023000001
    """

    parts = [part for part in special_id.split("-") if part.isdigit()]
    index = parts.pop()

    # up to 1 million cases a year before it rolls over and causes issues
    return int("".join([*parts, index.zfill(6)]))


def generate_special_id(special_id_key: str, instance, prefix: str) -> str:
    max_increment = (
        Case.objects.exclude(pk=instance.case_id if instance else None)
        .filter(**{f"meta__{special_id_key}__startswith": prefix})
        .annotate(
            increment=Cast(
                Replace(
                    Cast(KeyTextTransform(special_id_key, "meta"), CharField()),
                    Value(prefix),
                    Value(""),
                ),
                IntegerField(),
            )
        )
        .order_by("-increment")
        .values_list("increment", flat=True)
        .first()
    ) or 0

    return f"{prefix}{max_increment + 1}"


def generate_ebau_nr(instance, year: int) -> str:
    """Generate the next eBau number (Kt. BE)."""
    return generate_special_id("ebau-number", instance, f"{year}-")


def generate_dossier_nr(instance, year: int) -> str:
    """Generate the next Dossier number (Kt. GR)."""
    return generate_special_id("dossier-number", instance, f"{year}-")


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
    instance: Instance,
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
