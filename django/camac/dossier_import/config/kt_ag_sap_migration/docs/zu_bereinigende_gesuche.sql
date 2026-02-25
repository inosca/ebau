-- Gesuche in Bearbeitung
select city.CITY                                     as GEMEINDE,
       g.GESUCH_ID,
       g.BTITEL                                      as DOSSIER_TITEL,
       t.TXT30                                       as STATUS_TEXT,
       string_agg(v.ACTION, ', ' order by v.TSTAMPL) as ACTION_LISTE
from ZEBP_GESUCH g
         left join TJ30T t on t.ESTAT = g.ESTAT and t.STSMA = 'ZEBP'
         left join ZEZS_CITY city on city.CITY_ID = g.GEMEINDE_ID
         left join ZEZS_VERFSTAND v on v.EXTERN_ID = g.GESUCH_ID
where t.TXT30 = 'Gesuch in Bearbeitung'
  and city.CITY in ('Aarau', 'Aarburg', 'Arni (AG)', 'Biberstein', 'Dietwil', 'Endingen', 'Fischbach-Göslikon', 'Freienwil',
                    'Hellikon', 'Lengnau (AG)', 'Meisterschwanden', 'Menziken', 'Mettauertal', 'Möhlin', 'Mülligen',
                    'Obermumpf', 'Oberwil-Lieli', 'Olsberg', 'Riniken', 'Suhr', 'Tägerig', 'Tegerfelden',
                    'Wallbach', 'Würenlingen', 'Zuzgen'
    )
group by city.CITY, g.GESUCH_ID, g.BTITEL, t.TXT30
order by city.CITY, g.GESUCH_ID;

-- potentiell liegengeblieben
select city.CITY                                              as GEMEINDE,
       g.GESUCH_ID,
       g.BTITEL                                               as DOSSIER_TITEL,
       t.TXT30                                                as STATUS_TEXT,
       TO_VARCHAR(TO_DATE(g.crdat, 'YYYYMMDD'), 'DD.MM.YYYY') as CREATION_DATE
from ZEBP_GESUCH g
         left join TJ30T t on t.ESTAT = g.ESTAT and t.STSMA = 'ZEBP'
         left join ZEZS_CITY city on city.CITY_ID = g.GEMEINDE_ID
where t.TXT30 in ('Verfügung erstellt', 'Gesuch in Bearbeitung', 'Gesuch übermittelt', 'Anfrage / Stellungnahme offen',
                  'In öffentlicher Auflage')
  and city.CITY in ('Aarau', 'Aarburg', 'Arni (AG)', 'Biberstein', 'Dietwil', 'Endingen', 'Fischbach-Göslikon', 'Freienwil',
                    'Hellikon', 'Lengnau (AG)', 'Meisterschwanden', 'Menziken', 'Mettauertal', 'Möhlin', 'Mülligen',
                    'Obermumpf', 'Oberwil-Lieli', 'Olsberg', 'Riniken', 'Suhr', 'Tägerig', 'Tegerfelden',
                    'Wallbach', 'Würenlingen', 'Zuzgen'
    )
order by city.CITY, g.GESUCH_ID;
