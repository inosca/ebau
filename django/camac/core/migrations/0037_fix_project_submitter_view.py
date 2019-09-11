# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_auto_20190904_1040'),
    ]

    """
    NOTE: The problem with the old PROJECT_SUBMITTER_VIEW was that it did not respect instances that
    were not submitted through the portal. Instances which are created in Camac don't have an answer
    to question 257 and therefore don't show up in the view.

    Now if there is no answer to question 257 we will fallback to the APPLICANT_DATA_VIEW.
    """
    operations = [
        migrations.RunSQL("""
DROP VIEW IF EXISTS "PROJECT_SUBMITTER_DATA";
DROP VIEW IF EXISTS "PROJECT_SUBMITTER_VIEW";
CREATE VIEW "PROJECT_SUBMITTER_VIEW" AS
SELECT
        "INSTANCE"."INSTANCE_ID",
        COALESCE("ANSWER", '0') AS "ANSWER"
FROM "INSTANCE"
LEFT JOIN "ANSWER" "NAME_TBL"
        ON "NAME_TBL"."CHAPTER_ID" = 103
        AND "NAME_TBL"."QUESTION_ID" = 257
        AND "NAME_TBL"."ITEM" = 1
        AND "INSTANCE"."INSTANCE_ID" = "NAME_TBL"."INSTANCE_ID";

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
