# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_auto_20191004_1552'),
    ]

    """NOTE: Migration 0037_fix_project_submitter_view introduced a fallback mechansim where if an
    instance has no answer to question 257 we will fallback to the APPLICANT_DATA_VIEW.

    This was done so we can reuse the same view to get the required email to send the building
    permit per email and through the portal.

    Turns out the original behaviour was a feature not a bug. This view should only return the email
    address if the instance was submitted through the portal. This view is used for many different
    existing mail actions (e.g. when circulation finishes). With the new behavior to many emails are
    sent to people that did not submit their Dossier through the portal but are referenced as
    applicant in the form.

    This change should revert the view back to the original behavior.
    """
    operations = [
        migrations.RunSQL("""

DROP VIEW IF EXISTS "PROJECT_SUBMITTER_DATA";
DROP VIEW IF EXISTS "PROJECT_SUBMITTER_VIEW";

CREATE OR REPLACE VIEW "PROJECT_SUBMITTER_VIEW" AS
SELECT
    "ANSWER",
    "INSTANCE_ID"
FROM
    "ANSWER" "NAME_TBL"
WHERE
        "NAME_TBL"."CHAPTER_ID" = 103
    AND
        "NAME_TBL"."QUESTION_ID" = 257
    AND
        "NAME_TBL"."ITEM" = 1
;

-- This view was not touched, but needed to be recreated because it depends on PROJECT_SUBMITTER_VIEW
CREATE OR REPLACE VIEW "PROJECT_SUBMITTER_DATA" AS
SELECT
    CASE
        "PROJECT_SUBMITTER_VIEW"."ANSWER"
        WHEN '0' THEN "APPLICANT_DATA_VIEW"."NAME"
        WHEN '1' THEN "PROJECT_AUTHOR_DATA_VIEW"."NAME"
    END "NAME",
    CASE
        "PROJECT_SUBMITTER_VIEW"."ANSWER"
        WHEN '0' THEN "APPLICANT_DATA_VIEW"."EMAIL"
        WHEN '1' THEN "PROJECT_AUTHOR_DATA_VIEW"."EMAIL"
    END "EMAIL",
    "PROJECT_SUBMITTER_VIEW"."INSTANCE_ID",
    "PROJECT_SUBMITTER_VIEW"."ANSWER"
FROM
    "PROJECT_SUBMITTER_VIEW"
LEFT JOIN
    "APPLICANT_DATA_VIEW" ON
    "PROJECT_SUBMITTER_VIEW"."INSTANCE_ID" = "APPLICANT_DATA_VIEW"."INSTANCE_ID"
LEFT JOIN
    "PROJECT_AUTHOR_DATA_VIEW" ON
    "PROJECT_SUBMITTER_VIEW"."INSTANCE_ID"= "PROJECT_AUTHOR_DATA_VIEW"."INSTANCE_ID"
;
        """)
    ]
