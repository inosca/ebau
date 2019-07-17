UPDATE
    workflow_case
SET
    meta = jsonb_set(
        meta,
        '{submit-date}',
        to_jsonb(regexp_replace((meta ->> 'submit-date')::varchar, '^(\d+)\.(\d+)\.(\d+)', '\3-\2-\1')),
        TRUE
    )
WHERE
    (meta ->> 'submit-date')::varchar ~ '^\d{2}\.\d{2}\.\d{4}$';
