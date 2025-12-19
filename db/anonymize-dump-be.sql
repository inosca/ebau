BEGIN;

CREATE EXTENSION anon;
SELECT anon.init();

UPDATE caluma_form_answer
SET value = CASE
    -- Personalien: E-Mail, Name juristische Person, Name, Vorname, Telefon, Strasse, Nummer, PLZ, Ort
    WHEN question_id LIKE '%mail%'   THEN to_jsonb(anon.dummy_free_email())
    WHEN question_id LIKE 'name%'    THEN to_jsonb(anon.dummy_last_name())
    WHEN question_id LIKE 'vorname%' THEN to_jsonb(anon.dummy_first_name())
    WHEN question_id LIKE 'telefon%' THEN to_jsonb(anon.random_phone())
    WHEN question_id LIKE 'strasse%' THEN to_jsonb(anon.dummy_street_name())
    WHEN question_id LIKE 'nummer%'  THEN to_jsonb(anon.random_int_between(1, 200))
    WHEN question_id LIKE 'plz%'     THEN to_jsonb(anon.random_int_between(1000, 9999))
    WHEN question_id LIKE 'ort%'     THEN to_jsonb(anon.dummy_city_name())

    -- Kontaktperson Vorabklärungen
    WHEN question_id = 'kontaktperson-vorabklaerungen' THEN to_jsonb(anon.dummy_name())
    WHEN question_id = 'kontaktperson-name-energie'    THEN to_jsonb(anon.dummy_last_name())
    WHEN question_id = 'kontaktperson-vorname-energie' THEN to_jsonb(anon.dummy_first_name())

    -- Lokalisierung: Strasse (via strasse%), Nr, Ort (via ort%), Parzellen-, Liegenschafts-, Baurechts- & E-GRID-Nr, Koordinaten
    WHEN question_id = 'nr'                      THEN to_jsonb(anon.random_int_between(1, 200))
    WHEN question_id LIKE 'parzellennummer%'     THEN to_jsonb(anon.random_int_between(1, 9999))
    WHEN question_id LIKE 'liegenschaftsnummer%' THEN to_jsonb(anon.random_int_between(1, 9999))
    WHEN question_id LIKE 'baurecht-nummer%'     THEN to_jsonb(anon.random_int_between(1, 9999))
    WHEN question_id = 'e-grid-nr'               THEN to_jsonb(concat('CH', anon.random_bigint_between(1, 999999999999)::text))
    WHEN question_id = 'lagekoordinaten-nord'    THEN to_jsonb(anon.random_int_between(1070000, 1300000))
    WHEN question_id = 'lagekoordinaten-ost'     THEN to_jsonb(anon.random_int_between(2480000, 2840000))

    -- Baubeschrieb
    WHEN question_id IN ('beschreibung-bauvorhaben', 'bab-bauvorhaben', 'beschreibung-projektaenderung')
        THEN to_jsonb(
            anon.lorem_ipsum(characters := anon.length(value::text))
        )

    -- diverse Textfelder
    WHEN question_id IN (
        'bisherige-nutzung',
        'zusaetze-zu-amts-fachstellen',
        'begruendung-des-befreiungsgesuches',
        'weitere-vorhaben',
        'beschreibung-der-gefaehrdung'
    )
        THEN to_jsonb(
            anon.lorem_ipsum(characters := anon.length(value::text))
        )

    -- sämtliche "Bermerkungs-Felder" (Gesuchsformular, formelle & materielle Prüfung)
    WHEN question_id LIKE '%bemerkung%'
        THEN to_jsonb(
            anon.lorem_ipsum(characters := anon.length(value::text))
        )

    -- formelle & materielle Prüfung: diverse Textfelder
    WHEN question_id IN (
        'fp-offenkundige-materielle-maengel',
        'mp-welche-beilagen-fehlen'
    )
        THEN to_jsonb(
            anon.lorem_ipsum(characters := anon.length(value::text))
        )

    -- Nachforderungen: Bermerkung, Beschreibung
    WHEN question_id IN (
        'nfd-tabelle-bemerkung',
        'nfd-tabelle-beschreibung'
    )
        THEN to_jsonb(
            anon.lorem_ipsum(characters := anon.length(value::text))
        )

    -- Rechtsbegehren: Titel, Rügepunkte
    WHEN question_id IN (
        'legal-submission-title',
        'legal-submission-reprimands'
    )
        THEN to_jsonb(
            anon.lorem_ipsum(characters := anon.length(value::text))
        )

    -- Publikation: Text
    WHEN question_id = 'publikation-text'
        THEN to_jsonb(
            anon.lorem_ipsum(characters := anon.length(value::text))
        )

    -- Zirkulation: Bemerkungen, Stellungnahme, Nebenbestimmungen
    WHEN question_id IN (
        'inquiry-remark',
        'inquiry-answer-statement',
        'inquiry-answer-ancillary-clauses'
    )
        THEN to_jsonb(
            anon.lorem_ipsum(characters := anon.length(value::text))
        )

    -- Entscheid: Bemerkungen
    WHEN question_id = 'decision-remarks'
        THEN to_jsonb(
            anon.lorem_ipsum(characters := anon.length(value::text))
        )

    -- default: leave unchanged
    ELSE value
END
WHERE
       question_id LIKE '%mail%'
    OR question_id LIKE 'name%'
    OR question_id LIKE 'vorname%'
    OR question_id LIKE 'telefon%'
    OR question_id LIKE 'strasse%'
    OR question_id LIKE 'nummer%'
    OR question_id LIKE 'plz%'
    OR question_id LIKE 'ort%'

    OR question_id IN (
        'kontaktperson-vorabklaerungen',
        'kontaktperson-name-energie',
        'kontaktperson-vorname-energie',
        'nr',
        'e-grid-nr',
        'lagekoordinaten-nord',
        'lagekoordinaten-ost',
        'beschreibung-bauvorhaben',
        'bab-bauvorhaben',
        'beschreibung-projektaenderung',
        'bisherige-nutzung',
        'zusaetze-zu-amts-fachstellen',
        'begruendung-des-befreiungsgesuches',
        'weitere-vorhaben',
        'beschreibung-der-gefaehrdung',
        'fp-offenkundige-materielle-maengel',
        'mp-welche-beilagen-fehlen',
        'nfd-tabelle-bemerkung',
        'nfd-tabelle-beschreibung',
        'legal-submission-title',
        'legal-submission-reprimands',
        'publikation-text',
        'inquiry-remark',
        'inquiry-answer-statement',
        'inquiry-answer-ancillary-clauses',
        'decision-remarks'
    )
    OR question_id LIKE '%bemerkung%';

-- Manuelle Aufgaben: Titel, Beschreibung
update caluma_workflow_workitem set name=hstore('de', anon.lorem_ipsum( characters := anon.length(caluma_workflow_workitem.name -> 'de'))) where task_id = 'create-manual-workitems' and deadline is not null;
update caluma_workflow_workitem set description=hstore('de', anon.lorem_ipsum( characters := anon.length(caluma_workflow_workitem.description -> 'de'))) where task_id = 'create-manual-workitems' and deadline is not null;

-- Benutzer: Name, Vorname, E-Mail, Telefon (importiert aus BE-Login / AGOV)
SECURITY LABEL FOR anon ON COLUMN "USER"."NAME" IS 'MASKED WITH FUNCTION anon.dummy_first_name()';
SECURITY LABEL FOR anon ON COLUMN "USER"."SURNAME" IS 'MASKED WITH FUNCTION anon.dummy_last_name()';
SECURITY LABEL FOR anon ON COLUMN "USER"."EMAIL" IS 'MASKED WITH FUNCTION anon.dummy_free_email()';
SECURITY LABEL FOR anon ON COLUMN "USER"."PHONE" IS 'MASKED WITH FUNCTION anon.random_phone()';

-- Organisationen: E-Mail, Telefon
SECURITY LABEL FOR anon ON COLUMN "SERVICE"."PHONE" IS 'MASKED WITH FUNCTION anon.random_phone()';
SECURITY LABEL FOR anon ON COLUMN "SERVICE"."EMAIL" IS 'MASKED WITH FUNCTION anon.dummy_free_email()';

-- Dossiers: Rückweisungstext
SECURITY LABEL FOR anon ON COLUMN "INSTANCE".rejection_feedback IS
  'MASKED WITH FUNCTION anon.ternary(rejection_feedback is NULL, NULL, anon.lorem_ipsum(characters := anon.length("INSTANCE".rejection_feedback)))';

-- Berechtigungen / Einladungen auf Dossiers: E-Mail
SECURITY LABEL FOR anon ON COLUMN "APPLICANTS".email IS 'MASKED WITH FUNCTION anon.dummy_free_email()';

-- Dokumente: Dateiname, Pfad, Anzeigename
SECURITY LABEL FOR anon ON COLUMN "ATTACHMENT"."NAME" IS 'MASKED WITH FUNCTION anon.dummy_file_name()';
SECURITY LABEL FOR anon ON COLUMN "ATTACHMENT"."PATH" IS 'MASKED WITH FUNCTION anon.dummy_file_path()';
UPDATE "ATTACHMENT" SET context = jsonb_set(context, '{displayName}', to_jsonb(anon.dummy_file_name()), false) WHERE context ? 'displayName';

-- Journal: Text
SECURITY LABEL FOR anon ON COLUMN instance_journalentry.text IS 'MASKED WITH FUNCTION anon.lorem_ipsum(characters := anon.length(instance_journalentry.text))';

-- Gebühren: Text
SECURITY LABEL FOR anon ON COLUMN billing_billingv2entry.text IS 'MASKED WITH FUNCTION anon.lorem_ipsum(characters := anon.length(billing_billingv2entry.text))';

-- Kommunikationsmodul: Thema
SECURITY LABEL FOR anon ON COLUMN communications_communicationstopic.subject IS 'MASKED WITH FUNCTION anon.lorem_ipsum(characters := anon.length(communications_communicationstopic.subject))';
SECURITY LABEL FOR anon ON COLUMN communications_communicationsmessage.body IS 'MASKED WITH FUNCTION anon.lorem_ipsum(characters := anon.length(communications_communicationsmessage.body))';

-- Stichworte
SECURITY LABEL FOR anon ON COLUMN "TAGS"."NAME" IS 'MASKED WITH FUNCTION anon.lorem_ipsum(characters := anon.length("TAGS"."NAME"))';

-- Anonymize labelled data
SELECT anon.anonymize_database();

-- Reset
SELECT anon.remove_masks_for_all_columns();
SELECT anon.remove_masks_for_all_roles();
DROP EXTENSION anon;

COMMIT;
