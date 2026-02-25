t.TXT30 in ('Gesuch archiviert', 'Gesuch storniert', 'Gesuch abgeschrieben', 'Gesuch zurückgezogen')
  and city.CITY in
      ('Aarau', 'Aarburg', 'Arni (AG)', 'Biberstein', 'Dietwil', 'Endingen', 'Fischbach-Göslikon', 'Freienwil', 'Hellikon',
       'Lengnau (AG)', 'Meisterschwanden', 'Menziken', 'Mettauertal', 'Möhlin', 'Mülligen', 'Obermumpf', 'Oberwil-Lieli',
       'Olsberg', 'Riniken', 'Suhr', 'Tägerig', 'Tegerfelden', 'Wallbach', 'Würenlingen', 'Zuzgen')
  and g.DIVERSES_KNZ != 'X' and g.VORABKL_KNZ != 'X'
