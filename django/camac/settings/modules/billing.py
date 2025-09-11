from camac.settings.ebau_schema import ModuleConfig
from camac.settings.env import env
from camac.settings.modules.billing_schema import (
    BillingConfig,
    WilkenConfig,
)

CANTONAL_SERVICE_GROUP_SLUGS = [
    "baugesuchszentrale",
    "fachstellen",
]

ALLOWED_FORMS_FOR_PRODUCT_NUMBERS = [
    "baugesuch-reklamegesuch",
    "projektanderung",
    "vorentscheid-gemass-ss84-pbg",
    "technische-bewilligung",
]

BILLING = ModuleConfig[BillingConfig](
    default=BillingConfig(),
    kt_schwyz=BillingConfig(
        # Keep this config in sync with ember-ebau-core/addon/config/features/sz.js
        enabled=True,
        product_numbers=[],
        wilken=WilkenConfig(
            encoding="windows-1252",
            newline_character="~~",
            clerk=env.str("WILKEN_CLERK", default="ZDARE"),
            user_id=env.str("WILKEN_USER_ID", default="ZDARE"),
            invoice_file_name="Rechnung_Ebau_{datetime}_{identifier}.csv",
            payment_purpose="Baugesuch {instance_id}",
            customer_numbers={
                "Schwyz": "015177",
                "Arth": "015178",
                "Ingenbohl": "015180",
                "Muotathal": "015181",
                "Steinen": "015182",
                "Sattel": "015183",
                "Rothenthurm": "015185",
                "Oberiberg": "015184",
                "Unteriberg": "015186",
                "Lauerz": "015187",
                "Steinerberg": "015188",
                "Morschach": "015189",
                "Alpthal": "015190",
                "Illgau": "015191",
                "Riemenstalden": "015192",
                "Gersau": "015193",
                "Lachen": "015194",
                "Altendorf": "015195",
                "Galgenen": "015196",
                "Vorderthal": "015197",
                "Innerthal": "015199",
                "Schübelbach": "015200",
                "Tuggen": "015201",
                "Wangen": "015202",
                "Reichenburg": "015203",
                "Einsiedeln": "015204",
                "Küssnacht": "015205",
                "Wollerau": "015206",
                "Freienbach": "015207",
                "Feusisberg": "015208",
            },
            keycloak_client="wilken",
        ),
        cantonal_service_group_slugs=CANTONAL_SERVICE_GROUP_SLUGS,
    ),
)
