t.TXT30 in ('Gesuch archiviert', 'Gesuch storniert', 'Gesuch abgeschrieben', 'Gesuch zurückgezogen')
  and city.CITY in
        ('Fischbach-Göslikon', 'Aarburg', 'Möhlin', 'Zuzgen', 'Tägerig', 'Biberstein', 'Arni (AG)', 'Wallbach',
        'Tegerfelden', 'Lengnau (AG)', 'Würenlingen', 'Riniken')
  and g.DIVERSES_KNZ != 'X' and g.VORABKL_KNZ != 'X'
