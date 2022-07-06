from django.db import migrations

TASK_SLUGS = [
    # Shared
    "circulation",
    "reopen-circulation",
    "skip-circulation",
    "start-circulation",
    "start-decision",
    # BE
    "activation",
    "check-activation",
    "init-circulation",
    # SZ
    "alter-statement",
    "check-statement",
    "check-statements",
    "revise-statement",
    "start-additional-circulation",
    "write-statement",
]
WORKFLOW_SLUGS = ["circulation"]
FORM_SLUGS = ["circulation"]


class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunSQL(
            sql=[
                (
                    "DELETE FROM caluma_workflow_case WHERE workflow_id = ANY(%s);",
                    [WORKFLOW_SLUGS],
                ),
                (
                    "DELETE FROM caluma_workflow_historicalcase WHERE workflow_id = ANY(%s);",
                    [WORKFLOW_SLUGS],
                ),
                (
                    "DELETE FROM caluma_workflow_workflow_start_tasks WHERE workflow_id = ANY(%s);",
                    [WORKFLOW_SLUGS],
                ),
                (
                    "DELETE FROM caluma_workflow_workflow_allow_forms WHERE workflow_id = ANY(%s);",
                    [WORKFLOW_SLUGS],
                ),
                (
                    "DELETE FROM caluma_workflow_workflow WHERE slug = ANY(%s);",
                    [WORKFLOW_SLUGS],
                ),
                (
                    "UPDATE caluma_workflow_workitem SET previous_work_item_id = NULL WHERE previous_work_item_id IN (SELECT id FROM caluma_workflow_workitem WHERE task_id = ANY(%s));",
                    [TASK_SLUGS],
                ),
                (
                    "DELETE FROM caluma_workflow_workitem WHERE task_id = ANY(%s);",
                    [TASK_SLUGS],
                ),
                (
                    "DELETE FROM caluma_workflow_historicalworkitem WHERE task_id = ANY(%s);",
                    [TASK_SLUGS],
                ),
                (
                    "DELETE FROM caluma_workflow_task WHERE slug = ANY(%s);",
                    [TASK_SLUGS],
                ),
                (
                    "DELETE FROM caluma_workflow_flow WHERE id IN (SELECT flow_id FROM caluma_workflow_taskflow WHERE task_id = ANY(%s));",
                    [TASK_SLUGS],
                ),
                (
                    "DELETE FROM caluma_workflow_taskflow WHERE task_id = ANY(%s);",
                    [TASK_SLUGS],
                ),
                (
                    "DELETE FROM caluma_form_document WHERE form_id = ANY(%s);",
                    [FORM_SLUGS],
                ),
                (
                    "DELETE FROM caluma_form_historicaldocument WHERE form_id = ANY(%s);",
                    [FORM_SLUGS],
                ),
                (
                    "DELETE FROM caluma_form_form WHERE slug = ANY(%s);",
                    [FORM_SLUGS],
                ),
            ],
            reverse_sql=migrations.RunSQL.noop,
        )
    ]
