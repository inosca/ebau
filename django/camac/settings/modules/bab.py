from camac.settings.env import env

BAB = {
    "default": {},
    "kt_so": {
        "ENABLED": True,
        "SERVICE_GROUP": "service-bab",
        "MASTER_DATA_PROPERTIES": ["is_bab_temporary", "is_bab_location"],
        "EXCLUDED_IN_DISTRIBUTION": env.list(
            "DJANGO_EXCLUDED_IN_DISTRIBUTION",
            default=[
                # Test system values:
                113,  # Amt für Denkmalpflege und Archäologie
                108,  # Amt für Umwelt (AfU)
                112,  # Amt für Wald, Jagd und Fischerei
                114,  # Gesundheitsamt
                # TODO: add services that don't exist yet:
                # Amt für Verkehr und Tiefbau
                # Amt für Landwirtschaft
            ],
        ),
    },
}
