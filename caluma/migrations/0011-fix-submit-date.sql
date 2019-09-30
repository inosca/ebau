UPDATE
  form_document
SET
  meta = jsonb_set(
    d.meta,
    '{submit-date}',
    to_jsonb(to_char(hd.history_date, 'YYYY-MM-DD"T"HH24:MI:SS'))),
    TRUE
  )
FROM
  form_document d
  INNER JOIN form_historicaldocument hd
  ON d.id = hd.id
  AND hd.meta->>'submit-date' IS NOT NULL
  AND hd.meta->>'ebau-number' IS NULL
WHERE (d.meta->>'submit-date') ~ '^(\d{4})-(\d{2})-(\d{2})T00:00:00$';

UPDATE
  form_historicaldocument
SET
  meta = jsonb_set(
    hd.meta,
    '{submit-date}',
    d.meta->>'submit-date',
    TRUE
  )
FROM
  form_historicaldocument hd
  INNER JOIN form_document d
  ON hd.id = d.id
  AND hd.meta->>'submit-date' IS NOT NULL;

INSERT INTO migration_history (name) VALUES ('0011-fix-submit-date');
