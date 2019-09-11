UPDATE
  form_document
SET
  meta = jsonb_set(
    meta,
    '{submit-date}',
    to_jsonb(concat(meta->>'submit-date'::varchar, 'T00:00:00')),
    TRUE
  )
WHERE
  (meta->>'submit-date') ~ '^(\d{4})-(\d{2})-(\d{2})$';

INSERT INTO migration_history (name) VALUES ('0010-migrate-submit-date-to-datetime');
