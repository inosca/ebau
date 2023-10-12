# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_gr_client[query0-baugesuch] 1'] = {
    'data': {
        'ausserhalb-bauzone': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'ausserhalb-bauzone',
            'value': 'ausserhalb-bauzone-nein'
        },
        'das-bauvorhaben-befindet-sich-in': {
            'hidden': False,
            'label': 'das-bauvorhaben-befindet-sich-in',
            'value': [
                {
                    'displayValue': 'gewaesserschutzbereich',
                    'value': 'das-bauvorhaben-befindet-sich-in-gewaesserschutzbereich'
                },
                {
                    'displayValue': 'archaeologiezone',
                    'value': 'das-bauvorhaben-befindet-sich-in-archaeologiezone'
                }
            ]
        },
        'gemeinde': {
            'hidden': False,
            'label': 'gemeinde',
            'value': 'Chur'
        },
        'genereller-erschliessungsplan': {
            'hidden': False,
            'label': 'genereller-erschliessungsplan',
            'value': 'Fussgängerzone Altstadt, Parkierung Gebiete A'
        },
        'genereller-gestaltungsplan': {
            'hidden': False,
            'label': 'genereller-gestaltungsplan',
            'value': 'Bauten und Anlagen schützenswert, Schutzbereich Altstadt'
        },
        'gis-map': {
            'hidden': True,
            'label': 'gis-map',
            'value': '{"markers": [{"x": 2759870.935699284, "y": 1190699.1389424137}], "geometry": "POINT"}'
        },
        'kantonsstrassen': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-nein'
        },
        'ort-grundstueck': {
            'hidden': False,
            'label': 'ort-grundstueck',
            'value': 'Chur'
        },
        'parzelle': {
            'form': 'but-near-attack',
            'hidden': False,
            'label': 'parzelle',
            'value': [
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH676877828654'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '2830'
                    }
                }
            ]
        },
        'street-and-housenumber': {
            'hidden': False,
            'label': 'street-and-housenumber',
            'value': 'Hof 19'
        },
        'waldareal': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'waldareal',
            'value': 'waldareal-nein'
        },
        'zonenplan': {
            'hidden': False,
            'label': 'zonenplan',
            'value': 'Keine Gefahrenzone, Archäologiezone, Zentrumszone Altstadt 2'
        }
    }
}

snapshots['test_gr_client[query1-baugesuch] 1'] = {
    'data': {
        'ausserhalb-bauzone': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'ausserhalb-bauzone',
            'value': 'ausserhalb-bauzone-nein'
        },
        'das-bauvorhaben-befindet-sich-in': {
            'hidden': False,
            'label': 'das-bauvorhaben-befindet-sich-in',
            'value': [
                {
                    'displayValue': 'gewaesserschutzbereich',
                    'value': 'das-bauvorhaben-befindet-sich-in-gewaesserschutzbereich'
                }
            ]
        },
        'gemeinde': {
            'hidden': False,
            'label': 'gemeinde',
            'value': 'Roveredo (GR)'
        },
        'genereller-gestaltungsplan': {
            'hidden': False,
            'label': 'genereller-gestaltungsplan',
            'value': 'Linea di allineamento per la strutturazione edilizia, Linea di allineamento per la strutturazione edilizia'
        },
        'gis-map': {
            'hidden': True,
            'label': 'gis-map',
            'value': '{"markers": [{"x": 2730678.226988568, "y": 1122327.0823116319}], "geometry": "POINT"}'
        },
        'kantonsstrassen': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-nein'
        },
        'ort-grundstueck': {
            'hidden': False,
            'label': 'ort-grundstueck',
            'value': 'Roveredo (GR)'
        },
        'parzelle': {
            'form': 'but-near-attack',
            'hidden': False,
            'label': 'parzelle',
            'value': [
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH737679917002'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '3051'
                    }
                }
            ]
        },
        'waldareal': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'waldareal',
            'value': 'waldareal-nein'
        },
        'zonenplan': {
            'hidden': False,
            'label': 'zonenplan',
            'value': 'Nessuna zona di pericolo, Zona residenziale (i.s. 0.7)'
        }
    }
}

snapshots['test_gr_client[query10-baugesuch] 1'] = {
    'data': {
        'das-bauvorhaben-befindet-sich-in': {
            'hidden': False,
            'label': 'das-bauvorhaben-befindet-sich-in',
            'value': [
                {
                    'displayValue': 'gewaesserschutzbereich',
                    'value': 'das-bauvorhaben-befindet-sich-in-gewaesserschutzbereich'
                }
            ]
        },
        'gemeinde': {
            'hidden': False,
            'label': 'gemeinde',
            'value': 'Chur'
        },
        'gis-map': {
            'hidden': True,
            'label': 'gis-map',
            'value': '{"markers": [{"x": 2757567.75, "y": 1192209.3312499998}], "geometry": "POINT"}'
        },
        'kantonsstrassen': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-nein'
        },
        'ort-grundstueck': {
            'hidden': False,
            'label': 'ort-grundstueck',
            'value': 'Haldenstein'
        },
        'parzelle': {
            'form': 'but-near-attack',
            'hidden': False,
            'label': 'parzelle',
            'value': [
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH427965866853'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '31778'
                    }
                }
            ]
        },
        'waldareal': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'waldareal',
            'value': 'waldareal-nein'
        },
        'zonenplan': {
            'hidden': False,
            'label': 'zonenplan',
            'value': 'Gewässerraumzone, Keine Gefahrenzone, Zone übriges Gemeindegebiet (Gewässer)'
        }
    }
}

snapshots['test_gr_client[query11-baugesuch] 1'] = {
    'data': {
        'das-bauvorhaben-befindet-sich-in': {
            'hidden': False,
            'label': 'das-bauvorhaben-befindet-sich-in',
            'value': [
                {
                    'displayValue': 'gefahrenzone',
                    'value': 'das-bauvorhaben-befindet-sich-in-gefahrenzone'
                },
                {
                    'displayValue': 'gewaesserschutzbereich',
                    'value': 'das-bauvorhaben-befindet-sich-in-gewaesserschutzbereich'
                }
            ]
        },
        'gemeinde': {
            'hidden': False,
            'label': 'gemeinde',
            'value': 'Chur'
        },
        'genereller-erschliessungsplan': {
            'hidden': False,
            'label': 'genereller-erschliessungsplan',
            'value': 'Skatingweg, Fuss- / Radweg Hauptverbindung'
        },
        'genereller-gestaltungsplan': {
            'hidden': False,
            'label': 'genereller-gestaltungsplan',
            'value': 'Gewässerabstandslinien, Baumreihe, einseitig'
        },
        'gis-map': {
            'hidden': True,
            'label': 'gis-map',
            'value': '{"markers": [{"x": 2757771.4499999997, "y": 1192182.0312499998}], "geometry": "POINT"}'
        },
        'kantonsstrassen': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-nein'
        },
        'ort-grundstueck': {
            'hidden': False,
            'label': 'ort-grundstueck',
            'value': 'Chur'
        },
        'parzelle': {
            'form': 'but-near-attack',
            'hidden': False,
            'label': 'parzelle',
            'value': [
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH546886777384'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '1257'
                    }
                }
            ]
        },
        'waldareal': {
            'displayValue': 'waldabstandsbereich',
            'hidden': False,
            'label': 'waldareal',
            'value': 'waldareal-waldabstandsbereich'
        },
        'zonenplan': {
            'hidden': False,
            'label': 'zonenplan',
            'value': 'Statische Waldgrenze gemäss Art. 10/13 Waldgesetz, Statische Waldgrenze gemäss Art. 10/13 Waldgesetz, Gefahrenzone 1, Gewässer'
        }
    }
}

snapshots['test_gr_client[query12-baugesuch] 1'] = {
    'data': {
        'ausserhalb-bauzone': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'ausserhalb-bauzone',
            'value': 'ausserhalb-bauzone-nein'
        },
        'das-bauvorhaben-befindet-sich-in': {
            'hidden': False,
            'label': 'das-bauvorhaben-befindet-sich-in',
            'value': [
                {
                    'displayValue': 'gewaesserschutzbereich',
                    'value': 'das-bauvorhaben-befindet-sich-in-gewaesserschutzbereich'
                },
                {
                    'displayValue': 'archaeologiezone',
                    'value': 'das-bauvorhaben-befindet-sich-in-archaeologiezone'
                }
            ]
        },
        'folgeplanung': {
            'hidden': False,
            'label': 'folgeplanung',
            'value': 'Quartierplan Welschdörfli 4 (hinweisend), GÜP Welschdörfli West (hinweisend)'
        },
        'gemeinde': {
            'hidden': False,
            'label': 'gemeinde',
            'value': 'Chur'
        },
        'genereller-erschliessungsplan': {
            'hidden': False,
            'label': 'genereller-erschliessungsplan',
            'value': 'Parkierung Gebiete B'
        },
        'genereller-gestaltungsplan': {
            'hidden': False,
            'label': 'genereller-gestaltungsplan',
            'value': 'Quartierplan (QP)'
        },
        'gis-map': {
            'hidden': True,
            'label': 'gis-map',
            'value': '{"markers": [{"x": 2759143.4499999997, "y": 1190625.23125}], "geometry": "POINT"}'
        },
        'kantonsstrassen': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-nein'
        },
        'ort-grundstueck': {
            'hidden': False,
            'label': 'ort-grundstueck',
            'value': 'Chur'
        },
        'parzelle': {
            'form': 'but-near-attack',
            'hidden': False,
            'label': 'parzelle',
            'value': [
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH776877828620'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '2733'
                    }
                },
                {
                    'baurecht-nummer': {
                        'label': 'baurecht-nummer',
                        'value': '12768'
                    },
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH907068848655'
                    }
                }
            ]
        },
        'waldareal': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'waldareal',
            'value': 'waldareal-nein'
        },
        'zonenplan': {
            'hidden': False,
            'label': 'zonenplan',
            'value': 'Keine Gefahrenzone, Archäologiezone, Wohnzone 5'
        }
    }
}

snapshots['test_gr_client[query2-bauanzeige] 1'] = {
    'data': {
        'gemeinde': {
            'hidden': False,
            'label': 'gemeinde',
            'value': 'Roveredo (GR)'
        },
        'genereller-gestaltungsplan': {
            'hidden': False,
            'label': 'genereller-gestaltungsplan',
            'value': 'Linea di allineamento per la strutturazione edilizia, Linea di allineamento per la strutturazione edilizia'
        },
        'gis-map': {
            'hidden': True,
            'label': 'gis-map',
            'value': '{"markers": [{"x": 2730678.226988568, "y": 1122327.0823116319}], "geometry": "POINT"}'
        },
        'ort-grundstueck': {
            'hidden': False,
            'label': 'ort-grundstueck',
            'value': 'Roveredo (GR)'
        },
        'parzelle': {
            'form': 'but-near-attack',
            'hidden': False,
            'label': 'parzelle',
            'value': [
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH737679917002'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '3051'
                    }
                }
            ]
        },
        'zonenplan': {
            'hidden': False,
            'label': 'zonenplan',
            'value': 'Nessuna zona di pericolo, Zona residenziale (i.s. 0.7)'
        }
    }
}

snapshots['test_gr_client[query3-baugesuch] 1'] = {
    'data': {
        'ausserhalb-bauzone': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'ausserhalb-bauzone',
            'value': 'ausserhalb-bauzone-nein'
        },
        'das-bauvorhaben-befindet-sich-in': {
            'hidden': False,
            'label': 'das-bauvorhaben-befindet-sich-in',
            'value': [
                {
                    'displayValue': 'gewaesserschutzbereich',
                    'value': 'das-bauvorhaben-befindet-sich-in-gewaesserschutzbereich'
                }
            ]
        },
        'gemeinde': {
            'hidden': False,
            'label': 'gemeinde',
            'value': 'Roveredo (GR)'
        },
        'genereller-erschliessungsplan': {
            'hidden': False,
            'label': 'genereller-erschliessungsplan',
            'value': 'Percorso pedonale, Percorso pedonale'
        },
        'gis-map': {
            'hidden': True,
            'label': 'gis-map',
            'value': '{"markers": [{"x": 2730686.563711087, "y": 1122237.578980265}, {"x": 2730701.779260571, "y": 1122223.4682885902}], "geometry": "LINESTRING"}'
        },
        'kantonsstrassen': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-nein'
        },
        'ort-grundstueck': {
            'hidden': False,
            'label': 'ort-grundstueck',
            'value': 'Roveredo (GR)'
        },
        'parzelle': {
            'form': 'but-near-attack',
            'hidden': False,
            'label': 'parzelle',
            'value': [
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH356476789154'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '920'
                    }
                },
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH479178647641'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '921'
                    }
                }
            ]
        },
        'street-and-housenumber': {
            'hidden': False,
            'label': 'street-and-housenumber',
            'value': "Sant'Antoni 11, 13, 17"
        },
        'waldareal': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'waldareal',
            'value': 'waldareal-nein'
        },
        'zonenplan': {
            'hidden': False,
            'label': 'zonenplan',
            'value': 'Nessuna zona di pericolo, Zona nucleo di nuova formazione'
        }
    }
}

snapshots['test_gr_client[query4-baugesuch] 1'] = {
    'data': {
        'ausserhalb-bauzone': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'ausserhalb-bauzone',
            'value': 'ausserhalb-bauzone-nein'
        },
        'das-bauvorhaben-befindet-sich-in': {
            'hidden': False,
            'label': 'das-bauvorhaben-befindet-sich-in',
            'value': [
                {
                    'displayValue': 'gewaesserschutzbereich',
                    'value': 'das-bauvorhaben-befindet-sich-in-gewaesserschutzbereich'
                }
            ]
        },
        'folgeplanung': {
            'hidden': False,
            'label': 'folgeplanung',
            'value': 'Baulinie allgemein'
        },
        'gemeinde': {
            'hidden': False,
            'label': 'gemeinde',
            'value': 'Chur'
        },
        'genereller-erschliessungsplan': {
            'hidden': False,
            'label': 'genereller-erschliessungsplan',
            'value': 'Fuss- / Radweg Hauptverbindung, Sammelstrasse, Parkierung Gebiete B'
        },
        'genereller-gestaltungsplan': {
            'hidden': False,
            'label': 'genereller-gestaltungsplan',
            'value': 'Baumreihe, einseitig'
        },
        'gis-map': {
            'hidden': True,
            'label': 'gis-map',
            'value': '{"markers": [{"x": 2758821.8885866464, "y": 1191884.7759206274}, {"x": 2758835.689140816, "y": 1191889.2217609326}, {"x": 2758844.747878619, "y": 1191856.4200200567}, {"x": 2758832.507804883, "y": 1191854.8711072344}], "geometry": "POLYGON"}'
        },
        'kantonsstrassen': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-nein'
        },
        'ort-grundstueck': {
            'hidden': False,
            'label': 'ort-grundstueck',
            'value': 'Chur'
        },
        'parzelle': {
            'form': 'but-near-attack',
            'hidden': False,
            'label': 'parzelle',
            'value': [
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH838677680049'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '4629'
                    }
                },
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH827700866871'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '4628'
                    }
                },
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH846886770055'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '4630'
                    }
                },
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH880086687762'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '4624'
                    }
                },
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH807768008655'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '4626'
                    }
                },
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH816800867795'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '4627'
                    }
                },
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH898677006887'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '4625'
                    }
                }
            ]
        },
        'street-and-housenumber': {
            'hidden': False,
            'label': 'street-and-housenumber',
            'value': 'Scalettastrasse; Alpsteinweg 2'
        },
        'waldareal': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'waldareal',
            'value': 'waldareal-nein'
        },
        'zonenplan': {
            'hidden': False,
            'label': 'zonenplan',
            'value': 'Keine Gefahrenzone, Wohnzone 2'
        }
    }
}

snapshots['test_gr_client[query5-baugesuch] 1'] = {
    'data': {
        'ausserhalb-bauzone': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'ausserhalb-bauzone',
            'value': 'ausserhalb-bauzone-nein'
        },
        'das-bauvorhaben-befindet-sich-in': {
            'hidden': False,
            'label': 'das-bauvorhaben-befindet-sich-in',
            'value': [
                {
                    'displayValue': 'gewaesserschutzbereich',
                    'value': 'das-bauvorhaben-befindet-sich-in-gewaesserschutzbereich'
                }
            ]
        },
        'gemeinde': {
            'hidden': False,
            'label': 'gemeinde',
            'value': 'Roveredo (GR)'
        },
        'gis-map': {
            'hidden': True,
            'label': 'gis-map',
            'value': '{"markers": [{"x": 2731195.9499999997, "y": 1122174.3312499998}], "geometry": "POINT"}'
        },
        'kantonsstrassen': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-nein'
        },
        'ort-grundstueck': {
            'hidden': False,
            'label': 'ort-grundstueck',
            'value': 'Roveredo (GR)'
        },
        'parzelle': {
            'form': 'but-near-attack',
            'hidden': False,
            'label': 'parzelle',
            'value': [
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH786876917826'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '493'
                    }
                },
                {
                    'baurecht-nummer': {
                        'label': 'baurecht-nummer',
                        'value': '544'
                    },
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH837678916876'
                    }
                }
            ]
        },
        'street-and-housenumber': {
            'hidden': False,
            'label': 'street-and-housenumber',
            'value': 'Véra 10, 12'
        },
        'waldareal': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'waldareal',
            'value': 'waldareal-nein'
        },
        'zonenplan': {
            'hidden': False,
            'label': 'zonenplan',
            'value': 'Nessuna zona di pericolo, Zona per edifici pubblici (GdS III)'
        }
    }
}

snapshots['test_gr_client[query6-baugesuch] 1'] = {
    'data': {
        'ausserhalb-bauzone': {
            'displayValue': 'ja',
            'hidden': False,
            'label': 'ausserhalb-bauzone',
            'value': 'ausserhalb-bauzone-ja'
        },
        'gemeinde': {
            'hidden': False,
            'label': 'gemeinde',
            'value': 'Chur'
        },
        'gis-map': {
            'hidden': True,
            'label': 'gis-map',
            'value': '{"markers": [{"x": 2758622.7126099495, "y": 1190131.3069476}], "geometry": "POINT"}'
        },
        'kantonsstrassen': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-nein'
        },
        'ort-grundstueck': {
            'hidden': False,
            'label': 'ort-grundstueck',
            'value': 'Chur'
        },
        'parzelle': {
            'form': 'but-near-attack',
            'hidden': False,
            'label': 'parzelle',
            'value': [
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH698677986855'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '3479'
                    }
                }
            ]
        },
        'waldareal': {
            'displayValue': 'ja',
            'hidden': False,
            'label': 'waldareal',
            'value': 'waldareal-ja'
        },
        'zonenplan': {
            'hidden': False,
            'label': 'zonenplan',
            'value': 'Auf Gefahrenzonen nicht untersuchtes Gebiet (orientierend), Wald (orientierend)'
        }
    }
}

snapshots['test_gr_client[query7-baugesuch] 1'] = {
    'data': {
        'ausserhalb-bauzone': {
            'displayValue': 'ja',
            'hidden': False,
            'label': 'ausserhalb-bauzone',
            'value': 'ausserhalb-bauzone-ja'
        },
        'gemeinde': {
            'hidden': False,
            'label': 'gemeinde',
            'value': 'Chur'
        },
        'gis-map': {
            'hidden': True,
            'label': 'gis-map',
            'value': '{"markers": [{"x": 2760943.8499999996, "y": 1192035.0312499998}], "geometry": "POINT"}'
        },
        'kantonsstrassen': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-nein'
        },
        'ort-grundstueck': {
            'hidden': False,
            'label': 'ort-grundstueck',
            'value': 'Chur'
        },
        'parzelle': {
            'form': 'but-near-attack',
            'hidden': False,
            'label': 'parzelle',
            'value': [
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH416823867724'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '6978'
                    }
                }
            ]
        },
        'waldareal': {
            'displayValue': 'waldabstandsbereich',
            'hidden': False,
            'label': 'waldareal',
            'value': 'waldareal-waldabstandsbereich'
        },
        'zonenplan': {
            'hidden': False,
            'label': 'zonenplan',
            'value': 'Keine Gefahrenzone, Landwirtschaftszone'
        }
    }
}

snapshots['test_gr_client[query8-baugesuch] 1'] = {
    'data': {
        'ausserhalb-bauzone': {
            'displayValue': 'ja',
            'hidden': False,
            'label': 'ausserhalb-bauzone',
            'value': 'ausserhalb-bauzone-ja'
        },
        'gemeinde': {
            'hidden': False,
            'label': 'gemeinde',
            'value': 'Chur'
        },
        'gis-map': {
            'hidden': True,
            'label': 'gis-map',
            'value': '{"markers": [{"x": 2760930.5289222472, "y": 1192035.707010256}, {"x": 2760963.900865463, "y": 1192057.817393839}], "geometry": "LINESTRING"}'
        },
        'kantonsstrassen': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-nein'
        },
        'ort-grundstueck': {
            'hidden': False,
            'label': 'ort-grundstueck',
            'value': 'Chur'
        },
        'parzelle': {
            'form': 'but-near-attack',
            'hidden': False,
            'label': 'parzelle',
            'value': [
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH567786689869'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '3476'
                    }
                },
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH416823867724'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '6978'
                    }
                }
            ]
        },
        'waldareal': {
            'displayValue': 'ja',
            'hidden': False,
            'label': 'waldareal',
            'value': 'waldareal-ja'
        },
        'zonenplan': {
            'hidden': False,
            'label': 'zonenplan',
            'value': 'Keine Gefahrenzone, Auf Gefahrenzonen nicht untersuchtes Gebiet (orientierend), Landwirtschaftszone, Wald (orientierend)'
        }
    }
}

snapshots['test_gr_client[query9-baugesuch] 1'] = {
    'data': {
        'ausserhalb-bauzone': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'ausserhalb-bauzone',
            'value': 'ausserhalb-bauzone-nein'
        },
        'das-bauvorhaben-befindet-sich-in': {
            'hidden': False,
            'label': 'das-bauvorhaben-befindet-sich-in',
            'value': [
                {
                    'displayValue': 'gewaesserschutzbereich',
                    'value': 'das-bauvorhaben-befindet-sich-in-gewaesserschutzbereich'
                }
            ]
        },
        'gemeinde': {
            'hidden': False,
            'label': 'gemeinde',
            'value': 'Chur'
        },
        'genereller-erschliessungsplan': {
            'hidden': False,
            'label': 'genereller-erschliessungsplan',
            'value': 'Bahnlinie SBB/RhB (hinweisend), Fuss- / Radweg Hauptverbindung, Kantonale Verbindungsstrasse (orientierend), Kantonale Verbindungsstrasse (orientierend), Parkierung Gebiete C'
        },
        'genereller-gestaltungsplan': {
            'hidden': False,
            'label': 'genereller-gestaltungsplan',
            'value': 'Mühlbach überdeckt mit gestalterischem Aufwertungspotential'
        },
        'gis-map': {
            'hidden': True,
            'label': 'gis-map',
            'value': '{"markers": [{"x": 2760376.3950000005, "y": 1190000.739375}], "geometry": "POINT"}'
        },
        'kantonsstrassen': {
            'displayValue': 'ja',
            'hidden': False,
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-ja'
        },
        'ort-grundstueck': {
            'hidden': False,
            'label': 'ort-grundstueck',
            'value': 'Chur'
        },
        'parzelle': {
            'form': 'but-near-attack',
            'hidden': False,
            'label': 'parzelle',
            'value': [
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH946886778137'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '2646'
                    }
                }
            ]
        },
        'street-and-housenumber': {
            'hidden': False,
            'label': 'street-and-housenumber',
            'value': 'Sandstrasse 57, 59'
        },
        'waldareal': {
            'displayValue': 'nein',
            'hidden': False,
            'label': 'waldareal',
            'value': 'waldareal-nein'
        },
        'zonenplan': {
            'hidden': False,
            'label': 'zonenplan',
            'value': 'Keine Gefahrenzone, Wohnzone 3'
        }
    }
}
