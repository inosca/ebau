USER = {
    "default": {},
    "kt_gr": {
        "ENABLED": True,
        "QUESTION_USER_ATTRIBUTES_MAPPING": {
            "e-mail-gesuchstellerin": "email",
            "vorname-gesuchstellerin": "name",
            "name-gesuchstellerin": "surname",
        },
    },
    "kt_ag": {
        "ENABLED": True,
        "QUESTION_USER_ATTRIBUTES_MAPPING": {
            "e-mail-gesuchstellerin": "email",
            "vorname-gesuchstellerin": "name",
            "name-gesuchstellerin": "surname",
            "telefon-oder-mobile-gesuchstellerin": ["phone", "mobile"],
        },
        "ALLOWED_WRITE_ATTRIBUTES": ["title", "position", "phone", "mobile"],
    },
    "kt_so": {
        "ENABLED": True,
        "QUESTION_OIDC_ATTRIBUTES_MAPPING": {
            "e-mail-gesuchstellerin": "email",
            "vorname-gesuchstellerin": "given_name",
            "name-gesuchstellerin": "family_name",
        },
        "ALLOWED_WRITE_ATTRIBUTES": ["title", "position", "phone", "mobile"],
    },
}
