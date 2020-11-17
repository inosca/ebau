import pytest

from camac.constants.kt_bern import CHAPTER_EBAU_NR, QUESTION_EBAU_NR
from camac.core import models, utils


@pytest.mark.freeze_time("2020-10-16")
@pytest.mark.parametrize(
    "question__question_id,chapter__chapter_id",
    [
        (QUESTION_EBAU_NR, CHAPTER_EBAU_NR),
    ],  # noqa: E231
)
def test_max_ebau_nr(db, instance_factory, camac_answer_factory, question, chapter):
    # no answer
    assert utils.generate_ebau_nr(2020) == "2020-1"

    # unrelated answer
    camac_answer_factory(instance=instance_factory(), answer="foo")

    assert utils.generate_ebau_nr(2020) == "2020-1"

    camac_answer_factory(
        instance=instance_factory(), question=question, chapter=chapter, answer="2020-1"
    )
    assert utils.generate_ebau_nr(2020) == "2020-2"

    camac_answer_factory(
        instance=instance_factory(),
        question=question,
        chapter=chapter,
        answer="2020-10",
    )
    assert utils.generate_ebau_nr(2020) == "2020-11"

    camac_answer_factory(
        instance=instance_factory(),
        question=question,
        chapter=chapter,
        answer="2020-10",
    )
    assert utils.generate_ebau_nr(2020) == "2020-11"

    camac_answer_factory(
        instance=instance_factory(),
        question=question,
        chapter=chapter,
        answer="2019-100",
    )
    assert utils.generate_ebau_nr(2019) == "2019-101"
    assert utils.generate_ebau_nr(2020) == "2020-11"

    camac_answer_factory(
        instance=instance_factory(),
        question=question,
        chapter=chapter,
        answer="2020-99",
    )
    assert utils.generate_ebau_nr(2020) == "2020-100"

    assert utils.generate_ebau_nr(2011) == "2011-1"


@pytest.mark.freeze_time("2020-10-16")
@pytest.mark.parametrize(
    "question__question_id,chapter__chapter_id",
    [
        (QUESTION_EBAU_NR, CHAPTER_EBAU_NR),
    ],  # noqa: E231
)
def test_assign_ebau_nr(db, camac_answer_factory, question, chapter, instance_factory):
    inst = instance_factory()
    ebau_nr = utils.assign_ebau_nr(inst)

    assert models.Answer.objects.filter(
        instance=inst, question=question, chapter=chapter
    ).exists()

    assert ebau_nr == "2020-1"

    # no double assignment
    assert utils.assign_ebau_nr(inst) == "2020-1"

    # no change of year
    assert utils.assign_ebau_nr(inst, 2019) == "2020-1"

    inst2 = instance_factory()
    assert utils.assign_ebau_nr(inst2, 2020) == "2020-2"

    inst3 = instance_factory()
    assert utils.assign_ebau_nr(inst3, 2019) == "2019-1"

    camac_answer_factory(
        instance=instance_factory(),
        question=question,
        chapter=chapter,
        answer="2017-420",
    )

    inst4 = instance_factory()
    assert utils.assign_ebau_nr(inst4, 2017) == "2017-421"
