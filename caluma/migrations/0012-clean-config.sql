BEGIN TRANSACTION;

DELETE FROM form_formquestion
WHERE id IN (
  'baugesuch-generell.selbstdeklaration-1',
  'baugesuch-generell.selbstdeklaration-2',
  'baugesuch-mit-uvp.selbstdeklaration-1',
  'baugesuch-mit-uvp.selbstdeklaration-2',
  'baugesuch.selbstdeklaration-1',
  'baugesuch.selbstdeklaration-2',
  'vorabklaerung-vollstaendig.selbstdeklaration-1',
  'vorabklaerung-vollstaendig.selbstdeklaration-2',
  'waermepumpen.waermepumpen-titel',
  'dokumente-sb2.andere-dokument'
);

DELETE FROM form_questionoption
WHERE id IN (
  'juristische-person-personalien.juristische-person-personalien-ja',
  'juristische-person-personalien.juristische-person-personalien-nein'
);

DELETE FROM form_option
WHERE slug IN (
  'juristische-person-personalien-ja',
  'juristische-person-personalien-nein'
);

DELETE FROM form_question
WHERE slug = 'juristische-person-personalien';

INSERT INTO migration_history (name) VALUES ('0011-clean-config');

COMMIT TRANSACTION;
