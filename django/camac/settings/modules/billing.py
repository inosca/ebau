from camac.settings.env import env

"""
PRODUCT_NUMBERS

Configure product numbers which can be selected in the billing module when
creating new billing entries. This also requires the `productNumber` flag
to be set to true in `ember-ebau-core/addon/config/features/[canton].js`.

Available configuration options:
{
    Product number
    "number": number

    Name of the product number. Use gettext if it needs to be translated.
    "name": str

    List of service slugs which this product number is visible for.
    "only_for_services": list[string]

    List of service slugs which this product number is NOT visible for.
    "not_for_services": list[string]

    Should this product number be only available if an invoice exists already.
    "only_subsequent_charge": bool
}
"""

BILLING = {
    "default": {},
    "kt_schwyz": {
        "ENABLED": True,
        "PRODUCT_NUMBERS": [
            {
                "number": 100000,
                "name": "ARE BGZ, kant. Baubewilligung, Gebühren",
                "not_for_services": ["amfz-brandschutz", "laboratorium-urkantone"],
            },
            {
                "number": 150000,
                "name": "AMFZ Brandschutz, kant. Baubewilligung Gebühren",
                "only_for_services": ["amfz-brandschutz"],
            },
            {
                "number": 900000,
                "name": "Laburk, Bearbeitungsgebühren Baubewilligung",
                "only_for_services": ["laboratorium-urkantone"],
            },
            {
                "number": 300000,
                "name": "AMFZ Brandschutz, Baubegleitung und -Abnahme",
                "only_subsequent_charge": True,
                "only_for_services": ["amfz-brandschutz"],
            },
            {
                "number": 310000,
                "name": "AFG Gewässerschutz, Baubegleitung und -Abnahme",
                "only_subsequent_charge": True,
                "only_for_services": [
                    "afg-wasserbau",
                    "afg-fischerei",
                    "afg-industrie-gewerbeabwasser",
                    "afg-entwaesserung",
                ],
            },
        ],
        "WILKEN": {
            "ENCODING": "windows-1252",
            "NEWLINE_CHARACTER": "~~",
            "CLERK": env.str("WILKEN_CLERK", default="ZDARE"),
            "USER_ID": env.str("WILKEN_USER_ID", default="ZDARE"),
            "INVOICE_FILE_NAME": "Rechnung_Ebau_{datetime}_{identifier}.csv",
            "PAYMENT_PURPOSE": "Baugesuch {instance_id}",
            "CUSTOMER_NUMBERS": {
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
            "KEYCLOAK_CLIENT": "wilken",
        },
    },
}
