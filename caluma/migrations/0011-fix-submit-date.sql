BEGIN TRANSACTION;

UPDATE form_document
SET
  meta = jsonb_set(
    form_document.meta,
    '{submit-date}',
    to_jsonb(to_char(form_historicaldocument.history_date, 'YYYY-MM-DD"T"HH24:MI:SS')),
    TRUE
  )
FROM form_historicaldocument
WHERE
  form_document.id = form_historicaldocument.id
  AND
  form_document.meta->>'submit-date' ~ '^(\d{4})-(\d{2})-(\d{2})T00:00:00$'
  AND
  form_document.meta->>'migrated_from_old_camac' IS NULL
  AND
  form_historicaldocument.meta->>'submit-date' IS NOT NULL
  AND
  form_historicaldocument.meta->>'ebau-number' IS NULL;

UPDATE form_historicaldocument
SET
   meta = jsonb_set(
     form_historicaldocument.meta,
     '{submit-date}',
     to_jsonb(form_document.meta->>'submit-date'::varchar),
     TRUE
   )
FROM form_document
WHERE
  form_historicaldocument.id = form_document.id
  AND
  form_historicaldocument.meta->>'submit-date' IS NOT NULL;

INSERT INTO migration_history (name) VALUES ('0011-fix-submit-date');

COMMIT TRANSACTION;
