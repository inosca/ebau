import csv
import os
import sys
from contextlib import contextmanager
from typing import Optional

from dotenv import load_dotenv
from hdbcli import dbapi

from camac.dossier_import.config.kt_ag_sap_migration.sap.ebau_soap_client import (
    EBauSoapClient,
)

QUERIES = {
    "in_bearbeitung": """
        select city.CITY as GEMEINDE,
            g.GESUCH_ID,
            g.BTITEL                                      as DOSSIER_TITEL,
            t.TXT30                                       as STATUS_TEXT,
            string_agg(v.ACTION, ', ' order by v.TSTAMPL) as ACTION_LISTE
        from ZEBP_GESUCH g
        left join TJ30T t on t.ESTAT = g.ESTAT and t.STSMA = 'ZEBP'
        left join ZEZS_CITY city on city.CITY_ID = g.GEMEINDE_ID
        left join ZEZS_VERFSTAND v on v.EXTERN_ID = g.GESUCH_ID
        where t.TXT30 = 'Gesuch in Bearbeitung'
            and city.CITY in ('Aarau', 'Aarburg', 'Arni (AG)', 'Biberstein', 'Dietwil', 'Endingen', 'Fischbach-Göslikon', 'Freienwil',
                'Hellikon', 'Lengnau (AG)', 'Meisterschwanden', 'Menziken', 'Mettauertal', 'Möhlin', 'Mülligen',
                'Obermumpf', 'Oberwil-Lieli', 'Olsberg', 'Riniken', 'Suhr', 'Tägerig', 'Tegerfelden',
                'Wallbach', 'Würenlingen', 'Zuzgen'
            )
        group by city.CITY, g.GESUCH_ID, g.BTITEL, t.TXT30
        order by city.CITY, g.GESUCH_ID;
    """,
    "potentiell_liegengeblieben": """
        select city.CITY                                              as GEMEINDE,
               g.GESUCH_ID,
               g.BTITEL                                               as DOSSIER_TITEL,
               t.TXT30                                                as STATUS_TEXT,
               TO_VARCHAR(TO_DATE(g.crdat, 'YYYYMMDD'), 'DD.MM.YYYY') as CREATION_DATE
        from ZEBP_GESUCH g
                 left join TJ30T t on t.ESTAT = g.ESTAT and t.STSMA = 'ZEBP'
                 left join ZEZS_CITY city on city.CITY_ID = g.GEMEINDE_ID
        where t.TXT30 in ('Verfügung erstellt', 'Gesuch in Bearbeitung', 'Gesuch übermittelt', 'Anfrage / Stellungnahme offen',
                          'In öffentlicher Auflage')
          and city.CITY in ('Aarau', 'Aarburg', 'Arni (AG)', 'Biberstein', 'Dietwil', 'Endingen', 'Fischbach-Göslikon', 'Freienwil',
                            'Hellikon', 'Lengnau (AG)', 'Meisterschwanden', 'Menziken', 'Mettauertal', 'Möhlin', 'Mülligen',
                            'Obermumpf', 'Oberwil-Lieli', 'Olsberg', 'Riniken', 'Suhr', 'Tägerig', 'Tegerfelden',
                            'Wallbach', 'Würenlingen', 'Zuzgen'
            )
        order by city.CITY, g.GESUCH_ID;
    """,
}


class SAPAccess:  # pragma: no cover
    def __init__(
        self,
        enabled: bool,
        host: Optional[str],
        port: Optional[int],
        user: Optional[str],
        password: Optional[str],
        db_name: Optional[str],
        schema: Optional[str],
        soap_server: Optional[str],
        soap_user: Optional[str],
        soap_password: Optional[str],
    ):
        self._connection = None
        self.json_target_dir = None

        if enabled:
            self._schema = schema
            self._connection = dbapi.connect(
                address=host,
                port=port,
                user=user,
                password=password,
                databaseName=db_name,
            )
            print("Connected to SAP HANA successfully.")
            self.soap_client = EBauSoapClient(soap_server, soap_user, soap_password)

    def close_connection(self):
        if self._connection:
            self._connection.close()
            print("Connection closed.")

    @contextmanager
    def _managed_cursor(self):
        cursor = self._connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def run_query(self, query: str):
        with self._managed_cursor() as cursor:
            cursor.execute(f"SET SCHEMA {self._schema}")

            print(f"Executing query: {query[:30]}... .")
            cursor.execute(query)
            rows = cursor.fetchall()
            column_headers = [i[0] for i in cursor.description]
            return [column_headers] + rows


def write_csv(results, filename):
    with open(f"{filename}.csv", "w", newline="", encoding="utf-8") as csvfile:
        w = csv.writer(csvfile, delimiter=",")
        w.writerows(results)


if __name__ == "__main__":  # pragma: no cover
    if len(sys.argv) < 3:
        raise Exception("missing args. specify env and query.")

    env = sys.argv[1]
    query = sys.argv[2]

    if query not in QUERIES:
        raise Exception(f"unknown query, choose one of {QUERIES.keys()}")
    print(f"Environment: {env}")

    load_dotenv(f".env.{env}", override=True)

    host = os.getenv("HANA_HOST", "unknown")
    port = int(os.getenv("HANA_PORT", -1))
    user = os.getenv("HANA_USER", "unknown")
    password = os.getenv("HANA_PASSWORD", "unknown")
    dbname = os.getenv("HANA_DBNAME", "unknown")
    schema = os.getenv("HANA_SCHEMA", "unknown")

    soap_server = os.getenv("SOAP_SERVER", "unknown")
    soap_user = os.getenv("SOAP_USER", "unknown")
    soap_password = os.getenv("SOAP_PASSWORD", "unknown")

    base_dir = os.path.dirname(os.path.abspath(__file__))

    db_client = SAPAccess(
        enabled=True,
        host=host,
        port=port,
        user=user,
        password=password,
        db_name=dbname,
        schema=schema,
        soap_server=soap_server,
        soap_user=soap_user,
        soap_password=soap_password,
    )
    try:
        results = db_client.run_query(QUERIES[query])
        write_csv(results, query)
    finally:
        db_client.close_connection()
