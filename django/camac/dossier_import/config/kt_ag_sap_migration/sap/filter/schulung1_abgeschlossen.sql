t.TXT30 in ('Gesuch archiviert', 'Gesuch storniert', 'Gesuch abgeschrieben', 'Gesuch zurückgezogen')
  and city.CITY in
      ('Mettauertal', 'Hellikon', 'Mülligen', 'Suhr', 'Meisterschwanden', 'Freienwil', 'Olsberg', 'Obermumpf',
        'Menziken', 'Endingen', 'Oberwil-Lieli')
  and g.DIVERSES_KNZ != 'X' and g.VORABKL_KNZ != 'X'
