-- Change the question "company" to "organisation"


UPDATE "QUESTION"
SET "NAME" = 'Organisation'
WHERE "QUESTION_ID" IN (221, 222, 223);
