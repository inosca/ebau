-- status non-ebau-gemeinden
SELECT ge.KANTON_STATUS AS status_code,
       te.TXT30         AS status_beschreibung,
       COUNT(*)         AS anzahl_gesuche
from ZEBP_GESUCH g
         left join ZEB2_A_REQUEST ge on g.GESUCH_ID = ge.GESUCH_ID
         left join ZEZS_CITY city on city.CITY_ID = g.GEMEINDE_ID
         left join TJ30T te on te.ESTAT = ge.KANTON_STATUS and te.STSMA = 'ZEB2_REQ'
where city.CITY not in
      ('Aarau', 'Aarburg', 'Arni (AG)', 'Biberstein', 'Dietwil', 'Endingen', 'Fischbach-Göslikon', 'Freienwil',
       'Hellikon',
       'Lengnau (AG)', 'Meisterschwanden', 'Menziken', 'Mettauertal', 'Möhlin', 'Mülligen', 'Obermumpf',
       'Oberwil-Lieli',
       'Olsberg', 'Riniken', 'Suhr', 'Tägerig', 'Tegerfelden', 'Wallbach', 'Würenlingen', 'Zuzgen',
       'ZZ Testgemeinde', 'ZZ Testgemeinde MH 1')
  and ge.KANTON_STATUS is not null
  and g.DIVERSES_KNZ != 'X' and g.VORABKL_KNZ != 'X'
GROUP BY ge.KANTON_STATUS,
    te.TXT30
ORDER BY anzahl_gesuche DESC;

select distinct tj30.stsma
from tj30
where tj30.stsma like 'ZEB2%'

-- Gesuche mit Status "An Kanton gesendet" (aus ZEBP_GESUCH) ODER
-- mit Aktion "Gesuch an Kanton senden" (aus ZEZS_VERFSTAND),
-- die NICHT in ZEB2_A_REQUEST vorhanden sind
SELECT gesendet.GESUCH_ID
FROM (
         -- Teil 1: Gesuche mit Status "An Kanton gesendet"
         SELECT DISTINCT g.GESUCH_ID
         FROM ZEBP_GESUCH g
                  JOIN TJ30T t
                       ON g.ESTAT = t.ESTAT AND t.STSMA = 'ZEBP' AND t.SPRAS = 'D'
         WHERE t.TXT30 = 'An Kanton gesendet'

         UNION

         -- Teil 2: Gesuche mit Verfahrensaktion "Gesuch an Kanton senden"
         SELECT DISTINCT EXTERN_ID as GESUCH_ID
         FROM ZEZS_VERFSTAND
         WHERE ACTION = 'Gesuch an Kanton senden') AS gesendet
WHERE gesendet.GESUCH_ID NOT IN (SELECT ZEB2_A_REQUEST.GESUCH_ID
                                 FROM ZEB2_A_REQUEST);

-- ALLE eBau AG Gesuche, die an den Kanton gesendet sind
-- Teil 1: Gesuche mit Status "An Kanton gesendet"
select count(*)
from (SELECT DISTINCT g.GESUCH_ID
      FROM ZEBP_GESUCH g
               JOIN TJ30T t
                    ON g.ESTAT = t.ESTAT AND t.STSMA = 'ZEBP' AND t.SPRAS = 'D'
      WHERE t.TXT30 = 'An Kanton gesendet'
      union
-- Teil 2: Gesuche mit Verfahrensaktion "Gesuch an Kanton senden"
      SELECT DISTINCT EXTERN_ID
      FROM ZEZS_VERFSTAND
      WHERE ACTION = 'Gesuch an Kanton senden');

select count(*)
from ZEB2_A_REQUEST;

-- alle Gemeinden, die Gesuche in eBau extended haben
SELECT c.CITY_ID,
       c.CITY                      AS gemeinde_name,
       COUNT(DISTINCT g.GESUCH_ID) AS anzahl_gesuche
FROM ZEBP_GESUCH g
         JOIN ZEZS_CITY c
              ON g.GEMEINDE_ID = c.CITY_ID
WHERE g.ESTAT IN (SELECT t.ESTAT
                  FROM TJ30T t
                  WHERE t.TXT30 = 'An Kanton gesendet'
                    AND t.STSMA = 'ZEBP'
                    AND t.SPRAS = 'D')
   OR g.GESUCH_ID IN (SELECT v.EXTERN_ID
                      FROM ZEZS_VERFSTAND v
                      WHERE v.ACTION = 'Gesuch an Kanton senden')
GROUP BY c.CITY_ID, c.CITY
ORDER BY anzahl_gesuche DESC;

-- eBau AG GEmeinden, deren Gesuche nicht an den Kanton gingen
SELECT c.CITY_ID,
       c.CITY                      AS gemeinde_name,
       COUNT(DISTINCT g.GESUCH_ID) AS anzahl_gesuche
FROM ZEBP_GESUCH g
         JOIN ZEZS_CITY c
              ON g.GEMEINDE_ID = c.CITY_ID
WHERE g.GESUCH_ID NOT IN (SELECT DISTINCT gsub.GESUCH_ID
                          FROM ZEBP_GESUCH gsub
                                   JOIN TJ30T t
                                        ON gsub.ESTAT = t.ESTAT AND t.STSMA = 'ZEBP' AND t.SPRAS = 'D'
                          WHERE t.TXT30 = 'An Kanton gesendet'

                          UNION

                          SELECT v.EXTERN_ID
                          FROM ZEZS_VERFSTAND v
                          WHERE v.ACTION = 'Gesuch an Kanton senden')
GROUP BY c.CITY_ID, c.CITY
ORDER BY anzahl_gesuche DESC;

-- Gemeinden mit Gesuchen an beiden Orten
SELECT c.CITY_ID,
       c.CITY AS gemeinde_name,
       kanton.anzahl_an_kanton,
       nicht_kanton.anzahl_nicht_an_kanton
FROM ZEZS_CITY c

-- Join auf Gemeinden mit Gesuchen an den Kanton
         JOIN (SELECT g.GEMEINDE_ID, COUNT(DISTINCT g.GESUCH_ID) AS anzahl_an_kanton
               FROM ZEBP_GESUCH g
               WHERE g.ESTAT IN (SELECT t.ESTAT
                                 FROM TJ30T t
                                 WHERE t.TXT30 = 'An Kanton gesendet'
                                   AND t.STSMA = 'ZEBP'
                                   AND t.SPRAS = 'D')
                  OR g.GESUCH_ID IN (SELECT v.EXTERN_ID
                                     FROM ZEZS_VERFSTAND v
                                     WHERE v.ACTION = 'Gesuch an Kanton senden')
               GROUP BY g.GEMEINDE_ID) AS kanton
              ON c.CITY_ID = kanton.GEMEINDE_ID

-- Join auf Gemeinden mit Gesuchen NICHT an den Kanton
         JOIN (SELECT g.GEMEINDE_ID, COUNT(DISTINCT g.GESUCH_ID) AS anzahl_nicht_an_kanton
               FROM ZEBP_GESUCH g
               WHERE g.GESUCH_ID NOT IN (SELECT DISTINCT gsub.GESUCH_ID
                                         FROM ZEBP_GESUCH gsub
                                                  JOIN TJ30T t
                                                       ON gsub.ESTAT = t.ESTAT AND t.STSMA = 'ZEBP' AND t.SPRAS = 'D'
                                         WHERE t.TXT30 = 'An Kanton gesendet'

                                         UNION

                                         SELECT v.EXTERN_ID
                                         FROM ZEZS_VERFSTAND v
                                         WHERE v.ACTION = 'Gesuch an Kanton senden')
               GROUP BY g.GEMEINDE_ID) AS nicht_kanton
              ON c.CITY_ID = nicht_kanton.GEMEINDE_ID

ORDER BY anzahl_nicht_an_kanton desc, anzahl_an_kanton desc;

-- Korrelation Status eBau AG und eBau extended
SELECT local_status.TXT30  AS lokaler_status,
       kanton_status.TXT30 AS kanton_status,
       COUNT(*)            AS anzahl_gesuche
FROM ZEBP_GESUCH g
         JOIN ZEB2_A_REQUEST r
              ON g.GESUCH_ID = r.GESUCH_ID

-- lokale Statusbezeichnung aus ESTAT
         LEFT JOIN TJ30T local_status
                   ON g.ESTAT = local_status.ESTAT
                       AND local_status.STSMA = 'ZEBP'
                       AND local_status.SPRAS = 'D'

-- kantonale Statusbezeichnung aus KANTON_STATUS
         LEFT JOIN TJ30T kanton_status
                   ON r.KANTON_STATUS = kanton_status.ESTAT
                       AND kanton_status.STSMA = 'ZEB2_REQ'
                       AND kanton_status.SPRAS = 'D'

GROUP BY local_status.TXT30,
         kanton_status.TXT30

ORDER BY anzahl_gesuche DESC;

--- Anz. Gesuche je Status eBau AG only
SELECT t.TXT30  AS lokaler_status,
       COUNT(*) AS anzahl_gesuche
FROM ZEBP_GESUCH g
         LEFT JOIN TJ30T t
                   ON g.ESTAT = t.ESTAT
                       AND t.STSMA = 'ZEBP'
                       AND t.SPRAS = 'D'
WHERE g.GESUCH_ID NOT IN (SELECT r.GESUCH_ID
                          FROM ZEB2_A_REQUEST r)
GROUP BY t.TXT30
ORDER BY anzahl_gesuche DESC;


-- Hauptquery: Zentrale Tabelle ZEB2_A_REQUEST mit 1:1 verknüpften Tabellen
SELECT req.REQUEST_ID,
       req.GESUCH_ID,
       req.KANTON_STATUS,
       req.PROJECT_ID,
       req.CREATED_ON,
       req.CREATED_BY,
       req.LAST_CHANGED_ON,
       req.LAST_CHANGED_BY,

       adr.*,    -- Adresse
       geo.*,    -- Geodaten
       bau.*,    -- Bauvorhaben allgemein
       kontakt.* -- Kontaktperson

FROM ZEB2_A_REQUEST req

-- 1:1 Verknüpfte Tabellen
         LEFT JOIN ZEB2_A_ADDRESS adr
                   ON req.REQUEST_ID = adr.REQUEST_ID

         LEFT JOIN ZEB2_A_GEODATA geo
                   ON req.REQUEST_ID = geo.REQUEST_ID

         LEFT JOIN ZEB2_A_BUILDING bau
                   ON req.REQUEST_ID = bau.REQUEST_ID

         LEFT JOIN ZEB2_A_CONTACT kontakt
                   ON req.REQUEST_ID = kontakt.REQUEST_ID

WHERE req.GESUCH_ID = 'EBPA-3304-0441';

-- 1:n Nebenquery: Dokumente zum Gesuch
SELECT *
FROM ZEB2_A_DOCUMENT
WHERE REQUEST_ID = (SELECT REQUEST_ID
                    FROM ZEB2_A_REQUEST
                    WHERE GESUCH_ID = 'EBPA-3304-0441');

-- 1:n Nebenquery: Beteiligte Parteien
SELECT *
FROM ZEB2_A_PARTY
WHERE REQUEST_ID = (SELECT REQUEST_ID
                    FROM ZEB2_A_REQUEST
                    WHERE GESUCH_ID = 'EBPA-3304-0441');

-- 1:n Nebenquery: Bauteile (z.B. Erweiterungen)
SELECT *
FROM ZEB2_A_COMPONENT
WHERE REQUEST_ID = (SELECT REQUEST_ID
                    FROM ZEB2_A_REQUEST
                    WHERE GESUCH_ID = 'EBPA-3304-0441');

-- 1:n Nebenquery: Stellungnahmen
SELECT *
FROM ZEB2_A_COMMENT
WHERE REQUEST_ID = (SELECT REQUEST_ID
                    FROM ZEB2_A_REQUEST
                    WHERE GESUCH_ID = 'EBPA-3304-0441');


--- Actions von Gesuchen von eBau - Gemeinden mit kantonaler Beteiligung
SELECT c.CITY                       AS gemeinde,
       t.TXT30                      AS status_text,
       (SELECT STRING_AGG(v.ACTION, ', ' ORDER BY v.TSTAMPL)
        FROM ZEZS_VERFSTAND v
        WHERE v.MANDT = g.MANDT
          AND v.EXTERN_ID = g.GESUCH_ID
          AND v.ACTION IS NOT NULL) AS actions_chronologisch
FROM ZEB2_A_REQUEST r
         JOIN ZEBP_GESUCH g
              ON g.GESUCH_ID = r.GESUCH_ID
         LEFT JOIN TJ30T t
                   ON t.MANDT = g.MANDT
                       AND t.ESTAT = g.ESTAT
                       AND t.STSMA = 'ZEBP'
                       AND t.SPRAS = 'D'
         LEFT JOIN ZEZS_CITY c
                   ON c.CITY_ID = g.GEMEINDE_ID
WHERE c.CITY IN (
                 'Aarburg', 'Arni (AG)', 'Aarau', 'Biberstein', 'Dietwil', 'Endingen', 'Freienwil',
                 'Fischbach-Göslikon',
                 'Hellikon',
                 'Lengnau (AG)', 'Meisterschwanden', 'Menziken', 'Mettauertal', 'Möhlin', 'Mülligen', 'Obermumpf',
                 'Oberwil-Lieli',
                 'Olsberg', 'Riniken', 'Suhr', 'Tägerig', 'Tegerfelden', 'Wallbach', 'Würenlingen', 'Zuzgen'
    )
  and c.CITy <> 'Aarau'
ORDER BY c.CITY, t.TXT30;

-- Gesuchs Art / Request Type

-- eBau extended - Gesuchsart
select ga.GESART,
       CASE ga.GESART
           WHEN '1' THEN 'Anfrage'
           WHEN '2' THEN 'Baugesuch'
           WHEN '3' THEN 'Umweltverträglichkeitsprüfung (UVP)'
           WHEN '4' THEN 'Umnutzung'
           WHEN '5' THEN 'Vorentscheid'
           WHEN '6' THEN 'Rodung'
           WHEN '7' THEN 'Reklame'
           WHEN '8' THEN 'Abbruch'
           WHEN '9' THEN 'PGV'
           WHEN '10' THEN 'Anhörung'
           END AS GESART_TEXT,
       rt.DESCRIPTION
from ZEB2_A_REQUEST geZEBP_GESUCH g
         left join ZEBP_GESART ga
on g.GESUCH_ID = ga.GESUCH_ID
    left join ZEB2_A_REQUEST ge
    on g.GESUCH_ID = ge.GESUCH_ID
    left join ZEB2_C_REQ_TYPET rt on ge.REQUEST_TYPE = rt.REQUEST_TYPE
where g.GESUCH_ID = 'EBPA-4406-5058';

-- in eBau extended Gesuchsart gewählt => nur in ZEB2_A_REQ.REQUEST_TYPE, keine Einträge mehr in ZEBP_GESUCH
-- Zweiter Wert in eBau extended Gesuchsart gewählt => nur in ZEB2_A_REQ.REQUEST_TYPE, nur 2. ausgewählter Wert
-- alle angehakt => Anfragegesuch
--    Anfrage abgehakt => Baugesuch
--    Baugesuch abgehakt => UVP
--     ...
-- ABER: die Auswahl von eBau extended wird in eBau Aargau angezeigt, obwohl ZEBP_GESART leer ist
-- Diverses in eBau extended: null in GESART und null in REQUEST_TYPE
-- eBau extended - nur PGV => nur REQUEST_TYPE PGV
-- => nur wenn ich das in eBau erfasste Gesuch nicht mehr ändere, hat es in ZEBP_GESART Werte


--
--     Gesuchsarten der fiktiven eBau Gemeinde
--
select ga.GESART,
       CASE ga.GESART
           WHEN '1' THEN 'Anfrage'
           WHEN '2' THEN 'Baugesuch'
           WHEN '3' THEN 'Umweltverträglichkeitsprüfung (UVP)'
           WHEN '4' THEN 'Umnutzung'
           WHEN '5' THEN 'Vorentscheid'
           WHEN '6' THEN 'Rodung'
           WHEN '7' THEN 'Reklame'
           WHEN '8' THEN 'Abbruch'
           WHEN '9' THEN 'PGV'
           WHEN '10' THEN 'Anhörung'
           END AS GESART_TEXT,
       rt.DESCRIPTION,
       count(*)
from ZEBP_GESUCH g
         left join ZEBP_GESART ga on g.GESUCH_ID = ga.GESUCH_ID
         left join ZEB2_A_REQUEST ge
                   on g.GESUCH_ID = ge.GESUCH_ID
         left join ZEB2_C_REQ_TYPET rt on ge.REQUEST_TYPE = rt.REQUEST_TYPE
where g.GEMEINDE_ID = 1
group by ga.GESART, rt.DESCRIPTION
order by count(*) desc;

-- Parzellen für Gesuche mit der fiktiven Gemeinde: gibt es da immer 2, eine für CITY und eine für die Gemeinde ?
SELECT DISTINCT g.GESUCH_ID, p.*
FROM ZEBP_GESUCH g
         JOIN ZEBP_PARZ p ON g.GESUCH_ID = p.GESUCH_ID
WHERE g.GEMEINDE_ID = '0001'
  AND p.CITY_ID = '0001'
  AND NOT EXISTS (SELECT 1
                  FROM ZEBP_PARZ p2
                  WHERE p2.GESUCH_ID = g.GESUCH_ID
                    AND p2.PARZNR = p.PARZNR
                    AND p2.CITY_ID <> '0001')
ORDER BY g.GESUCH_ID, p.CITY_ID;

SELECT s.CITY_ID, g.*
FROM ZEBP_GESUCH g
         LEFT JOIN ZEBP_STORT s ON g.GESUCH_ID = s.GESUCH_ID
WHERE g.GEMEINDE_ID = '0001'
  AND s.GESUCH_ID IS not NULL
ORDER BY g.GESUCH_ID;


--- Gesuchscodes
select distinct BAUG_ID, DESCRIPTION
from ZEB2_A_RQ_BGSTYP
         left join zeb2_c_baugstypt on ZEB2_A_RQ_BGSTYP.BAUG_ID = zeb2_c_baugstypt.id
where REQUEST_ID = 'EBPA-4406-5058';

select id, description
from ZEB2_C_BAUGSTYPT;

-- Nutzungszonen
select DESCRIPTION
from ZEB2_A_RQ_NTZONE
         left join zeb2_c_ntzonet on ZEB2_A_RQ_NTZONE.zone_id = ZEB2_C_NTZONET.id
where REQUEST_ID = 'EBPA-4406-5058';

-- Schutzzonen
select DESCRIPTION
from ZEB2_A_RQ_SZZONE
         left join ZEB2_C_SCHZZONET on ZEB2_A_RQ_SZZONE.zone_id = ZEB2_C_SCHZZONET.id
where REQUEST_ID = 'EBPA-4406-5058';

-- Strassen
select description, road_number
from ZEB2_A_RQ_STRTYP
         left join zeb2_c_strtypt on ZEB2_A_RQ_STRTYP.street_type = ZEB2_C_STRTYPT.street_type
where REQUEST_ID = 'EBPA-4406-5058';

-- Bahnen
select description
from ZEB2_A_RQ_BAHN
         left join ZEB2_C_BAHNT on ZEB2_A_RQ_BAHN.bahn_id = ZEB2_C_BAHNT.id
where REQUEST_ID = 'EBPA-4406-5058';

-- Gewässer
select river_id, river_name
from ZEB2_A_RQ_GEWAS
where REQUEST_ID = 'EBPA-4406-5058';

--- Kanalisation
select distinct ka_ban_knz
from ZEB2_A_REQUEST;

--- Gebühren
select gc.COST_TYPE,
       ctt.DESCRIPTION,
       cs.calculation_scheme,
       CALC_SCHEME_POSITION,
       request_task_id,
       UNIT_PRICE,
       AMOUNT,
       MSEHI,
       TAKE,
       SHOW_IN_GV,
       COMMENT_FS,
       COMMENT_AFB
from ZEB2_A_GESCOST gc
         left join ZEB2_C_COSTTYPET ctt on gc.cost_type = ctt.cost_type
         left join ZEB2_C_CSCHEMEH cs on gc.calc_scheme_id = cs.calc_scheme_id
where REQUEST_ID = 'EBPA-2683-9115';


--- Sistierungen
select te.TXT30 as KANTONSTATUS, ge.completion_date, DATVON, DATBIS, NOTE, REASON, t.TXT30 as prev_status, s.created_on, s.created_by, resume_date, resume_by
from ZEB2_A_SUSPENS s
         LEFT JOIN TJ30T t on s.PREVIOUS_STATUS = t.ESTAT AND t.STSMA = 'ZEB2_REQ' AND t.SPRAS = 'D'
        left join ZEB2_A_REQUEST ge on ge.GESUCH_ID = s.REQUEST_ID
         LEFT JOIN TJ30T te on ge.KANTON_STATUS = te.ESTAT AND te.STSMA = 'ZEB2_REQ' AND te.SPRAS = 'D'
where ge.completion_date != '00000000' and te.txt30 not in ('Definitiver Abschluss', 'Vorläufiger Abschluss');

