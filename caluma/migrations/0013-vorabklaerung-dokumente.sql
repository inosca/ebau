BEGIN TRANSACTION;

DELETE FROM form_formquestion WHERE id IN (
  'vorabklaerung-einfach.name-gesuchstellerin-vorabklaerung',
  'vorabklaerung-einfach.vorname-gesuchstellerin-vorabklaerung',
  'vorabklaerung-einfach.strasse-gesuchstellerin',
  'vorabklaerung-einfach.nummer-gesuchstellerin',
  'vorabklaerung-einfach.plz-gesuchstellerin',
  'vorabklaerung-einfach.ort-gesuchstellerin',
  'vorabklaerung-einfach.gemeinde',
  'vorabklaerung-einfach.karte-einfache-vorabklaerung',
  'vorabklaerung-einfach.lagekoordinaten-ost-einfache-vorabklaerung',
  'vorabklaerung-einfach.lagekoordinaten-nord-einfache-vorabklaerung',
  'vorabklaerung-einfach.parzellennummer',
  'vorabklaerung-einfach.liegenschaftsnummer',
  'vorabklaerung-einfach.be-gid',
  'vorabklaerung-einfach.gwr-egid',
  'vorabklaerung-einfach.e-grid-nr',
  'vorabklaerung-einfach.anfrage-zur-vorabklaerung',
  'vorabklaerung-einfach.formulardownload-pdf',
  'vorabklaerung-einfach.einreichen-button'
);

INSERT INTO migration_history (name) VALUES ('0013-vorabklaerung-dokumente');

COMMIT TRANSACTION;
