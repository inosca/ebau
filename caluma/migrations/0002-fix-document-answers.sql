UPDATE
  form_answer
SET
  value = to_jsonb(string_to_array(trim(both '"' from value::text), ''))
WHERE
  question_id LIKE '%-dokument'
  AND
  jsonb_typeof(value) = 'string';
