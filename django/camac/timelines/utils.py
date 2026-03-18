def is_additional_demand_with_changes(work_item) -> bool:
    from django.conf import settings

    send_work_item = (
        work_item.case.work_items.filter(
            task_id=settings.ADDITIONAL_DEMAND["SEND_TASK"],
        ).first()
        if not work_item.task_id == settings.ADDITIONAL_DEMAND["SEND_TASK"]
        else work_item
    )

    allow_changes_answer = send_work_item.document.answers.filter(
        question_id="additional-demand-allow-changes"
    ).first()

    return allow_changes_answer and "additional-demand-allow-changes" in (
        allow_changes_answer.value
    )
