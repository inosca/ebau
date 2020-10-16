from django.db.models import IntegerField
from django.db.models.functions import Cast, Substr
from django.utils import timezone

from camac.constants.kt_bern import CHAPTER_EBAU_NR, QUESTION_EBAU_NR
from camac.instance.models import Instance

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

    ans, _ = Answer.objects.get_or_create(
        instance=instance,
        question_id=QUESTION_EBAU_NR,
        chapter_id=CHAPTER_EBAU_NR,
        # TODO check if this used somewhere
        item=1,
        defaults={"answer": ebau_nr},
    )

    return ans.answer
