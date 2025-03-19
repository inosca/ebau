from camac.settings.env import env

BILLING = {
    "default": {},
    "kt_schwyz": {
        "ENABLED": True,
        "PRODUCT_NUMBERS": [
            100000,  # ARE BGZ, kant. Baubewilligung, Gebühren
            150000,  # AMFZ Brandschutz, kant. Baubewilligung Gebühren
            900000,  # Laburk, Bearbeitungsgebühren Baubewilligung
            300000,  # AMFZ Brandschutz, Baubegleitung und -Abnahme
            310000,  # AFG Gewässerschutz, Baubegleitung und -Abnahme
        ],
        "WILKEN": {
            "ENCODING": "windows-1252",
            "NEWLINE_CHARACTER": "~~",
            # Needs to be configured from env
            "CLERK": env.str("WILKEN_CLERK", default="ZDARE"),
            "USER_ID": env.str("WILKEN_USER_ID", default="ZDARE"),
            "FTP_HOSTNAME": env.str("WILKEN_FTP_HOSTNAME", default="ftp"),
            "FTP_USER": env.str("WILKEN_FTP_USER", default="admin"),
            "FTP_PASSWORD": env.str("WILKEN_FTP_PASSWORD", default="admin"),
            "INVOICE_FILE_NAME": "Rechnung_Ebau_{datetime}.csv",
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
        },
    },
}
