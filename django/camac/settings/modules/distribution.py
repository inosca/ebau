from datetime import timedelta

from django.utils.translation import gettext_lazy as _

from camac.utils import (
    has_permission_for_inquiry_answer_document,
    has_permission_for_inquiry_document,
    is_lead_role,
)

"""
WARNING: Any key that is either "TASK or ends with "_TASK" will be picked up by the visibilty filter for work items (see django/camac/extensions/visibilities.py).
"""
DISTRIBUTION = {
    "default": {
        "DEFAULT_DEADLINE_LEAD_TIME": 30,  # 30 days, needs to be the same as configured in the frontend
        "DISTRIBUTION_WORKFLOW": "distribution",
        "DISTRIBUTION_TASK": "distribution",
        "DISTRIBUTION_INIT_TASK": "init-distribution",
        "DISTRIBUTION_COMPLETE_TASK": "complete-distribution",
        "DISTRIBUTION_CHECK_TASK": "check-distribution",
        "INQUIRY_TASK": "inquiry",
        "INQUIRY_FORM": "inquiry",
        "INQUIRY_CREATE_TASK": "create-inquiry",
        "INQUIRY_CHECK_TASK": "check-inquiries",
        "INQUIRY_REDO_TASK": "redo-inquiry",
        "INQUIRY_WORKFLOW": "inquiry",
        "INQUIRY_ANSWER_FORM": "inquiry-answer",
        "INQUIRY_ANSWER_FILL_TASK": "fill-inquiry",
        "HISTORY": {},
        "REDO_INQUIRY": {},
        "REDO_DISTRIBUTION": {},
        "QUESTIONS": {
            "DEADLINE": "inquiry-deadline",
            "REMARK": "inquiry-remark",
            "STATUS": "inquiry-answer-status",
        },
        "ANSWERS": {},
        "NOTIFICATIONS": {},
        # For the suggestions services ids or slugs can be used but they shouldn't be mixed.
        "SUGGESTIONS": [],
        "DEFAULT_SUGGESTIONS": [],
        "PERMISSIONS": {
            "CompleteWorkItem": {
                "DISTRIBUTION_COMPLETE_TASK": lambda group, *_: is_lead_role(group),
                "DISTRIBUTION_CHECK_TASK": lambda group, *_: is_lead_role(group),
                "INQUIRY_CHECK_TASK": lambda group, *_: is_lead_role(group),
            },
            "ResumeWorkItem": {
                "INQUIRY_TASK": lambda group, *_: is_lead_role(group),
            },
            "CancelWorkItem": {
                "INQUIRY_TASK": lambda group, *_: is_lead_role(group),
            },
            "RedoWorkItem": {
                "DISTRIBUTION_TASK": lambda group, *_: is_lead_role(group),
                "INQUIRY_TASK": lambda group, *_: is_lead_role(group),
            },
            "SaveDocumentAnswer": {
                "INQUIRY_FORM": lambda group, document, *_: is_lead_role(group)
                and has_permission_for_inquiry_document(group, document),
                "INQUIRY_ANSWER_FORM": lambda group,
                document,
                *_: has_permission_for_inquiry_answer_document(group, document),
            },
        },
    },
    "kt_bern": {
        "ENABLED": True,
        "INSTANCE_STATE_DISTRIBUTION": "circulation",
        "HISTORY": {
            "COMPLETE_DISTRIBUTION": _("Circulation completed"),
            "SKIP_DISTRIBUTION": _("Circulation skipped"),
            "REDO_DISTRIBUTION": _("Circulation reopened"),
        },
        "REDO_INQUIRY": {
            "REOPEN_TASKS": ["fill-inquiry"],
        },
        "QUESTIONS": {
            "STATEMENT": "inquiry-answer-statement",
            "ANCILLARY_CLAUSES": "inquiry-answer-ancillary-clauses",
        },
        "ANSWERS": {
            "STATUS": {
                "POSITIVE": "inquiry-answer-status-positive",
                "NEGATIVE": "inquiry-answer-status-negative",
                "NOT_INVOLVED": "inquiry-answer-status-not-involved",
                "CLAIM": "inquiry-answer-status-claim",
                "UNKNOWN": "inquiry-answer-status-unknown",
            },
        },
        "NOTIFICATIONS": {
            "INQUIRY_SENT": {
                "template_slug": "03-verfahrensablauf-fachstelle",
                "recipient_types": ["inquiry_addressed"],
            },
            "INQUIRY_ANSWERED": {
                "template_slug": "05-bericht-erstellt",
                "recipient_types": ["inquiry_controlling"],
            },
        },
        # Service IDs or slugs can be used for the suggestions but they shouldn't be mixed.
        "SUGGESTIONS": {
            "FORM": {
                "heat-generator": [20046],
                "heat-generator-v2": [20046],
            },
            "QUESTIONS": {
                (
                    "art-versickerung-dach",
                    "art-versickerung-dach-oberflaechengewaesser",
                ): [20063],
                (
                    "art-versickerung-platz",
                    "art-versickerung-platz-oberflachengewasser",
                ): [20063],
                (
                    "art-versickerung-dach-v2",
                    "art-versickerung-dach-v2-oberflaechengewaesser",
                ): [20063],
                (
                    "art-versickerung-platz-v2",
                    "art-versickerung-platz-v2-oberflaechengewaesser",
                ): [20063],
                (
                    "ausnahme-im-sinne-von-artikel-64-kenv",
                    "ausnahme-im-sinne-von-artikel-64-kenv-ja",
                ): [20046],
                (
                    "aussenlaerm",
                    "aussenlaerm-ja",
                ): [20054],
                (
                    "bau-im-wald-oder-innerhalb-von-30-m-abstand",
                    "bau-im-wald-oder-innerhalb-von-30-m-abstand-ja",
                ): [20048],
                (
                    "baubeschrieb",
                    "baubeschrieb-erweiterung-anbau",
                ): [20068, 20055],
                (
                    "baubeschrieb",
                    "baubeschrieb-neubau",
                ): [20055],
                (
                    "baubeschrieb",
                    "baubeschrieb-technische-anlage",
                ): [20055],
                (
                    "baubeschrieb",
                    "baubeschrieb-tiefbauanlage",
                ): [20068],
                (
                    "baubeschrieb",
                    "baubeschrieb-um-ausbau",
                ): [20055, 20068],
                (
                    "baubeschrieb",
                    "baubeschrieb-umnutzung",
                ): [20055],
                (
                    "baugruppe-bauinventar",
                    "baugruppe-bauinventar-ja",
                ): [20043],
                (
                    "bauten-oder-pfaehlen-im-grundwasser",
                    "bauten-oder-pfaehlen-im-grundwasser-ja",
                ): [20050],
                (
                    "belasteter-standort",
                    "belasteter-standort-ja",
                ): [20050],
                (
                    "besondere-brandrisiken",
                    "besondere-brandrisiken-ja",
                ): [20057],
                (
                    "brandbelastung",
                    "brandbelastung-ja",
                ): [20057],
                (
                    "eigenstaendiger-grossverbraucher",
                    "eigenstaendiger-grossverbraucher-ja",
                ): [20046],
                (
                    "erhaltenswert",
                    "erhaltenswert-ja",
                ): [20043],
                (
                    "feuerungsanlagen",
                    "feuerungsanlagen-holzfeuerungen",
                ): [20057],
                (
                    "feuerungsanlagen",
                    "feuerungsanlagen-ol-oder-gasfeuerungen-350-kw",
                ): [20057],
                (
                    "feuerungsanlagen",
                    "feuerungsanlagen-pellet-schnitzelfeuerungsanlage",
                ): [20055, 20054, 20057],
                (
                    "gebiet-mit-archaeologischen-objekten",
                    "gebiet-mit-archaeologischen-objekten-ja",
                ): [20043],
                (
                    "gebiet-mit-naturgefahren",
                    "gebiet-mit-naturgefahren-ja",
                ): [20049],
                (
                    "gefahrenstufe",
                    "gefahrenstufe-blau",
                ): [20049],
                (
                    "gefahrenstufe",
                    "gefahrenstufe-rot",
                ): [20049],
                (
                    "gefahrenstufe",
                    "gefahrenstufe-unbestimmt",
                ): [20049],
                (
                    "gefaehrliche-stoffe",
                    "gefaehrliche-stoffe-ja",
                ): [20055],
                (
                    "geplante-anlagen",
                    "geplante-anlagen-solar-oder-photovoltaik-anlage",
                ): [20054],
                (
                    "grundwasserschutzzonen",
                    "grundwasserschutzzonen-s1",
                ): [20050],
                (
                    "grundwasserschutzzonen",
                    "grundwasserschutzzonen-s2sh",
                ): [20050],
                (
                    "grundwasserschutzzonen",
                    "grundwasserschutzzonen-s3sm",
                ): [20050],
                (
                    "grundwasserschutzzonen-v2",
                    "grundwasserschutzzonen-v2-s1",
                ): [20050],
                (
                    "grundwasserschutzzonen-v2",
                    "grundwasserschutzzonen-v2-s2",
                ): [20050],
                (
                    "grundwasserschutzzonen-v2",
                    "grundwasserschutzzonen-v2-s3-s3zu",
                ): [20050],
                (
                    "grundwasserschutzzonen-v2",
                    "grundwasserschutzzonen-v2-sa",
                ): [20050],
                (
                    "grundwasserschutzzonen-v2",
                    "grundwasserschutzzonen-v2-sbw",
                ): [20050],
                (
                    "grundwasserschutzzonen-v2",
                    "grundwasserschutzzonen-v2-sh",
                ): [20050],
                (
                    "grundwasserschutzzonen-v2",
                    "grundwasserschutzzonen-v2-sm",
                ): [20050],
                (
                    "ist-das-vorhaben-energierelevant",
                    "ist-das-vorhaben-energierelevant-ja",
                ): [20046],
                (
                    "ist-durch-das-bauvorhaben-boden-betroffen",
                    "ist-durch-das-bauvorhaben-boden-betroffen-ja",
                ): [20050],
                (
                    "ist-durch-das-bauvorhaben-boden-ober-unterboden-betroffen-v2",
                    "ist-durch-das-bauvorhaben-boden-ober-unterboden-betroffen-v2-ja",
                ): [20050],
                (
                    "ist-mit-bauabfaellen-zu-rechnen",
                    "ist-mit-bauabfaellen-zu-rechnen-ja",
                ): [20050],
                (
                    "k-objekt",
                    "k-objekt-ja",
                ): [20043],
                (
                    "klassierung-der-taetigkeit",
                    "klassierung-der-taetigkeit-klasse-3",
                ): [20055],
                (
                    "klassierung-der-taetigkeit",
                    "klassierung-der-taetigkeit-klasse-4",
                ): [20055],
                (
                    "maschinelle-arbeitsmittel",
                    "maschinelle-arbeitsmittel-ja",
                ): [20055],
                (
                    "maschinen-aus-den-folgenden-kategorien",
                    "maschinen-aus-den-folgenden-kategorien-erzeugung",
                ): [20055],
                (
                    "maschinen-aus-den-folgenden-kategorien",
                    "maschinen-aus-den-folgenden-kategorien-reinigung",
                ): [20055],
                (
                    "maschinen-aus-den-folgenden-kategorien",
                    "maschinen-aus-den-folgenden-kategorien-strom",
                ): [20055],
                (
                    "maschinen-aus-den-folgenden-kategorien",
                    "maschinen-aus-den-folgenden-kategorien-transport",
                ): [20055],
                (
                    "maschinen-aus-den-folgenden-kategorien",
                    "maschinen-aus-den-folgenden-kategorien-werkhoefe",
                ): [20055],
                (
                    "naturschutz",
                    "naturschutz-ja",
                ): [20065],
                (
                    "nutzungsart",
                    "nutzungsart-andere",
                ): [20054, 20055],
                (
                    "nutzungsart",
                    "nutzungsart-dienstleistung",
                ): [20054, 20055],
                (
                    "nutzungsart",
                    "nutzungsart-gastgewerbe",
                ): [20054, 20055],
                (
                    "nutzungsart",
                    "nutzungsart-gewerbe",
                ): [20054, 20055, 20074],
                (
                    "nutzungsart",
                    "nutzungsart-industrie",
                ): [20054, 20055, 20074],
                (
                    "nutzungsart",
                    "nutzungsart-lager",
                ): [20054, 20055],
                (
                    "nutzungsart",
                    "nutzungsart-landwirtschaft",
                ): [20054, 20055, 20074],
                (
                    "nutzungsart",
                    "nutzungsart-verkauf",
                ): [20054, 20055],
                (
                    "organismen-in-anlage",
                    "organismen-in-anlage-andere",
                ): [20055],
                (
                    "organismen-in-anlage",
                    "organismen-in-anlage-bakterien",
                ): [20055],
                (
                    "organismen-in-anlage",
                    "organismen-in-anlage-viren",
                ): [20055],
                (
                    "rrb",
                    "rrb-ja",
                ): [20043],
                (
                    "schuetzenswert",
                    "schuetzenswert-ja",
                ): [20043],
                (
                    "sind-belange-des-gewasserschutzes-betroffen",
                    "sind-belange-des-gewasserschutzes-betroffen-ja",
                ): [20050],
                (
                    "sind-belange-des-gewaesserschutzes-betroffen-v2",
                    "sind-belange-des-gewaesserschutzes-betroffen-v2-ja",
                ): [20050],
                (
                    "versickerung",
                    "versickerung-nein",
                ): [20063],
                (
                    "versickerung-v2",
                    "versickerung-v2-nein",
                ): [20063],
                (
                    "verunreinigte-abluft",
                    "verunreinigte-abluft-ja",
                ): [20054],
                (
                    "verwendungszweck-der-anlage",
                    "verwendungszweck-der-anlage-andere",
                ): [20055],
                (
                    "verwendungszweck-der-anlage",
                    "verwendungszweck-der-anlage-diagnostik",
                ): [20055],
                (
                    "verwendungszweck-der-anlage",
                    "verwendungszweck-der-anlage-forschung",
                ): [20055],
                (
                    "verwendungszweck-der-anlage",
                    "verwendungszweck-der-anlage-gewaechshaus",
                ): [20055],
                (
                    "verwendungszweck-der-anlage",
                    "verwendungszweck-der-anlage-produktion",
                ): [20055],
                (
                    "verwendungszweck-der-anlage",
                    "verwendungszweck-der-anlage-tieranlage",
                ): [20055],
                (
                    "verwendungszweck-der-anlage",
                    "verwendungszweck-der-anlage-unterricht",
                ): [20055],
                (
                    "was-fuer-ein-vorhaben",
                    "was-fuer-ein-vorhaben-andere",
                ): [20055],
                (
                    "was-fuer-ein-vorhaben",
                    "was-fuer-ein-vorhaben-grossraumbueros",
                ): [20055],
                (
                    "was-fuer-ein-vorhaben",
                    "was-fuer-ein-vorhaben-spitaeler",
                ): [20055],
                (
                    "was-fuer-ein-vorhaben",
                    "was-fuer-ein-vorhaben-verkaufsgeschaefte",
                ): [20055],
                (
                    "wassergefaehrdende-explosive-stoffe",
                    "wassergefaehrdende-explosive-stoffe-ja",
                ): [20050],
                (
                    "welche-art-vorhaben",
                    "welche-art-vorhaben-erstellung-aussenraum",
                ): [20068],
                (
                    "welche-art-vorhaben",
                    "welche-art-vorhaben-fischhaltung-aquakulturanlage",
                ): [20050, 20051, 20052, 20053, 20063],
                (
                    "welche-waermepumpen",
                    "welche-waermepumpen-boden-untergrund",
                ): [20053],
                (
                    "welche-waermepumpen",
                    "welche-waermepumpen-luft",
                ): [20054],
                (
                    "welche-waermepumpen",
                    "welche-waermepumpen-wasser",
                ): [20053, 20063],
                (
                    "werden-brandschutzabstaende-unterschritten",
                    "werden-brandschutzabstande-unterschritten-ja",
                ): [20057],
                (
                    "werden-siloanlagen-erstellt",
                    "werden-siloanlagen-erstellt-ja",
                ): [20055],
                (
                    "wildtierschutz",
                    "wildtierschutz-ja",
                ): [20064],
                (
                    "gesuchstyp",
                    "gesuchstyp-baum",
                ): [20065],
                (
                    "gesuchstyp",
                    "gesuchstyp-hecke-feldgehoelz",
                ): [20065],
                (
                    "handelt-es-sich-um-ein-sensibles-objekt",
                    "handelt-es-sich-um-ein-sensibles-objekt-ja",
                ): [20075, 20076, 20077, 20078],
                (
                    "sv-betrieb-neu-oder-bestehend-v3",
                    "sv-betrieb-neu-oder-bestehend-v3-neu",
                ): [20060],
                (
                    "sv-kurzbericht-risikoermittlung-v3",
                    "sv-kurzbericht-risikoermittlung-v3-nein",
                ): [20060],
                (
                    "sv-relevanz-gueltigkeit-v3",
                    "sv-relevanz-gueltigkeit-v3-trifft-nicht-zu",
                ): [20060],
                (
                    "triagefrage-biologische-sicherheit-v3",
                    "triagefrage-biologische-sicherheit-v3-ja",
                ): [20060],
            },
        },
        "PERMISSIONS": {
            "CompleteWorkItem": {
                "INQUIRY_ANSWER_FILL_TASK": lambda group, *_: is_lead_role(group),
            },
        },
    },
    "kt_schwyz": {
        "ENABLED": True,
        "INSTANCE_STATE_DISTRIBUTION": "circ",
        "INQUIRY_ANSWER_CHECK_TASK": "check-inquiry",
        "INQUIRY_ANSWER_REVISE_TASK": "revise-inquiry",
        "INQUIRY_ANSWER_ALTER_TASK": "alter-inquiry",
        "HISTORY": {
            "COMPLETE_DISTRIBUTION": "Zirkulationsentscheid gestartet",
            "SKIP_DISTRIBUTION": "Zirkulationsentscheid gestartet",
        },
        "REDO_INQUIRY": {
            "REOPEN_TASKS": ["check-inquiry", "revise-inquiry"],
            "COMPLETE_TASKS": ["revise-inquiry"],
        },
        "REDO_DISTRIBUTION": {
            "CREATE_TASKS": ["additional-demand"],
        },
        "QUESTIONS": {
            "REQUEST": "inquiry-answer-request",
            "ANCILLARY_CLAUSES": "inquiry-answer-ancillary-clauses",
            "REASON": "inquiry-answer-reason",
            "RECOMMENDATION": "inquiry-answer-recommendation",
            "HINT": "inquiry-answer-hint",
        },
        "DEFAULT_SUGGESTIONS": [7],  # Baugesuchszentrale
        # Service IDs or slugs can be used for the suggestions but they shouldn't be mixed.
        "SUGGESTIONS": {
            "SUBMODULES": [
                ("fachthemen.landwirtschaft", [9]),
                ("fachthemen.wald", [15]),
                ("fachthemen.naturgefahren", [15]),
                ("fachthemen.arbeitssicherheit-und-gesundheitsschutz", [4]),
                ("fachthemen.zivilschutz", [79]),
                ("fachthemen.zivilschutz-v2", [79]),
                ("fachthemen.gewasserschutz", [267, 13]),
                ("fachthemen.reklamen", [18]),
                ("fachthemen.denkmalschutz-und-archaeologie", [8]),
                ("fachthemen.fischerei", [267]),
            ],
            "QUESTIONS": [
                (
                    "'Ja' in 'lebensmittel-umgehen'|value || 'Ja' in 'offentlich-duschanlage-oder-bad'|value",
                    [22],
                )
            ],
        },
        "NOTIFICATIONS": {
            "INQUIRY_SENT": {
                "template_slug": "einladung-zur-stellungnahme",
                "recipient_types": ["inquiry_addressed"],
            },
        },
        "PERMISSIONS": {
            "CompleteWorkItem": {
                "INQUIRY_CREATE_TASK": lambda group, *_: is_lead_role(group),
                "INQUIRY_ANSWER_CHECK_TASK": lambda group, *_: is_lead_role(group),
                "INQUIRY_ANSWER_REVISE_TASK": lambda group, *_: is_lead_role(group),
            },
        },
        "SYNC_INQUIRY_DEADLINE_TO_ANSWER_TASKS": {
            "fill-inquiry": {
                "TIME_DELTA": timedelta(days=-3)  # check-inquiry lead-time
            }
        },
    },
    "kt_gr": {
        "ENABLED": True,
        "INSTANCE_STATE_DISTRIBUTION": "circulation",
        "HISTORY": {
            "COMPLETE_DISTRIBUTION": _("Circulation completed"),
            "SKIP_DISTRIBUTION": _("Circulation skipped"),
            "REDO_DISTRIBUTION": _("Circulation reopened"),
        },
        "REDO_INQUIRY": {
            "REOPEN_TASKS": ["fill-inquiry"],
        },
        "QUESTIONS": {
            "STATEMENT": "inquiry-answer-assessment",
            "ANCILLARY_CLAUSES": "inquiry-answer-ancillary-clauses",
            "DEADLINE": "inquiry-deadline",
        },
        "NOTIFY_ON_CANCELLATION": True,
        "NOTIFICATIONS": {
            "INQUIRY_SENT": {
                "template_slug": "verfahrensablauf-fachstelle",
                "recipient_types": ["inquiry_addressed"],
            },
            "INQUIRY_SENT_TO_USO": {
                "template_slug": "verfahrensablauf-uso",
                "recipient_types": ["inquiry_addressed"],
            },
            "INQUIRY_ANSWERED": {
                "template_slug": "bericht-erstellt",
                "recipient_types": ["inquiry_controlling"],
            },
            "CANCELED_DISTRIBUTION": {
                "template_slug": "zirkulation-abgebrochen",
                "recipient_types": ["services_with_incomplete_inquiries"],
            },
        },
        "INQUIRY_TASK": "inquiry",
        "DEADLINE_LEAD_TIME_FOR_ADDRESSED_SERVICES": {
            "uso": 7,
            "authority-bab": 90,
        },
        "ANSWERS": {
            "STATUS": {
                "POSITIVE": "inquiry-answer-status-positive",
                "NEGATIVE": "inquiry-answer-status-negative",
                "NOT_INVOLVED": "inquiry-answer-status-not-involved",
                "CLAIM": "inquiry-answer-status-claim",
                "UNKNOWN": "inquiry-answer-status-unknown",
            },
        },
        "SUGGESTIONS": {
            "QUESTIONS": {
                ("ausserhalb-bauzone", "ausserhalb-bauzone-ja"): ["are"],
                (
                    "waldareal",
                    "waldareal-ja",
                ): ["alt"],
                (
                    "wohnnutzung",
                    "wohnnutzung-ja",
                ): ["alg1"],
                (
                    "mehr-als-vier-wohneinheiten",
                    "mehr-als-vier-wohneinheiten-ja",
                ): ["pro-infirmis"],
                (
                    "beschreibung-der-nutzung",
                    "beschreibung-der-nutzung-abfallanlage",
                ): ["alg2"],
                (
                    "beschreibung-der-nutzung",
                    "beschreibung-der-nutzung-lageranlage",
                ): ["alg2"],
                (
                    "beschreibung-der-nutzung",
                    "beschreibung-der-nutzung-materialgewinnung",
                ): ["alg2"],
                (
                    "industrie-und-gewerbeabwasser",
                    "industrie-und-gewerbeabwasser-ja",
                ): ["alg2"],
                (
                    "mehr-als-50-arbeitsplaetze",
                    "mehr-als-50-arbeitsplaetze-ja",
                ): ["pro-infirmis"],
                (
                    "kantonsstrassen",
                    "kantonsstrassen-ja",
                ): ["bafu"],
                (
                    "haustechnische-anlagen-brandschutz",
                    "haustechnische-anlagen-brandschutz-ja",
                ): ["gvg"],
                (
                    "ist-ein-gewaesser-betroffen",
                    "ist-ein-gewaesser-betroffen-ja",
                ): ["anu", "ajf"],
                (
                    "muessen-ufervegetation-hecken-oder-feldgehoelze-entfernt-werden",
                    "muessen-ufervegetation-hecken-oder-feldgehoelze-entfernt-werden-ja",
                ): ["alg2"],
                (
                    "objekt-der-denkmalpflege",
                    "objekt-der-denkmalpflege-ja",
                ): ["denkmalpflege"],
                (
                    "wird-material-vor-ort-aufbereitet",
                    "wird-material-vor-ort-aufbereitet-ja",
                ): ["alg2"],
                (
                    "uvp-pflicht",
                    "uvp-pflicht-ja",
                ): ["alg2"],
                (
                    "beschreibung-der-anlagen",
                    "beschreibung-der-anlagen-solaranlagen",
                ): ["gvg", "aev"],
                (
                    "beschreibung-der-anlagen",
                    "beschreibung-der-anlagen-verkehrsanlagen",
                ): ["aev"],
                (
                    "beschreibung-der-anlagen",
                    "beschreibung-der-anlagen-waermepumpen",
                ): ["alg2"],
                (
                    "das-bauvorhaben-befindet-sich-in",
                    "das-bauvorhaben-befindet-sich-in-gefahrenzone",
                ): ["alt", "gvg"],
                (
                    "das-bauvorhaben-befindet-sich-in",
                    "das-bauvorhaben-befindet-sich-in-kataster-belasteter-standorte",
                ): ["alg2"],
                (
                    "das-bauvorhaben-befindet-sich-in",
                    "das-bauvorhaben-befindet-sich-in-gewaesserschutzbereich",
                ): ["alg2"],
                (
                    "das-bauvorhaben-befindet-sich-in-laermvorbelastetes",
                    "das-bauvorhaben-befindet-sich-in-laermvorbelastetes-gebiet",
                ): ["alg2"],
                (
                    "das-bauvorhaben-befindet-sich-in",
                    "das-bauvorhaben-befindet-sich-in-archaeologiezone",
                ): ["adg"],
                (
                    "landwirtschaftliches-vorhaben",
                    "landwirtschaftliches-vorhaben-ja",
                ): ["alg1"],
                (
                    "erschliessungsanlagen",
                    "erschliessungsanlagen-versorgung-entsorgung",
                ): ["alg2", "anu"],
                (
                    "erschliessungsanlagen",
                    "erschliessungsanlagen-abwasser",
                ): ["alg2"],
                (
                    "erschliessungsanlagen",
                    "erschliessungsanlagen-antennenanlage",
                ): ["alg2"],
                (
                    "erschliessungsanlagen",
                    "erschliessungsanlagen-beschneiungsanlage",
                ): ["alg2"],
                (
                    "erschliessungsanlagen",
                    "erschliessungsanlagen-pistenkorrektur",
                ): ["alg2"],
                (
                    "erschliessungsanlagen",
                    "erschliessungsanlagen-terrainveraenderung",
                ): ["alg2"],
                (
                    "erschliessungsanlagen",
                    "erschliessungsanlagen-materialablagerung",
                ): ["alg2"],
                (
                    "nutzungszweck-landwirtschaft",
                    "nutzungszweck-landwirtschaft-bienenhaus",
                ): ["alg1"],
                (
                    "handelt-es-sich-um-einen-subventionierten-stall",
                    "handelt-es-sich-um-einen-subventionierten-stall-ja",
                ): ["alg1"],
                (
                    "nutzungszweck-der-gewerblichen-baute",
                    "nutzungszweck-der-gewerblichen-baute-hotel",
                ): ["alg1"],
                (
                    "nutzungszweck-der-gewerblichen-baute",
                    "nutzungszweck-der-gewerblichen-baute-gastronomie",
                ): ["alg1"],
                (
                    "bauanzeige-haustechnische-anlagen-brandschutz",
                    "bauanzeige-haustechnische-anlagen-brandschutz-ja",
                ): ["gvg"],
                (
                    "dachtyp",
                    "dachtyp-schraegdach",
                ): ["gvg", "aib"],
                (
                    "dachtyp",
                    "dachtyp-flachdach",
                ): ["gvg", "aib"],
            }
        },
    },
    "kt_so": {
        "ENABLED": True,
        "INSTANCE_STATE_DISTRIBUTION": "distribution",
        "HISTORY": {
            "COMPLETE_DISTRIBUTION": _("Circulation completed"),
            "SKIP_DISTRIBUTION": _("Circulation skipped"),
            "REDO_DISTRIBUTION": _("Circulation reopened"),
        },
        "REDO_INQUIRY": {
            "REOPEN_TASKS": ["fill-inquiry"],
        },
        "QUESTIONS": {
            "STATEMENT": "inquiry-answer-positive-assessments",
            "ANCILLARY_CLAUSES": "inquiry-answer-notices-for-authority",
            "DIRECT": "inquiry-direct",
        },
        "ANSWERS": {
            "STATUS": {
                "POSITIVE": "inquiry-answer-status-positive",
                "NEGATIVE": "inquiry-answer-status-negative",
                "CLAIM": "inquiry-answer-status-additional-demand",
                "NO_COMMENT": "inquiry-answer-status-no-comment",
                "UNKNOWN": "inquiry-answer-status-unknown",
                "DIRECT": "inquiry-answer-status-direct",
            },
            "DIRECT": {
                "YES": "inquiry-direct-yes",
            },
        },
        "NOTIFICATIONS": {
            "INQUIRY_SENT": {
                "template_slug": "stellungnahme-angefordert",
                "recipient_types": ["inquiry_addressed"],
            },
            "INQUIRY_ANSWERED": {
                "template_slug": "stellungnahme-beantwortet",
                "recipient_types": ["inquiry_controlling"],
            },
        },
        # For the suggestions services ids or slugs can be used but they shouldn't be mixed.
        "SUGGESTIONS": {
            "QUESTIONS": {
                (
                    "fumoir",
                    "fumoir-ja",
                ): [114],
                (
                    "infrastrukturanlagen-landschaft",
                    "infrastrukturanlagen-landschaft-trinkwasser",
                ): [114],
                (
                    "gefahrenstufen",
                    "gefahrenstufen-geringe-gefaehrdung",
                ): [115],
                (
                    "gefahrenstufen",
                    "gefahrenstufen-mittlere-gefaehrdung",
                ): [115],
                (
                    "gefahrenstufen",
                    "gefahrenstufen-erhebliche-gefaehrdung",
                ): [115],
                (
                    "gefahrenstufen",
                    "gefahrenstufen-restgefaehrdung",
                ): [115],
                (
                    "naturgefahrengefaehrdung",
                    "naturgefahrengefaehrdung-ja",
                ): [108, 112, 115],
                (
                    "gefaehrdung-durch-oberflaechenabfluss",
                    "gefaehrdung-durch-oberflaechenabfluss-ja",
                ): [115],
                (
                    "objektschutzmassnahmen-geplant",
                    "objektschutzmassnahmen-geplant-ja",
                ): [115],
                (
                    "objektschutzmassnahmen-beratung",
                    "objektschutzmassnahmen-beratung-ja",
                ): [115],
                (
                    "mindest-und-grenzabstaende",
                    "mindest-und-grenzabstaende-gebaeudeabstand",
                ): [115],
                (
                    "brandschutzplaene",
                    "brandschutzplaene-ja",
                ): [115],
                (
                    "aushublagerplaetze-oder-baupisten",
                    "aushublagerplaetze-oder-baupisten-ja",
                ): [109],
                ("bab", "bab-ja"): [109],
            },
        },
    },
    "kt_uri": {
        "ENABLED": True,
        "INSTANCE_STATE_DISTRIBUTION": "comm",
        "HISTORY": {
            "COMPLETE_DISTRIBUTION": _("Circulation completed"),
            "SKIP_DISTRIBUTION": _("Circulation skipped"),
            "REDO_DISTRIBUTION": _("Circulation reopened"),
        },
        "REDO_INQUIRY": {
            "REOPEN_TASKS": ["fill-inquiry"],
        },
        "QUESTIONS": {
            "STATEMENT": "inquiry-answer-statement",
            "ANCILLARY_CLAUSES": "inquiry-answer-ancillary-clauses",
        },
        "NOTIFICATIONS": {
            "INQUIRY_SENT": {
                "template_slug": "4-1-zirkulation-gemeinde-gestartet",
                "recipient_types": ["inquiry_addressed"],
            },
            "KOOR_INQUIRY_ANSWERED": {
                "template_slug": "4-2-kantonale-bearbeitung-abgeschlossen",
                "recipient_types": ["inquiry_controlling"],
            },
        },
        "DEFAULT_SUGGESTIONS": [1],  # KOOR BG
        # For the suggestions services ids or slugs can be used but they shouldn't be mixed.
        "SUGGESTIONS": {
            "QUESTIONS": {
                (
                    "purpose",
                    "purpose-industrie",
                ): [3],
                (
                    "purpose",
                    "purpose-gewerbe",
                ): [3],
                (
                    "purpose",
                    "purpose-dienstleistung",
                ): [82],
                (
                    "purpose",
                    "purpose-verkauf",
                ): [82],
                (
                    "purpose",
                    "purpose-landwirtschaft",
                ): [525],
                (
                    "purpose",
                    "purpose-forstwirtschaft",
                ): [546],
                (
                    "purpose",
                    "purpose-gastgewerbe",
                ): [3],
                (
                    "purpose",
                    "purpose-oeffentlich-zugaenglich",
                ): [82],
                (
                    "grundnutzung",
                    "Gewerbezone",
                ): [3],
                (
                    "grundnutzung",
                    "Industriezone",
                ): [3],
                (
                    "grundnutzung",
                    "Kernzone",
                ): [241],
                (
                    "grundnutzung",
                    "Zone für öffentliche Bauten und Anlagen",
                ): [82],
                (
                    "grundnutzung",
                    "Landwirtschaftszone",
                ): [96, 88, 261, 262],
                (
                    "grundnutzung",
                    "Naturschutzzone",
                ): [98],
                (
                    "grundnutzung",
                    "Uferbereich",
                ): [567, 568],
                (
                    "grundnutzung",
                    "Gewässer",
                ): [567, 568, 41, 88, 261, 262],
                (
                    "grundnutzung",
                    "Verkehrsfläche ausserhalb Bauzone",
                ): [88, 261, 262, 41],
                (
                    "grundnutzung",
                    "Reservezone",
                ): [88, 261, 262],
                (
                    "grundnutzung",
                    "Wald",
                ): [2, 88, 261, 262],
                (
                    "grundnutzung",
                    "Deponiezone",
                ): [567, 568],
                (
                    "grundnutzung",
                    "Abbauzone",
                ): [567, 568],
                (
                    "municipality",
                    "1201",
                ): [88],  # BaB 1
                (
                    "municipality",
                    "1216",
                ): [88],
                (
                    "municipality",
                    "1209",
                ): [88],
                (
                    "municipality",
                    "1220",
                ): [88],
                (
                    "municipality",
                    "1208",
                ): [88],
                (
                    "municipality",
                    "1202",
                ): [88],
                (
                    "municipality",
                    "1210",
                ): [88],
                (
                    "municipality",
                    "1212",
                ): [88],
                (
                    "municipality",
                    "1217",
                ): [261],  # BaB 2
                (
                    "municipality",
                    "1207",
                ): [261],
                (
                    "municipality",
                    "1218",
                ): [261],
                (
                    "municipality",
                    "1219",
                ): [261],
                (
                    "municipality",
                    "1213",
                ): [262],  # Bab 3
                (
                    "municipality",
                    "1214",
                ): [262],
                (
                    "municipality",
                    "1204",
                ): [262],
                (
                    "municipality",
                    "1211",
                ): [262],
                (
                    "municipality",
                    "1215",
                ): [262],
                (
                    "municipality",
                    "1205",
                ): [262],
                (
                    "municipality",
                    "1203",
                ): [262],
            },
        },
    },
    "demo": {"ENABLED": True},
}
