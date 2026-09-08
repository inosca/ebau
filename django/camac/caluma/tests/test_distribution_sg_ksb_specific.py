import pytest
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Question
from caluma.caluma_workflow.api import resume_work_item

from camac.caluma.extensions.events.distribution_sg_ksb_specific import (
    META_FIRST_WEEK_KEY,
)


@pytest.mark.parametrize(
    ("inquiry_type", "expected_first_week"),
    [
        ("inquiry-type-first-week", True),
        ("inquiry-type-statement", False),
        (None, False),
    ],
)
@pytest.mark.django_db
def test_mark_inquiry_as_first_week(
    caluma_admin_user,
    expected_first_week,
    inquiry_factory_sg,
    inquiry_type,
    sg_distribution_settings,
):
    inquiry = inquiry_factory_sg()

    if inquiry_type:
        save_answer(
            question=Question.objects.get(
                pk=sg_distribution_settings["QUESTIONS"]["TYPE"]
            ),
            document=inquiry.document,
            user=caluma_admin_user,
            value=inquiry_type,
        )

    resume_work_item(work_item=inquiry, user=caluma_admin_user)
    inquiry.refresh_from_db()

    assert inquiry.meta.get(META_FIRST_WEEK_KEY, False) == expected_first_week
