/**
 * This SQL script is a fast way to clean up any instance-related data.
 * This is often needed to clean up a system of any test data - without
 * removing users, group memberships etc. (e.g. before going into production)
 **/

BEGIN;

-- eBau
DELETE FROM "APPLICANTS";
DELETE FROM "INSTANCE_SERVICE";
DELETE FROM "INSTANCE";
DELETE FROM "RESPONSIBLE_SERVICE";
DELETE FROM billing_billingv2entry;
DELETE FROM communications_communicationsattachment;
DELETE FROM communications_communicationsmessage;
DELETE FROM communications_communicationsreadmarker;
DELETE FROM communications_communicationstopic;
DELETE FROM django_q_task;
DELETE FROM deadlines_suspension;
DELETE FROM deadlines_instancedeadline;
DELETE FROM dossier_import_dossierimport;
DELETE FROM dossier_import_migration_document_status;
DELETE FROM ech0211_message;
DELETE FROM gis_export_aggisexport;
DELETE FROM instance_historyentry;
DELETE FROM instance_historyentryt;
DELETE FROM instance_instancealexandriadocument;
DELETE FROM instance_instancegroup;
DELETE FROM instance_journalentry;
DELETE FROM linker_gwrlink;
DELETE FROM manabi_lock;
DELETE FROM permissions_instanceacl;
DELETE FROM reversion_revision;
DELETE FROM reversion_version;
DELETE FROM tags_keyword_instances;
DELETE FROM tags_keyword;

-- Caluma
DELETE FROM caluma_form_answerdocument;
DELETE FROM caluma_form_answer WHERE document_id IS NOT NULL;
DELETE FROM caluma_form_document;
DELETE FROM caluma_form_dynamicoption;
DELETE FROM caluma_workflow_case;
DELETE FROM caluma_workflow_workitem;

-- Alexandria
DELETE FROM alexandria_core_file;
DELETE FROM alexandria_core_document;
DELETE FROM alexandria_core_tag;
DELETE FROM alexandria_core_document_tags;
DELETE FROM alexandria_core_document_marks;

-- History
DELETE FROM caluma_form_historicalanswer;
DELETE FROM caluma_form_historicalanswerdocument;
DELETE FROM caluma_form_historicaldocument;
DELETE FROM caluma_form_historicaldynamicoption;
DELETE FROM caluma_form_historicalform;
DELETE FROM caluma_form_historicalformquestion;
DELETE FROM caluma_form_historicaloption;
DELETE FROM caluma_form_historicalquestion;
DELETE FROM caluma_form_historicalquestionoption;
DELETE FROM caluma_workflow_historicalcase;
DELETE FROM caluma_workflow_historicalflow;
DELETE FROM caluma_workflow_historicaltaskflow;
DELETE FROM caluma_workflow_historicalworkitem;
DELETE FROM dossier_import_historicaldossierimport;

-- Reset INSTANCE_ID sequence
SELECT setval(pg_get_serial_sequence('"INSTANCE"','INSTANCE_ID'), coalesce(max("INSTANCE_ID"), 1), max("INSTANCE_ID") IS NOT null) FROM "INSTANCE";

COMMIT;

VACUUM;

SELECT
    n.nspname   AS schema,
  p.relname   AS table,
  p.reltuples AS count
FROM
    pg_class AS p
    INNER JOIN
    pg_namespace AS n ON n.oid = p.relnamespace
WHERE
    n.nspname NOT IN ('pg_catalog', 'information_schema') AND
    p.relkind='r' AND
    p.reltuples > 0 AND
    n.nspname = 'public'
order by p.reltuples asc;
