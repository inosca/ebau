from typing import Callable

from django.db.models import IntegerField
from django.db.models.functions import Cast, Substr
from django.utils import timezone

from camac.constants.kt_bern import CHAPTER_EBAU_NR, QUESTION_EBAU_NR
from camac.core.models import HistoryActionConfig
from camac.core.translations import get_translations
from camac.instance.models import HistoryEntry, HistoryEntryT, Instance
from camac.user.models import User

from .models import Answer


def get_max_ebau_nr(year: int) -> int:
    ebau_answer = (
        Answer.objects.filter(
            question_id=QUESTION_EBAU_NR,
            chapter_id=CHAPTER_EBAU_NR,
            answer__startswith=year,
        )
        # Substr is 1-index, so start after "YYYY-"
        .annotate(seq=Cast(Substr("answer", 6), output_field=IntegerField()))
        .order_by("-seq")
        .first()
    )
    return ebau_answer.seq if ebau_answer is not None else 0


def generate_ebau_nr(year: int) -> str:
    return "%d-%d" % (year, get_max_ebau_nr(year) + 1)


def assign_ebau_nr(instance: Instance, year=None) -> str:
    year = timezone.now().year if year is None else year

    ebau_nr = generate_ebau_nr(year)

    ans, _ = save_ebau_nr_answer(instance, ebau_nr)
    return ans.answer


def save_ebau_nr_answer(instance: Instance, ebau_nr: str):
    return Answer.objects.get_or_create(
        instance=instance,
        question_id=QUESTION_EBAU_NR,
        chapter_id=CHAPTER_EBAU_NR,
        # TODO check if this used somewhere
        item=1,
        defaults={"answer": ebau_nr},
    )


def create_history_entry(
    instance: Instance,
    user: User,
    text: str,
    text_data: Callable[[str], dict] = lambda language: {},
    history_type: str = HistoryActionConfig.HISTORY_TYPE_STATUS,
) -> None:
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

    history = HistoryEntry.objects.create(
        instance=instance,
        created_at=timezone.now(),
        user=user,
        history_type=history_type,
    )

    for (language, text) in get_translations(text):
        HistoryEntryT.objects.create(
            history_entry=history, title=text % text_data(language), language=language
        )
