from camac.settings.ebau_schema import ModuleConfig
from camac.settings.modules.user_schema import UserConfig

USER = ModuleConfig[UserConfig](
    default=UserConfig(),
    kt_gr=UserConfig(
        enabled=True,
        question_user_attributes_mapping={
            "e-mail-gesuchstellerin": "email",
            "name-gesuchstellerin": "name",
            "vorname-gesuchstellerin": "surname",
        },
    ),
    kt_ag=UserConfig(
        enabled=True,
        question_user_attributes_mapping={
            "e-mail-gesuchstellerin": "email",
            "name-gesuchstellerin": "name",
            "vorname-gesuchstellerin": "surname",
            "telefon-oder-mobile-gesuchstellerin": ["phone", "mobile"],
        },
        allowed_write_attributes=[
            "title",
            "position",
            "phone",
            "mobile",
        ],
    ),
    kt_so=UserConfig(
        enabled=True,
        question_user_attributes_mapping={
            "e-mail-gesuchstellerin": "email",
            "name-gesuchstellerin": "name",
            "vorname-gesuchstellerin": "surname",
        },
        allowed_write_attributes=[
            "title",
            "position",
            "phone",
            "mobile",
            "division",
        ],
    ),
)
