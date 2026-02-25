-- all requests to be migrated
select count(*)
from ZEBP_GESUCH g
         left join ZEZS_CITY city on city.CITY_ID = g.GEMEINDE_ID
         left join TJ30T t on t.ESTAT = g.ESTAT and t.STSMA = 'ZEBP'
where city.CITY not in ('ZZ Testgemeinde', 'ZZ Testgemeinde MH 1')
  and t.TXT30 != 'Gesuch in Erfassung'
  and g.DIVERSES_KNZ != 'X' and g.VORABKL_KNZ != 'X';

select ZEBP_GESUCH.*, TJ30T.*, ZEZS_CITY.*
from ZEBP_GESUCH
         left join TJ30T on TJ30T.ESTAT = ZEBP_GESUCH.ESTAT and TJ30T.STSMA = 'ZEBP'
         left join ZEZS_CITY on ZEZS_CITY.CITY_ID = ZEBP_GESUCH.GEMEINDE_ID
WHERE
    ZEBP_GESUCH.GESUCH_ID in ('EBPA-0219-7779', 'EBPA-1010-5310', 'EBPA-1720-6526', 'EBPA-8318-3681', 'EBPA-0353-1598')

-- Standorte je Gesuch
select ZEBP_STORT.*, ZEZS_CITY.*
from ZEBP_STORT
         left join ZEZS_CITY on ZEBP_STORT.CITY_ID = ZEZS_CITY.CITY_ID
where ZEBP_STORT.GESUCH_ID = 'EBPA-8318-3681'

-- Parzellen je Gesuch
select ZEBP_PARZ.*, ZEZS_CITY.*
from ZEBP_PARZ
         left join ZEZS_CITY on ZEBP_PARZ.CITY_ID = ZEZS_CITY.CITY_ID
where ZEBP_PARZ.GESUCH_ID = 'EBPA-8318-3681'

-- Kontakte je Gesuch
select ZEBP_KONTAKT.*
from ZEBP_KONTAKT
where ZEBP_KONTAKT.GESUCH_ID = 'EBPA-5618-4193'

-- Fristen je Gesuch
select ZEZS_DATES.*
from ZEZS_DATES
where process_id = 'ZEBP'
  and ZEZS_DATES.EXTERN_ID = 'EBPA-1720-6526'

-- "GESART" = Art der Gesuchs
select ZEBP_GESART.*
from ZEBP_GESART
where ZEBP_GESART.GESUCH_ID = 'EBPA-8318-3681'

select ZEBP_GESART.GESART, count(*)
from ZEBP_GESART
         left join ZEBP_GESUCH on ZEBP_GESUCH.GESUCH_ID = ZEBP_GESART.GESUCH_ID
where ZEBP_GESUCH.GESUCH_ID is not null
group by ZEBP_GESART.GESART
order by ZEBP_GESART.GESART


-- "VERFSTAND" = Einträge für den Verfahrensstand je Gesuch
select ZEZS_VERFSTAND.*
from ZEZS_VERFSTAND
where ZEZS_VERFSTAND.PROCESS_ID = 'ZEBP'
  and ZEZS_VERFSTAND.EXTERN_ID = 'EBPA-7515-4925';


-- tests zum status - mapping

select ZEBP_GESUCH.VERFTYP, count(*)
from ZEBP_GESUCH
group by ZEBP_GESUCH.VERFTYP
order by ZEBP_GESUCH.VERFTYP

select ZEBP_GESUCH.GESUCH_ID, STRING_AGG(ZEBP_GESART.GESART, ', ')
from ZEBP_GESART
         left join ZEBP_GESART ges1 on ges1.GESUCH_ID = ZEBP_GESART.GESUCH_ID and ges1.GESART != ZEBP_GESART.GESART
         left join ZEBP_GESUCH
on ZEBP_GESART.GESUCH_ID = ZEBP_GESUCH.GESUCH_ID
where ZEBP_GESUCH.GESUCH_ID is not null
GROUP BY ZEBP_GESUCH.GESUCH_ID;

select ZEBP_KONTAKT.*
from ZEBP_KONTAKT
where ZEBP_KONTAKT.REF_NR like 'N%';

-- count gesuche
select ZEZS_CITY.CITY, count(*)
from ZEBP_GESUCH
         left join ZEZS_CITY on ZEZS_CITY.CITY_ID = ZEBP_GESUCH.GEMEINDE_ID
group by ZEZS_CITY.CITY
order by ZEZS_CITY.CITY

-- list eBau extended dossier ids that are not in eBau Aargau
SELECT r.GESUCH_ID
FROM ZEB2_A_REQUEST r
         LEFT JOIN ZEBP_GESUCH g ON r.GESUCH_ID = g.GESUCH_ID
WHERE g.GESUCH_ID IS NULL;

-- check for number of dossiers in certain state or verfstand
-- different actions
SELECT action, count (*) as number
FROM SAPABAP1.ZEZS_VERFSTAND
where process_id = 'ZEBP'
group by action
order by number desc;

-- different steps
SELECT step, count(*) as number
FROM SAPABAP1.ZEZS_VERFSTAND
where process_id = 'ZEBP'
group by step
order by number desc;

-- different actions per steps
SELECT step, action, count (*) as number
FROM SAPABAP1.ZEZS_VERFSTAND
where process_id = 'ZEBP'
group by step, action
order by step asc;

-- status ebau
SELECT ZEBP_GESUCH.estat, count(*) as number
FROM ZEBP_GESUCH
         join TJ30T on TJ30T.estat = ZEBP_GESUCH.estat
where TJ30T.SPRAS = 'D'
group by ZEBP_GESUCH.estat
order by number desc;

-- status ebau, gruppiert
SELECT TJ30T.TXT30 AS status_text, COUNT(*) AS number
FROM ZEBP_GESUCH g
         left JOIN TJ30T ON TJ30T.estat = g.estat and TJ30T.SPRAS = 'D' and TJ30T.STSMA = 'ZEBP'
         left join ZEZS_CITY city on city.CITY_ID = g.GEMEINDE_ID
WHERE city.CITY in
      ('Aarau', 'Aarburg', 'Arni (AG)', 'Biberstein', 'Dietwil', 'Endingen', 'Fischbach-Göslikon', 'Freienwil',
       'Hellikon',
       'Lengnau (AG)', 'Meisterschwanden', 'Menziken', 'Mettauertal', 'Möhlin', 'Mülligen', 'Obermumpf',
       'Oberwil-Lieli',
       'Olsberg', 'Riniken', 'Suhr', 'Tägerig', 'Tegerfelden', 'Wallbach', 'Würenlingen', 'Zuzgen')
  and g.DIVERSES_KNZ != 'X' and g.VORABKL_KNZ != 'X'
GROUP BY TJ30T.TXT30
ORDER BY number DESC;

SELECT estat, txt30
from tj30t
WHERE TJ30T.SPRAS = 'D'
  and TJ30T.STSMA = 'ZEBP';

-- all groups
SELECT TJ30T.TXT30 AS status, ZEZS_VERFSTAND.Step, ZEZS_VERFSTAND.Action, COUNT(*) AS number
FROM ZEBP_GESUCH
         JOIN TJ30T ON TJ30T.estat = ZEBP_GESUCH.estat
         join ZEZS_VERFSTAND on ZEZS_VERFSTAND.EXTERN_ID = ZEBP_GESUCH.GESUCH_ID
WHERE TJ30T.SPRAS = 'D'
  and TJ30T.STSMA = 'ZEBP'
GROUP BY TJ30T.TXT30, ZEZS_VERFSTAND.step, ZEZS_VERFSTAND.action, zebp_gesuch.estat
ORDER BY zebp_gesuch.estat asc;

-- Aktueller Status + letzter Schritt für ein Gesuch
SELECT g.GESUCH_ID,
       t.TXT30       AS STATUS,
       MAX(v.STEP)   AS LETZTER_SCHRITT,
       MAX(v.ACTION) AS LETZTE_AKTION
FROM ZEBP_GESUCH g
         LEFT JOIN TJ30T t
                   ON t.MANDT = g.MANDT AND t.ESTAT = g.ESTAT AND t.SPRAS = 'D' and t.STSMA = 'ZEBP'
         right JOIN ZEZS_VERFSTAND v
                    ON v.MANDT = g.MANDT AND v.EXTERN_ID = g.GESUCH_ID
GROUP BY g.GESUCH_ID, t.TXT30;

-- Alle Gesuche, die kein Mapping haben
SELECT g.GESUCH_ID,
       t.TXT30                      AS status_text,
       (SELECT STRING_AGG(v.ACTION, ', ' ORDER BY v.TSTAMPL)
        FROM ZEZS_VERFSTAND v
        WHERE v.MANDT = g.MANDT
          AND v.EXTERN_ID = g.GESUCH_ID
          AND v.ACTION IS NOT NULL) AS actions_chronologisch
FROM ZEBP_GESUCH g
         LEFT JOIN TJ30T t
                   ON t.MANDT = g.MANDT
                       AND t.ESTAT = g.ESTAT
                       AND t.SPRAS = 'D'
                       AND t.STSMA = 'ZEBP'
WHERE t.TXT30 NOT IN (
                      'Gesuch in Erfassung',
                      'Gesuch übermittelt',
                      'Gesuch archiviert',
                      'Gesuch zurückgezogen',
                      'Gesuch abgeschrieben',
                      'Gesuch storniert'
    )
  AND NOT EXISTS (SELECT 1
                  FROM ZEZS_VERFSTAND v
                  WHERE v.MANDT = g.MANDT
                    AND v.EXTERN_ID = g.GESUCH_ID
                    AND v.ACTION IN (
                                     'Vorprüfung durchführen',
                                     'Materielle Prüfung gestartet',
                                     'Materielle Prüfung abgeschlossen',
                                     'Verfügung erstellt',
                                     'Gesuch an Kanton senden'
                      ))
ORDER BY g.GESUCH_ID;

-- actions aus mapping mehrfach
SELECT g.GESUCH_ID,
       t.TXT30                      AS status_text,
       (SELECT STRING_AGG(v.ACTION, ', ' ORDER BY v.TSTAMPL)
        FROM ZEZS_VERFSTAND v
        WHERE v.MANDT = g.MANDT
          AND v.EXTERN_ID = g.GESUCH_ID
          AND v.ACTION IS NOT NULL) AS actions_chronologisch
FROM ZEBP_GESUCH g
         LEFT JOIN TJ30T t
                   ON t.MANDT = g.MANDT
                       AND t.ESTAT = g.ESTAT
                       AND t.SPRAS = 'D'
                       AND t.STSMA = 'ZEBP'
WHERE t.TXT30 NOT IN (
                      'Gesuch in Erfassung',
                      'Gesuch übermittelt',
                      'Gesuch archiviert',
                      'Gesuch zurückgezogen',
                      'Gesuch abgeschrieben',
                      'Gesuch storniert',
                      'An Kanton gesendet'
    )
  AND NOT EXISTS (SELECT 1
                  FROM ZEZS_VERFSTAND v
                  WHERE v.MANDT = g.MANDT
                    AND v.EXTERN_ID = g.GESUCH_ID
                    AND v.ACTION = 'Gesuch an Kanton senden')
  AND EXISTS (SELECT 1
              FROM ZEZS_VERFSTAND v
              WHERE v.MANDT = g.MANDT
                AND v.EXTERN_ID = g.GESUCH_ID
                AND v.ACTION IN (
                                 'Vorprüfung durchführen',
                                 'Materielle Prüfung gestartet',
                                 'Materielle Prüfung abgeschlossen',
                                 'Verfügung erstellt'
                  )
              GROUP BY v.ACTION
              HAVING COUNT(*) > 1)
ORDER BY g.GESUCH_ID;


-- count
SELECT COUNT(*) AS anzahl_betroffene_gesuche
FROM ZEBP_GESUCH g
         LEFT JOIN TJ30T t
                   ON t.MANDT = g.MANDT AND t.ESTAT = g.ESTAT AND t.SPRAS = 'D' and t.STSMA = 'ZEBP'
WHERE t.TXT30 NOT IN (
                      'Gesuch in Erfassung',
                      'Gesuch übermittelt',
                      'Gesuch archiviert',
                      'Gesuch zurückgezogen',
                      'Gesuch abgeschrieben',
                      'Gesuch storniert'
    )
  AND NOT EXISTS (SELECT 1
                  FROM ZEZS_VERFSTAND v
                  WHERE v.MANDT = g.MANDT
                    AND v.EXTERN_ID = g.GESUCH_ID
                    AND v.ACTION IN (
                                     'Vorprüfung durchführen',
                                     'Materielle Prüfung gestartet',
                                     'Materielle Prüfung abgeschlossen',
                                     'Verfügung erstellt'
                      ));


-- strange EINDAT
select c.city, GESUCH_ID, EINDAT, CRDAT as creation_date
from ZEBP_GESUCH g
         left join ZEZS_CITY c on g.gemeinde_id = c.city_id
         LEFT JOIN TJ30T t
                   ON t.MANDT = g.MANDT AND t.ESTAT = g.ESTAT AND t.SPRAS = 'D' and t.STSMA = 'ZEBP'
where g.EINDAT < 20170000
  and t.txt30 != 'Gesuch in Erfassung'
order by c.city, g.EINDAT;


select g.GESUCH_ID, t.TXT30 as GEMEINDE_STATUS, te.TXT30 as KANTONS_STATUS
from ZEBP_GESUCH g
         left join ZEB2_A_REQUEST ge on g.GESUCH_ID = ge.GESUCH_ID
         left join TJ30T t on t.ESTAT = g.ESTAT and t.STSMA = 'ZEBP'
         left join TJ30T te on te.ESTAT = ge.ESTAT and te.STSMA = 'ZEB2_REQ'
where te.TXT30 is not null
  and t.TXT30 = 'An Kanton gesendet';

-- Gesuche in Papierform
select CASE
           WHEN erfgrnd = '1' THEN 'Gesuch in Papierform'
           WHEN erfgrnd = '2' THEN 'Bauen ohne Baubewilligung'
           WHEN erfgrnd = '3' THEN 'Nacherfassung'
           WHEN erfgrnd = '4' THEN 'Online Erfassung'
           ELSE erfgrnd -- Behalte den Originalwert, wenn es keinen passenden Code gibt
           END AS erfgrnd_uebersetzt,
       count(*)
from zebp_gesuch
group by erfgrnd;

SELECT CASE
           WHEN erfgrnd = '1' THEN 'Gesuch in Papierform'
           WHEN erfgrnd = '2' THEN 'Bauen ohne Baubewilligung'
           WHEN erfgrnd = '3' THEN 'Nacherfassung'
           WHEN erfgrnd = '4' THEN 'Online Erfassung'
           ELSE erfgrnd -- Behalte den Originalwert, wenn es keinen passenden Code gibt
           END AS erfgrnd_uebersetzt,
       count(*)
FROM ZEBP_GESUCH g
WHERE EXISTS (SELECT 1
              FROM ZEBP_BERECHT b
              WHERE b.GESUCH_ID = g.GESUCH_ID
                and b.partner like 'N%')
group by g.erfgrnd;


select distinct partner
from ZEBP_BERECHT
where partner not like 'N%'

select count(*)
from ZEBP_DOK_STATUS
where DMS_VERS = '00'
  and DMS_ID in
      (select DMS_ID
       from ZEBP_DOK_STATUS
       where DMS_VERS = '')
