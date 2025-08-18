BAB = {
    "default": {},
    "kt_gr": {
        "ENABLED": True,
        "SERVICE_GROUP": "authority-bab",
        "MASTER_DATA_PROPERTIES": ["is_bab_location"],
    },
    "kt_so": {
        "ENABLED": True,
        "SERVICE_GROUP": "service-bab",
        "MASTER_DATA_PROPERTIES": ["is_bab_temporary", "is_bab_location"],
    },
}
