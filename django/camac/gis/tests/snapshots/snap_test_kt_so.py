# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_sogis_client[bln-and-ivs-regional-local-coords3] 1'] = {
    'data': {
        'bundesinventare': {
            'label': 'Kay-Uwe Walter',
            'value': 'BLN: Weissenstein, Nr. des BLN: 1010, IVS Regional und Lokal: Hächler - Schitterwald, Nr. des IVS Regional und Lokal: SO 421'
        },
        'gemeinde': {
            'label': 'Suse Junk',
            'value': 'Welschenrohr-Gänsbrunnen'
        },
        'gemeindenummer-bfs': {
            'label': 'Elise Thanel',
            'value': '2430'
        },
        'nutzungsplanung-grundnutzung': {
            'label': 'Tülay Rose',
            'value': 'Wald'
        },
        'nutzungsplanung-weitere-festlegungen': {
            'label': 'Sinaida Söding-Christoph',
            'value': None
        },
        'ort': {
            'label': 'Herr Hans-Rainer Zänker',
            'value': 'Welschenrohr'
        },
        'parzellen': {
            'form': 'those-charge-why',
            'label': 'Elwira Pärtzelt',
            'value': {
                'e-grid': {
                    'label': 'Apostolos Klapp',
                    'value': 'CH607506603227'
                },
                'lagekoordinaten-nord': {
                    'label': 'Ilona Henck B.Eng.',
                    'value': 1235122.657259761
                },
                'lagekoordinaten-ost': {
                    'label': 'Marc Caspar MBA.',
                    'value': 2606265.992581233
                },
                'ort': {
                    'label': 'Herr Hans-Rainer Zänker',
                    'value': 'Welschenrohr'
                },
                'parzellennummer': {
                    'label': 'Univ.Prof. Randolf Oestrovsky B.A.',
                    'value': '685'
                },
                'plz': {
                    'label': None,
                    'value': None
                },
                'strasse-flurname': {
                    'label': 'Muzaffer Reuter',
                    'value': None
                },
                'strasse-nummer': {
                    'label': 'Ing. Monique Hoffmann MBA.',
                    'value': None
                }
            }
        },
        'richtplan-grundnutzung': {
            'label': 'Traugott Kaul',
            'value': 'Wald'
        },
        'richtplan-weiteres': {
            'label': 'Ing. Helen Jungfer',
            'value': 'Linie: Historischer_Verkehrsweg, Waldnähe (aus Richtplan): Ja, Fläche: Juraschutzzone, Fläche: Naturpark, Fläche: BLN_Gebiet'
        },
        'strasse-flurname': {
            'label': 'Muzaffer Reuter',
            'value': None
        },
        'strasse-nummer': {
            'label': 'Ing. Monique Hoffmann MBA.',
            'value': None
        },
        'weitere-gis-informationen': {
            'label': 'Rainer van der Dussen',
            'value': 'Bodenbedeckung: geschlossener_Wald'
        }
    }
}

snapshots['test_sogis_client[crop-rotation-area-coords6] 1'] = {
    'data': {
        'bundesinventare': {
            'label': 'Kay-Uwe Walter',
            'value': None
        },
        'gemeinde': {
            'label': 'Suse Junk',
            'value': 'Lüsslingen-Nennigkofen'
        },
        'gemeindenummer-bfs': {
            'label': 'Elise Thanel',
            'value': '2464'
        },
        'nutzungsplanung-grundnutzung': {
            'label': 'Tülay Rose',
            'value': 'Landwirtschaftszone'
        },
        'nutzungsplanung-weitere-festlegungen': {
            'label': 'Sinaida Söding-Christoph',
            'value': 'Fläche: Kommunale Schutzzone Wildtierkorridor'
        },
        'ort': {
            'label': 'Herr Hans-Rainer Zänker',
            'value': 'Lüsslingen'
        },
        'parzellen': {
            'form': 'those-charge-why',
            'label': 'Elwira Pärtzelt',
            'value': {
                'e-grid': {
                    'label': 'Apostolos Klapp',
                    'value': 'CH727351320675'
                },
                'lagekoordinaten-nord': {
                    'label': 'Ilona Henck B.Eng.',
                    'value': 1227634.5322569455
                },
                'lagekoordinaten-ost': {
                    'label': 'Marc Caspar MBA.',
                    'value': 2603913.165006131
                },
                'ort': {
                    'label': 'Herr Hans-Rainer Zänker',
                    'value': 'Lüsslingen'
                },
                'parzellennummer': {
                    'label': 'Univ.Prof. Randolf Oestrovsky B.A.',
                    'value': '9'
                },
                'plz': {
                    'label': None,
                    'value': None
                },
                'strasse-flurname': {
                    'label': 'Muzaffer Reuter',
                    'value': None
                },
                'strasse-nummer': {
                    'label': 'Ing. Monique Hoffmann MBA.',
                    'value': None
                }
            }
        },
        'richtplan-grundnutzung': {
            'label': 'Traugott Kaul',
            'value': 'Landwirtschaftsgebiet'
        },
        'richtplan-weiteres': {
            'label': 'Ing. Helen Jungfer',
            'value': 'Waldnähe (aus Richtplan): Nein, Fläche: Fruchtfolgeflaeche, Fläche: Witischutzzone'
        },
        'strasse-flurname': {
            'label': 'Muzaffer Reuter',
            'value': None
        },
        'strasse-nummer': {
            'label': 'Ing. Monique Hoffmann MBA.',
            'value': None
        },
        'weitere-gis-informationen': {
            'label': 'Rainer van der Dussen',
            'value': None
        }
    }
}

snapshots['test_sogis_client[default-coords0] 1'] = {
    'data': {
        'bundesinventare': {
            'label': 'Kay-Uwe Walter',
            'value': None
        },
        'gemeinde': {
            'label': 'Suse Junk',
            'value': 'Solothurn'
        },
        'gemeindenummer-bfs': {
            'label': 'Elise Thanel',
            'value': '2601'
        },
        'nutzungsplanung-grundnutzung': {
            'label': 'Tülay Rose',
            'value': 'Kernzone, offene Bauweise, 3-geschossig AZ max. 1.0'
        },
        'nutzungsplanung-weitere-festlegungen': {
            'label': 'Sinaida Söding-Christoph',
            'value': None
        },
        'ort': {
            'label': 'Herr Hans-Rainer Zänker',
            'value': 'Solothurn'
        },
        'parzellen': {
            'form': 'those-charge-why',
            'label': 'Elwira Pärtzelt',
            'value': {
                'e-grid': {
                    'label': 'Apostolos Klapp',
                    'value': 'CH354732700648'
                },
                'lagekoordinaten-nord': {
                    'label': 'Ilona Henck B.Eng.',
                    'value': 1228434.884375
                },
                'lagekoordinaten-ost': {
                    'label': 'Marc Caspar MBA.',
                    'value': 2607160.642708333
                },
                'ort': {
                    'label': 'Herr Hans-Rainer Zänker',
                    'value': 'Solothurn'
                },
                'parzellennummer': {
                    'label': 'Univ.Prof. Randolf Oestrovsky B.A.',
                    'value': '850'
                },
                'plz': {
                    'label': None,
                    'value': None
                },
                'strasse-flurname': {
                    'label': 'Muzaffer Reuter',
                    'value': None
                },
                'strasse-nummer': {
                    'label': 'Ing. Monique Hoffmann MBA.',
                    'value': None
                }
            }
        },
        'richtplan-grundnutzung': {
            'label': 'Traugott Kaul',
            'value': 'Siedlungsgebiet.Wohnen_oeffentliche_Bauten'
        },
        'richtplan-weiteres': {
            'label': 'Ing. Helen Jungfer',
            'value': 'Waldnähe (aus Richtplan): Nein'
        },
        'strasse-flurname': {
            'label': 'Muzaffer Reuter',
            'value': None
        },
        'strasse-nummer': {
            'label': 'Ing. Monique Hoffmann MBA.',
            'value': None
        },
        'weitere-gis-informationen': {
            'label': 'Rainer van der Dussen',
            'value': None
        }
    }
}

snapshots['test_sogis_client[highway-coords7] 1'] = {
    'data': {
        'bundesinventare': {
            'label': 'Kay-Uwe Walter',
            'value': None
        },
        'gemeinde': {
            'label': 'Suse Junk',
            'value': 'Luterbach'
        },
        'gemeindenummer-bfs': {
            'label': 'Elise Thanel',
            'value': '2527'
        },
        'nutzungsplanung-grundnutzung': {
            'label': 'Tülay Rose',
            'value': None
        },
        'nutzungsplanung-weitere-festlegungen': {
            'label': 'Sinaida Söding-Christoph',
            'value': None
        },
        'ort': {
            'label': 'Herr Hans-Rainer Zänker',
            'value': 'Luterbach'
        },
        'parzellen': {
            'form': 'those-charge-why',
            'label': 'Elwira Pärtzelt',
            'value': {
                'e-grid': {
                    'label': 'Apostolos Klapp',
                    'value': 'CH667932069772'
                },
                'lagekoordinaten-nord': {
                    'label': 'Ilona Henck B.Eng.',
                    'value': 1228741.4541305029
                },
                'lagekoordinaten-ost': {
                    'label': 'Marc Caspar MBA.',
                    'value': 2611103.2977669733
                },
                'ort': {
                    'label': 'Herr Hans-Rainer Zänker',
                    'value': 'Luterbach'
                },
                'parzellennummer': {
                    'label': 'Univ.Prof. Randolf Oestrovsky B.A.',
                    'value': '2501'
                },
                'plz': {
                    'label': None,
                    'value': None
                },
                'strasse-flurname': {
                    'label': 'Muzaffer Reuter',
                    'value': None
                },
                'strasse-nummer': {
                    'label': 'Ing. Monique Hoffmann MBA.',
                    'value': None
                }
            }
        },
        'richtplan-grundnutzung': {
            'label': 'Traugott Kaul',
            'value': 'Nationalstrasse'
        },
        'richtplan-weiteres': {
            'label': 'Ing. Helen Jungfer',
            'value': 'Linie: Nationalstrasse.Strasse, Waldnähe (aus Richtplan): Nein'
        },
        'strasse-flurname': {
            'label': 'Muzaffer Reuter',
            'value': None
        },
        'strasse-nummer': {
            'label': 'Ing. Monique Hoffmann MBA.',
            'value': None
        },
        'weitere-gis-informationen': {
            'label': 'Rainer van der Dussen',
            'value': None
        }
    }
}

snapshots['test_sogis_client[ivs-national-coords4] 1'] = {
    'data': {
        'bundesinventare': {
            'label': 'Kay-Uwe Walter',
            'value': 'IVS National: St. Niklaus - Einsiedelei; Verenaschlucht, Nr. des IVS National: SO 365.0.1'
        },
        'gemeinde': {
            'label': 'Suse Junk',
            'value': 'Rüttenen'
        },
        'gemeindenummer-bfs': {
            'label': 'Elise Thanel',
            'value': '2555'
        },
        'nutzungsplanung-grundnutzung': {
            'label': 'Tülay Rose',
            'value': None
        },
        'nutzungsplanung-weitere-festlegungen': {
            'label': 'Sinaida Söding-Christoph',
            'value': 'Fläche: Perimeter kantonaler Nutzungsplan'
        },
        'ort': {
            'label': 'Herr Hans-Rainer Zänker',
            'value': 'Rüttenen'
        },
        'parzellen': {
            'form': 'those-charge-why',
            'label': 'Elwira Pärtzelt',
            'value': {
                'e-grid': {
                    'label': 'Apostolos Klapp',
                    'value': 'CH810699329948'
                },
                'lagekoordinaten-nord': {
                    'label': 'Ilona Henck B.Eng.',
                    'value': 1230212.5463196996
                },
                'lagekoordinaten-ost': {
                    'label': 'Marc Caspar MBA.',
                    'value': 2607372.235299003
                },
                'ort': {
                    'label': 'Herr Hans-Rainer Zänker',
                    'value': 'Rüttenen'
                },
                'parzellennummer': {
                    'label': 'Univ.Prof. Randolf Oestrovsky B.A.',
                    'value': '90041'
                },
                'plz': {
                    'label': None,
                    'value': None
                },
                'strasse-flurname': {
                    'label': 'Muzaffer Reuter',
                    'value': None
                },
                'strasse-nummer': {
                    'label': 'Ing. Monique Hoffmann MBA.',
                    'value': None
                }
            }
        },
        'richtplan-grundnutzung': {
            'label': 'Traugott Kaul',
            'value': 'Wald'
        },
        'richtplan-weiteres': {
            'label': 'Ing. Helen Jungfer',
            'value': 'Linie: Historischer_Verkehrsweg, Waldnähe (aus Richtplan): Ja, Fläche: kantonales_Naturreservat'
        },
        'strasse-flurname': {
            'label': 'Muzaffer Reuter',
            'value': None
        },
        'strasse-nummer': {
            'label': 'Ing. Monique Hoffmann MBA.',
            'value': None
        },
        'weitere-gis-informationen': {
            'label': 'Rainer van der Dussen',
            'value': 'Denkmalschutz Schutzstufe: geschützt, Denkmalschutzobjekt: Verenaschlucht, Bodenbedeckung: geschlossener_Wald, Denkmalschutz Schutzstufe: geschützt, Denkmalschutzobjekt: Gedenkstein für Amanz Gressly, Bodenbedeckung: fliessendes Gewaesser'
        }
    }
}

snapshots['test_sogis_client[monument-coords5] 1'] = {
    'data': {
        'bundesinventare': {
            'label': 'Kay-Uwe Walter',
            'value': 'IVS Regional und Lokal: Solothurn/Hübeli - Kreuzen - Einsiedelei, Nr. des IVS Regional und Lokal: SO 441'
        },
        'gemeinde': {
            'label': 'Suse Junk',
            'value': 'Rüttenen'
        },
        'gemeindenummer-bfs': {
            'label': 'Elise Thanel',
            'value': '2555'
        },
        'nutzungsplanung-grundnutzung': {
            'label': 'Tülay Rose',
            'value': None
        },
        'nutzungsplanung-weitere-festlegungen': {
            'label': 'Sinaida Söding-Christoph',
            'value': None
        },
        'ort': {
            'label': 'Herr Hans-Rainer Zänker',
            'value': 'Rüttenen'
        },
        'parzellen': {
            'form': 'those-charge-why',
            'label': 'Elwira Pärtzelt',
            'value': {
                'e-grid': {
                    'label': 'Apostolos Klapp',
                    'value': 'CH227060320651'
                },
                'lagekoordinaten-nord': {
                    'label': 'Ilona Henck B.Eng.',
                    'value': 1230171.7275696846
                },
                'lagekoordinaten-ost': {
                    'label': 'Marc Caspar MBA.',
                    'value': 2607376.2625398953
                },
                'ort': {
                    'label': 'Herr Hans-Rainer Zänker',
                    'value': 'Rüttenen'
                },
                'parzellennummer': {
                    'label': 'Univ.Prof. Randolf Oestrovsky B.A.',
                    'value': '99'
                },
                'plz': {
                    'label': None,
                    'value': '4500'
                },
                'strasse-flurname': {
                    'label': 'Muzaffer Reuter',
                    'value': 'Kreuzen'
                },
                'strasse-nummer': {
                    'label': 'Ing. Monique Hoffmann MBA.',
                    'value': '6'
                }
            }
        },
        'richtplan-grundnutzung': {
            'label': 'Traugott Kaul',
            'value': 'Wald'
        },
        'richtplan-weiteres': {
            'label': 'Ing. Helen Jungfer',
            'value': 'Waldnähe (aus Richtplan): Ja'
        },
        'strasse-flurname': {
            'label': 'Muzaffer Reuter',
            'value': 'Kreuzen'
        },
        'strasse-nummer': {
            'label': 'Ing. Monique Hoffmann MBA.',
            'value': '6'
        },
        'weitere-gis-informationen': {
            'label': 'Rainer van der Dussen',
            'value': 'Denkmalschutz Schutzstufe: geschützt, Denkmalschutzobjekt: Sigristenhaus zu Kreuzen, Denkmalschutzobjekt: Verenaschlucht, Bodenbedeckung: geschlossener_Wald'
        }
    }
}

snapshots['test_sogis_client[moor-and-sanctuary-coords2] 1'] = {
    'data': {
        'bundesinventare': {
            'label': 'Kay-Uwe Walter',
            'value': 'Amphibien Ortsfeste Objekte: Grenchner Witi, Wasser- und Zugvogelreservate: Witi (BE,SO), Flachmoore: Altwasser'
        },
        'gemeinde': {
            'label': 'Suse Junk',
            'value': 'Grenchen'
        },
        'gemeindenummer-bfs': {
            'label': 'Elise Thanel',
            'value': '2546'
        },
        'nutzungsplanung-grundnutzung': {
            'label': 'Tülay Rose',
            'value': 'Landwirtschaftszone'
        },
        'nutzungsplanung-weitere-festlegungen': {
            'label': 'Sinaida Söding-Christoph',
            'value': None
        },
        'ort': {
            'label': 'Herr Hans-Rainer Zänker',
            'value': 'Grenchen'
        },
        'parzellen': {
            'form': 'those-charge-why',
            'label': 'Elwira Pärtzelt',
            'value': {
                'e-grid': {
                    'label': 'Apostolos Klapp',
                    'value': 'CH470673043283'
                },
                'lagekoordinaten-nord': {
                    'label': 'Ilona Henck B.Eng.',
                    'value': 1223872.4541323201
                },
                'lagekoordinaten-ost': {
                    'label': 'Marc Caspar MBA.',
                    'value': 2595908.1098607033
                },
                'ort': {
                    'label': 'Herr Hans-Rainer Zänker',
                    'value': 'Grenchen'
                },
                'parzellennummer': {
                    'label': 'Univ.Prof. Randolf Oestrovsky B.A.',
                    'value': '5'
                },
                'plz': {
                    'label': None,
                    'value': None
                },
                'strasse-flurname': {
                    'label': 'Muzaffer Reuter',
                    'value': None
                },
                'strasse-nummer': {
                    'label': 'Ing. Monique Hoffmann MBA.',
                    'value': None
                }
            }
        },
        'richtplan-grundnutzung': {
            'label': 'Traugott Kaul',
            'value': 'Landwirtschaftsgebiet'
        },
        'richtplan-weiteres': {
            'label': 'Ing. Helen Jungfer',
            'value': 'Waldnähe (aus Richtplan): Nein, Fläche: kantonales_Naturreservat, Fläche: kantonale_Uferschutzzone, Fläche: Witischutzzone'
        },
        'strasse-flurname': {
            'label': 'Muzaffer Reuter',
            'value': None
        },
        'strasse-nummer': {
            'label': 'Ing. Monique Hoffmann MBA.',
            'value': None
        },
        'weitere-gis-informationen': {
            'label': 'Rainer van der Dussen',
            'value': None
        }
    }
}

snapshots['test_sogis_client[near-forest-coords1] 1'] = {
    'data': {
        'bundesinventare': {
            'label': 'Kay-Uwe Walter',
            'value': None
        },
        'gemeinde': {
            'label': 'Suse Junk',
            'value': 'Langendorf'
        },
        'gemeindenummer-bfs': {
            'label': 'Elise Thanel',
            'value': '2550'
        },
        'nutzungsplanung-grundnutzung': {
            'label': 'Tülay Rose',
            'value': 'Landwirtschaftszone'
        },
        'nutzungsplanung-weitere-festlegungen': {
            'label': 'Sinaida Söding-Christoph',
            'value': 'Grundwasserschutz: S2, Fläche: kommunale Landschaftsschutzzone'
        },
        'ort': {
            'label': 'Herr Hans-Rainer Zänker',
            'value': 'Langendorf'
        },
        'parzellen': {
            'form': 'those-charge-why',
            'label': 'Elwira Pärtzelt',
            'value': {
                'e-grid': {
                    'label': 'Apostolos Klapp',
                    'value': 'CH640632711258'
                },
                'lagekoordinaten-nord': {
                    'label': 'Ilona Henck B.Eng.',
                    'value': 1230671.22757022
                },
                'lagekoordinaten-ost': {
                    'label': 'Marc Caspar MBA.',
                    'value': 2606261.686890635
                },
                'ort': {
                    'label': 'Herr Hans-Rainer Zänker',
                    'value': 'Langendorf'
                },
                'parzellennummer': {
                    'label': 'Univ.Prof. Randolf Oestrovsky B.A.',
                    'value': '298'
                },
                'plz': {
                    'label': None,
                    'value': None
                },
                'strasse-flurname': {
                    'label': 'Muzaffer Reuter',
                    'value': None
                },
                'strasse-nummer': {
                    'label': 'Ing. Monique Hoffmann MBA.',
                    'value': None
                }
            }
        },
        'richtplan-grundnutzung': {
            'label': 'Traugott Kaul',
            'value': 'Landwirtschaftsgebiet'
        },
        'richtplan-weiteres': {
            'label': 'Ing. Helen Jungfer',
            'value': 'Waldnähe (aus Richtplan): Ja, Fläche: Grundwasserschutzzone_areal'
        },
        'strasse-flurname': {
            'label': 'Muzaffer Reuter',
            'value': None
        },
        'strasse-nummer': {
            'label': 'Ing. Monique Hoffmann MBA.',
            'value': None
        },
        'weitere-gis-informationen': {
            'label': 'Rainer van der Dussen',
            'value': 'Bodenbedeckung: geschlossener_Wald'
        }
    }
}

snapshots['test_sogis_client_errors[so_unknown_layer_data_source-200] 1'] = {
    'data': {
    },
    'errors': [
        {
            'client': 'camac.gis.clients.sogis.SoGisClient',
            'data_source_id': '49992886-4602-4eb3-8499-ebeb58c9f17d',
            'detail': 'Fehler 404 beim Abrufen der Daten von der geo.so.ch Schnittstelle'
        }
    ]
}

snapshots['test_sogis_client_errors[so_unknown_property_data_source-200] 1'] = {
    'data': {
        'gemeinde': {
            'label': 'Suse Junk',
            'value': None
        }
    }
}

snapshots['test_sogis_client_errors[so_unknown_question_data_source-200] 1'] = {
    'data': {
        'unknown_question': {
            'label': None,
            'value': 'Solothurn'
        }
    }
}
