te.TXT30 in
      ('Vorläufiger Abschluss', 'Sistiert', 'Fachstelle Aufgabe offen', 'Weiterbearbeitung AfB', 'Freigabeverfahren',
       'Zurückgewiesen', 'Neues Gesuch')
  and city.CITY not in
      ('Aarau', 'Aarburg', 'Arni (AG)', 'Biberstein', 'Dietwil', 'Endingen', 'Fischbach-Göslikon', 'Freienwil', 'Hellikon',
       'Lengnau (AG)', 'Meisterschwanden', 'Menziken', 'Mettauertal', 'Möhlin', 'Mülligen', 'Obermumpf', 'Oberwil-Lieli',
       'Olsberg', 'Riniken', 'Suhr', 'Tägerig', 'Tegerfelden', 'Wallbach', 'Würenlingen', 'Zuzgen',
       'ZZ Testgemeinde', 'ZZ Testgemeinde MH 1')
  and g.DIVERSES_KNZ != 'X' and g.VORABKL_KNZ != 'X'
