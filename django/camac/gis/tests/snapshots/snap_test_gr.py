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
            'value': 'Auf Gefahrenzonen nicht untersuchtes Gebiet, Wald'
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
            'value': 'Keine Gefahrenzone, Auf Gefahrenzonen nicht untersuchtes Gebiet, Landwirtschaftszone, Wald'
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
            'value': 'Bahnlinie SBB/RhB, Fuss- / Radweg Hauptverbindung, Kantonale Verbindungsstrasse, Kantonale Verbindungsstrasse, Parkierung Gebiete C'
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
