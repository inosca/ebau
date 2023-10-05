# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_gr_client[markers0-POINT-baugesuch] 1'] = {
    'data': {
        'ausserhalb-bauzone': {
            'displayValue': 'nein',
            'label': 'ausserhalb-bauzone',
            'value': 'ausserhalb-bauzone-nein'
        },
        'coordinates': {
            'label': None,
            'value': "'2730678.226988568,1122327.0823116319'"
        },
        'das-bauvorhaben-befindet-sich-in': {
            'label': 'das-bauvorhaben-befindet-sich-in',
            'value': [
                {
                    'displayValue': 'gewaesserschutzbereich',
                    'value': 'das-bauvorhaben-befindet-sich-in-gewaesserschutzbereich'
                }
            ]
        },
        'gemeinde': {
            'label': 'gemeinde',
            'value': 'Roveredo (GR)'
        },
        'genereller-gestaltungsplan': {
            'label': 'genereller-gestaltungsplan',
            'value': 'Linea di allineamento per la strutturazione edilizia, Linea di allineamento per la strutturazione edilizia'
        },
        'kantonsstrassen': {
            'displayValue': 'nein',
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-nein'
        },
        'parzelle': {
            'form': 'property-rate',
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
            'label': 'waldareal',
            'value': 'waldareal-nein'
        },
        'zonenplan': {
            'label': 'zonenplan',
            'value': 'Nessuna zona di pericolo, Zona residenziale (i.s. 0.7)'
        }
    }
}

snapshots['test_gr_client[markers1-POINT-bauanzeige] 1'] = {
    'data': {
        'coordinates': {
            'label': None,
            'value': "'2730678.226988568,1122327.0823116319'"
        },
        'gemeinde': {
            'label': 'gemeinde',
            'value': 'Roveredo (GR)'
        },
        'genereller-gestaltungsplan': {
            'label': 'genereller-gestaltungsplan',
            'value': 'Linea di allineamento per la strutturazione edilizia, Linea di allineamento per la strutturazione edilizia'
        },
        'parzelle': {
            'form': 'property-rate',
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
            'label': 'zonenplan',
            'value': 'Nessuna zona di pericolo, Zona residenziale (i.s. 0.7)'
        }
    }
}

snapshots['test_gr_client[markers10-POINT-baugesuch] 1'] = {
    'data': {
        'coordinates': {
            'label': None,
            'value': "'2757771.4499999997,1192182.0312499998'"
        },
        'das-bauvorhaben-befindet-sich-in': {
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
            'label': 'gemeinde',
            'value': 'Chur'
        },
        'genereller-erschliessungsplan': {
            'label': 'genereller-erschliessungsplan',
            'value': 'Skatingweg, Fuss- / Radweg Hauptverbindung'
        },
        'genereller-gestaltungsplan': {
            'label': 'genereller-gestaltungsplan',
            'value': 'Gewässerabstandslinien, Baumreihe, einseitig'
        },
        'kantonsstrassen': {
            'displayValue': 'nein',
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-nein'
        },
        'parzelle': {
            'form': 'property-rate',
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
            'label': 'waldareal',
            'value': 'waldareal-waldabstandsbereich'
        },
        'zonenplan': {
            'label': 'zonenplan',
            'value': 'Statische Waldgrenze gemäss Art. 10/13 Waldgesetz, Statische Waldgrenze gemäss Art. 10/13 Waldgesetz, Gefahrenzone 1, Gewässer'
        }
    }
}

snapshots['test_gr_client[markers2-LINESTRING-baugesuch] 1'] = {
    'data': {
        'ausserhalb-bauzone': {
            'displayValue': 'nein',
            'label': 'ausserhalb-bauzone',
            'value': 'ausserhalb-bauzone-nein'
        },
        'coordinates': {
            'label': None,
            'value': "'2730686.563711087,1122237.578980265', '2730701.779260571,1122223.4682885902'"
        },
        'das-bauvorhaben-befindet-sich-in': {
            'label': 'das-bauvorhaben-befindet-sich-in',
            'value': [
                {
                    'displayValue': 'gewaesserschutzbereich',
                    'value': 'das-bauvorhaben-befindet-sich-in-gewaesserschutzbereich'
                }
            ]
        },
        'gemeinde': {
            'label': 'gemeinde',
            'value': 'Roveredo (GR)'
        },
        'genereller-erschliessungsplan': {
            'label': 'genereller-erschliessungsplan',
            'value': 'Percorso pedonale, Percorso pedonale'
        },
        'kantonsstrassen': {
            'displayValue': 'nein',
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-nein'
        },
        'parzelle': {
            'form': 'property-rate',
            'label': 'parzelle',
            'value': [
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH479178647641'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '921'
                    }
                },
                {
                    'e-grid-nr': {
                        'label': 'e-grid-nr',
                        'value': 'CH356476789154'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '920'
                    }
                }
            ]
        },
        'street-and-housenumber': {
            'label': 'street-and-housenumber',
            'value': "Sant'Antoni 11, 13, 17"
        },
        'waldareal': {
            'displayValue': 'nein',
            'label': 'waldareal',
            'value': 'waldareal-nein'
        },
        'zonenplan': {
            'label': 'zonenplan',
            'value': 'Nessuna zona di pericolo, Zona nucleo di nuova formazione'
        }
    }
}

snapshots['test_gr_client[markers3-POLYGON-baugesuch] 1'] = {
    'data': {
        'ausserhalb-bauzone': {
            'displayValue': 'nein',
            'label': 'ausserhalb-bauzone',
            'value': 'ausserhalb-bauzone-nein'
        },
        'coordinates': {
            'label': None,
            'value': "'2758821.8885866464,1191884.7759206274', '2758835.689140816,1191889.2217609326', '2758844.747878619,1191856.4200200567', '2758832.507804883,1191854.8711072344'"
        },
        'das-bauvorhaben-befindet-sich-in': {
            'label': 'das-bauvorhaben-befindet-sich-in',
            'value': [
                {
                    'displayValue': 'gewaesserschutzbereich',
                    'value': 'das-bauvorhaben-befindet-sich-in-gewaesserschutzbereich'
                }
            ]
        },
        'folgeplanung': {
            'label': 'folgeplanung',
            'value': 'Baulinie allgemein'
        },
        'gemeinde': {
            'label': 'gemeinde',
            'value': 'Chur'
        },
        'genereller-erschliessungsplan': {
            'label': 'genereller-erschliessungsplan',
            'value': 'Fuss- / Radweg Hauptverbindung, Sammelstrasse, Parkierung Gebiete B'
        },
        'genereller-gestaltungsplan': {
            'label': 'genereller-gestaltungsplan',
            'value': 'Baumreihe, einseitig'
        },
        'kantonsstrassen': {
            'displayValue': 'nein',
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-nein'
        },
        'parzelle': {
            'form': 'property-rate',
            'label': 'parzelle',
            'value': [
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
                        'value': 'CH898677006887'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '4625'
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
                        'value': 'CH880086687762'
                    },
                    'liegenschaftsnummer': {
                        'label': 'liegenschaftsnummer',
                        'value': '4624'
                    }
                }
            ]
        },
        'street-and-housenumber': {
            'label': 'street-and-housenumber',
            'value': 'Scalettastrasse; Alpsteinweg 2'
        },
        'waldareal': {
            'displayValue': 'nein',
            'label': 'waldareal',
            'value': 'waldareal-nein'
        },
        'zonenplan': {
            'label': 'zonenplan',
            'value': 'Keine Gefahrenzone, Wohnzone 2'
        }
    }
}

snapshots['test_gr_client[markers4-POINT-baugesuch] 1'] = {
    'data': {
        'ausserhalb-bauzone': {
            'displayValue': 'nein',
            'label': 'ausserhalb-bauzone',
            'value': 'ausserhalb-bauzone-nein'
        },
        'coordinates': {
            'label': None,
            'value': "'2731195.9499999997,1122174.3312499998'"
        },
        'das-bauvorhaben-befindet-sich-in': {
            'label': 'das-bauvorhaben-befindet-sich-in',
            'value': [
                {
                    'displayValue': 'gewaesserschutzbereich',
                    'value': 'das-bauvorhaben-befindet-sich-in-gewaesserschutzbereich'
                }
            ]
        },
        'gemeinde': {
            'label': 'gemeinde',
            'value': 'Roveredo (GR)'
        },
        'kantonsstrassen': {
            'displayValue': 'nein',
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-nein'
        },
        'parzelle': {
            'form': 'property-rate',
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
            'label': 'street-and-housenumber',
            'value': 'Véra 10, 12'
        },
        'waldareal': {
            'displayValue': 'nein',
            'label': 'waldareal',
            'value': 'waldareal-nein'
        },
        'zonenplan': {
            'label': 'zonenplan',
            'value': 'Nessuna zona di pericolo, Zona per edifici pubblici (GdS III)'
        }
    }
}

snapshots['test_gr_client[markers5-POINT-baugesuch] 1'] = {
    'data': {
        'ausserhalb-bauzone': {
            'displayValue': 'ja',
            'label': 'ausserhalb-bauzone',
            'value': 'ausserhalb-bauzone-ja'
        },
        'coordinates': {
            'label': None,
            'value': "'2758622.7126099495,1190131.3069476'"
        },
        'gemeinde': {
            'label': 'gemeinde',
            'value': 'Chur'
        },
        'kantonsstrassen': {
            'displayValue': 'nein',
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-nein'
        },
        'parzelle': {
            'form': 'property-rate',
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
            'label': 'waldareal',
            'value': 'waldareal-ja'
        },
        'zonenplan': {
            'label': 'zonenplan',
            'value': 'Auf Gefahrenzonen nicht untersuchtes Gebiet(orientierend), Wald(orientierend)'
        }
    }
}

snapshots['test_gr_client[markers6-POINT-baugesuch] 1'] = {
    'data': {
        'ausserhalb-bauzone': {
            'displayValue': 'ja',
            'label': 'ausserhalb-bauzone',
            'value': 'ausserhalb-bauzone-ja'
        },
        'coordinates': {
            'label': None,
            'value': "'2760943.8499999996,1192035.0312499998'"
        },
        'gemeinde': {
            'label': 'gemeinde',
            'value': 'Chur'
        },
        'kantonsstrassen': {
            'displayValue': 'nein',
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-nein'
        },
        'parzelle': {
            'form': 'property-rate',
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
            'label': 'waldareal',
            'value': 'waldareal-waldabstandsbereich'
        },
        'zonenplan': {
            'label': 'zonenplan',
            'value': 'Keine Gefahrenzone, Landwirtschaftszone'
        }
    }
}

snapshots['test_gr_client[markers7-LINESTRING-baugesuch] 1'] = {
    'data': {
        'ausserhalb-bauzone': {
            'displayValue': 'ja',
            'label': 'ausserhalb-bauzone',
            'value': 'ausserhalb-bauzone-ja'
        },
        'coordinates': {
            'label': None,
            'value': "'2760930.5289222472,1192035.707010256', '2760963.900865463,1192057.817393839'"
        },
        'gemeinde': {
            'label': 'gemeinde',
            'value': 'Chur'
        },
        'kantonsstrassen': {
            'displayValue': 'nein',
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-nein'
        },
        'parzelle': {
            'form': 'property-rate',
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
            'label': 'waldareal',
            'value': 'waldareal-ja'
        },
        'zonenplan': {
            'label': 'zonenplan',
            'value': 'Keine Gefahrenzone, Auf Gefahrenzonen nicht untersuchtes Gebiet(orientierend), Landwirtschaftszone, Wald(orientierend)'
        }
    }
}

snapshots['test_gr_client[markers8-POINT-baugesuch] 1'] = {
    'data': {
        'ausserhalb-bauzone': {
            'displayValue': 'nein',
            'label': 'ausserhalb-bauzone',
            'value': 'ausserhalb-bauzone-nein'
        },
        'coordinates': {
            'label': None,
            'value': "'2760376.3950000005,1190000.739375'"
        },
        'das-bauvorhaben-befindet-sich-in': {
            'label': 'das-bauvorhaben-befindet-sich-in',
            'value': [
                {
                    'displayValue': 'gewaesserschutzbereich',
                    'value': 'das-bauvorhaben-befindet-sich-in-gewaesserschutzbereich'
                }
            ]
        },
        'gemeinde': {
            'label': 'gemeinde',
            'value': 'Chur'
        },
        'genereller-erschliessungsplan': {
            'label': 'genereller-erschliessungsplan',
            'value': 'Bahnlinie SBB/RhB(hinweisend), Fuss- / Radweg Hauptverbindung, Kantonale Verbindungsstrasse(orientierend), Kantonale Verbindungsstrasse(orientierend), Parkierung Gebiete C'
        },
        'genereller-gestaltungsplan': {
            'label': 'genereller-gestaltungsplan',
            'value': 'Mühlbach überdeckt mit gestalterischem Aufwertungspotential'
        },
        'kantonsstrassen': {
            'displayValue': 'ja',
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-ja'
        },
        'parzelle': {
            'form': 'property-rate',
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
            'label': 'street-and-housenumber',
            'value': 'Sandstrasse 57, 59'
        },
        'waldareal': {
            'displayValue': 'nein',
            'label': 'waldareal',
            'value': 'waldareal-nein'
        },
        'zonenplan': {
            'label': 'zonenplan',
            'value': 'Keine Gefahrenzone, Wohnzone 3'
        }
    }
}

snapshots['test_gr_client[markers9-POINT-baugesuch] 1'] = {
    'data': {
        'coordinates': {
            'label': None,
            'value': "'2757567.75,1192209.3312499998'"
        },
        'das-bauvorhaben-befindet-sich-in': {
            'label': 'das-bauvorhaben-befindet-sich-in',
            'value': [
                {
                    'displayValue': 'gewaesserschutzbereich',
                    'value': 'das-bauvorhaben-befindet-sich-in-gewaesserschutzbereich'
                }
            ]
        },
        'gemeinde': {
            'label': 'gemeinde',
            'value': 'Chur'
        },
        'kantonsstrassen': {
            'displayValue': 'nein',
            'label': 'kantonsstrassen',
            'value': 'kantonsstrassen-nein'
        },
        'parzelle': {
            'form': 'property-rate',
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
            'label': 'waldareal',
            'value': 'waldareal-nein'
        },
        'zonenplan': {
            'label': 'zonenplan',
            'value': 'Gewässerraumzone, Keine Gefahrenzone, Zone übriges Gemeindegebiet (Gewässer)'
        }
    }
}
