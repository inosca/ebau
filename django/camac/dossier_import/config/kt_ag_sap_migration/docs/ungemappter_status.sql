--- nicht gemappter Status
SELECT c.CITY                       AS gemeinde,
       g.GESUCH_ID,
       g.BTITEL                     AS dossier_titel,
       t.TXT30                      AS status_text,
       g.CRDAT                      AS creation_date,

       (SELECT STRING_AGG(v.ACTION, ', ' ORDER BY v.TSTAMPL)
        FROM ZEZS_VERFSTAND v
        WHERE v.MANDT = g.MANDT
          AND v.EXTERN_ID = g.GESUCH_ID
          AND v.ACTION IS NOT NULL) AS actions_chronologisch

FROM ZEBP_GESUCH g

         LEFT JOIN TJ30T t
                   ON t.MANDT = g.MANDT
                       AND t.ESTAT = g.ESTAT
                       AND t.STSMA = 'ZEBP'
                       AND t.SPRAS = 'D'

         LEFT JOIN ZEZS_CITY c
                   ON c.CITY_ID = g.GEMEINDE_ID

WHERE c.CITY IN (
                 'Aarburg', 'Arni (AG)', 'Aarau', 'Biberstein', 'Dietwil', 'Endingen', 'Freienwil', 'Fischbach-Göslikon',
                 'Hellikon',
                 'Lengnau (AG)', 'Meisterschwanden', 'Menziken', 'Mettauertal', 'Möhlin', 'Mülligen', 'Obermumpf',
                 'Oberwil-Lieli',
                 'Olsberg', 'Riniken', 'Suhr', 'Tägerig', 'Tegerfelden', 'Wallbach', 'Würenlingen', 'Zuzgen'
    )

-- Ausschluss: archiviert, zurückgezogen, abgeschrieben, storniert
  AND t.TXT30 NOT IN (
                      'Gesuch archiviert',
                      'Gesuch zurückgezogen',
                      'Gesuch abgeschrieben',
                      'Gesuch storniert'
    )

-- Ausschluss: Status "Verfügung erstellt"
  AND t.TXT30 <> 'Verfügung erstellt'

-- Ausschluss: Action "Materielle Prüfung abgeschlossen"
  AND NOT EXISTS (SELECT 1
                  FROM ZEZS_VERFSTAND v
                  WHERE v.MANDT = g.MANDT
                    AND v.EXTERN_ID = g.GESUCH_ID
                    AND v.ACTION = 'Materielle Prüfung abgeschlossen')

-- Ausschluss: Action "Materielle Prüfung gestartet"
  AND NOT EXISTS (SELECT 1
                  FROM ZEZS_VERFSTAND v
                  WHERE v.MANDT = g.MANDT
                    AND v.EXTERN_ID = g.GESUCH_ID
                    AND v.ACTION = 'Materielle Prüfung gestartet')

-- Ausschluss: Stellungnahmen bei bestimmten Stati
  AND NOT EXISTS (SELECT 1
                  FROM ZEZS_VERFSTAND v
                  WHERE v.MANDT = g.MANDT
                    AND v.EXTERN_ID = g.GESUCH_ID
                    AND v.ACTION IN (
                                     'Stellungnahmen eingefordert',
                                     'Stellungnahme akzeptiert',
                                     'Stellungnahme eingetroffen',
                                     'Stellungnahme abgelehnt'
                      )
                    AND t.TXT30 IN (
                                    'Gesuch in Bearbeitung',
                                    'Anfrage / Stellungnahme offen',
                                    'In öffentlicher Auflage'
                      ))

-- Ausschluss: Vorprüfung durchführen
  AND NOT EXISTS (SELECT 1
                  FROM ZEZS_VERFSTAND v
                  WHERE v.MANDT = g.MANDT
                    AND v.EXTERN_ID = g.GESUCH_ID
                    AND v.ACTION = 'Vorprüfung durchführen')

-- Ausschluss: Ergänzung / Überarbeitung (alle Varianten)
  AND NOT EXISTS (SELECT 1
                  FROM ZEZS_VERFSTAND v
                  WHERE v.MANDT = g.MANDT
                    AND v.EXTERN_ID = g.GESUCH_ID
                    AND v.ACTION IN (
                                     'Ergänzung / Überarbeitung eingefordert',
                                     'Ergänzung / Überarbeitung eingereicht',
                                     'Ergänzung / Überarbeitung vom Kanton eingefordert'
                      ))

-- Ausschluss: Eingang bestätigt
  AND NOT EXISTS (SELECT 1
                  FROM ZEZS_VERFSTAND v
                  WHERE v.MANDT = g.MANDT
                    AND v.EXTERN_ID = g.GESUCH_ID
                    AND v.ACTION = 'Eingangsbestätigung versandt')

-- Ausschluss: Gesuch übermittelt
  AND t.TXT30 <> 'Gesuch übermittelt'

-- Ausschluss: Gesuch in Erfassung
  AND t.TXT30 <> 'Gesuch in Erfassung'

-- temp. Ausschluss Aarau
  and c.CITY <> 'Aarau'

ORDER BY c.CITY, g.CRDAT;
