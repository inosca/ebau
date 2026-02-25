t.TXT30 in ('Verfügung erstellt', 'Gesuch in Bearbeitung', 'Gesuch übermittelt', 'Anfrage / Stellungnahme offen',
                  'In öffentlicher Auflage')
  and city.CITY in
      ('Mettauertal', 'Hellikon', 'Mülligen', 'Suhr', 'Meisterschwanden', 'Freienwil', 'Olsberg', 'Obermumpf',
        'Menziken', 'Endingen', 'Oberwil-Lieli')
  and g.DIVERSES_KNZ != 'X' and g.VORABKL_KNZ != 'X'
