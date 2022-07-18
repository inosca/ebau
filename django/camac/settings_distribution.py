from datetime import timedelta

from camac.utils import (
    has_permission_for_inquiry_answer_document,
    has_permission_for_inquiry_document,
    is_lead_role,
)

DISTRIBUTION = {
    "default": {
        "ECH_EVENTS": False,
        "DEFAULT_DEADLINE_DELTA": timedelta(days=30),
        "DISTRIBUTION_WORKFLOW": "distribution",
        "DISTRIBUTION_TASK": "distribution",
        "DISTRIBUTION_INIT_TASK": "init-distribution",
        "DISTRIBUTION_COMPLETE_TASK": "complete-distribution",
        "INQUIRY_TASK": "inquiry",
        "INQUIRY_FORM": "inquiry",
        "INQUIRY_CREATE_TASK": "create-inquiry",
        "INQUIRY_CHECK_TASK": "check-inquiries",
        "INQUIRY_WORKFLOW": "inquiry",
        "INQUIRY_ANSWER_FORM": "inquiry-answer",
        "INQUIRY_ANSWER_FILL_TASK": "fill-inquiry",
        "QUESTIONS": {
            "DEADLINE": "inquiry-deadline",
            "REMARK": "inquiry-remark",
            "STATUS": "inquiry-answer-status",
        },
        "ANSWERS": {},
        "NOTIFICATIONS": {},
        "SUGGESTIONS": [],
        "DEFAULT_SUGGESTIONS": [],
        "PERMISSIONS": {
            "CompleteWorkItem": {
                "DISTRIBUTION_COMPLETE_TASK": lambda group, *_: is_lead_role(group),
            },
            "ResumeWorkItem": {
                "INQUIRY_TASK": lambda group, *_: is_lead_role(group),
            },
            "CancelWorkItem": {
                "INQUIRY_TASK": lambda group, *_: is_lead_role(group),
            },
            "SaveDocumentAnswer": {
                "INQUIRY_FORM": lambda group, document, *_: has_permission_for_inquiry_document(
                    group, document
                ),
                "INQUIRY_ANSWER_FORM": lambda group, document, *_: has_permission_for_inquiry_answer_document(
                    group, document
                ),
            },
        },
    },
    "kt_bern": {
        "ENABLED": True,
        "ECH_EVENTS": True,
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
        "SUGGESTIONS": {
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
                "gentechnisch-veraenderte-organismen",
                "gentechnisch-veraenderte-organismen-ja",
            ): [20060],
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
            ): [20050, 20060],
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
        },
        "PERMISSIONS": {
            "CompleteWorkItem": {
                "INQUIRY_ANSWER_FILL_TASK": lambda group, *_: is_lead_role(group),
            },
        },
    },
    "kt_schwyz": {
        "ENABLED": True,
        "INQUIRY_ANSWER_CHECK_TASK": "check-inquiry",
        "INQUIRY_ANSWER_REVISE_TASK": "revise-inquiry",
        "INQUIRY_ANSWER_ALTER_TASK": "alter-inquiry",
        "DEFAULT_SUGGESTIONS": [7],  # Baugesuchszentrale
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
    },
}
