PROJECT_MODIFICATION = {
    "default": {},
    "kt_bern": {
        "ENABLED": True,
        "ALLOW_FORMS": [
            "baugesuch",
            "baugesuch-v2",
            "baugesuch-v3",
            "baugesuch-v5",
            "baugesuch-generell",
            "baugesuch-generell-v2",
            "baugesuch-generell-v3",
            "baugesuch-generell-v5",
            "baugesuch-mit-uvp",
            "baugesuch-mit-uvp-v2",
            "baugesuch-mit-uvp-v3",
            "baugesuch-mit-uvp-v5",
        ],
        "DISALLOW_STATES": ["new", "finished", "archived"],
    },
    "kt_uri": {
        "ENABLED": True,
        "ALLOW_FORMS": ["building-permit"],
        "DISALLOW_STATES": ["new", "done", "old", "arch"],
    },
    "kt_gr": {
        "ENABLED": True,
        "ALLOW_FORMS": ["baugesuch"],
        "DISALLOW_STATES": ["new"],
    },
    "kt_so": {
        "ENABLED": True,
    },
}
