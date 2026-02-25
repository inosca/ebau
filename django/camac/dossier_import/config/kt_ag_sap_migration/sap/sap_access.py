import glob
import json
import os
import sys
import timeit
import zipfile
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Dict, Generator, List, Optional

from codetiming import Timer
from dotenv import load_dotenv
from hdbcli import dbapi
from hdbcli.dbapi import Cursor, Decimal

from camac.dossier_import.config.kt_ag_sap_migration.sap.ebau_soap_client import (
    EBauSoapClient,
)
from camac.dossier_import.config.kt_ag_sap_migration.sap.sap_codes import FIELD_CODES

MUNICIPALITIES_COUNTS_FILE = "municipalities_counts.json"

QUERY_DOSSIERS = """select g.*, t.TXT30 as GEMEINDE_STATUS, te.TXT30 as KANTONS_STATUS, rt.DESCRIPTION as GESART_KANTON, city.*,
                    ge.CREATED_ON as KANTON_EINGANG, ge.BEARBEITUNGSFRIST as KANTON_BEARBEITUNGSFRIST, rgt.DESCRIPTION as KANTON_GRUPPE,
                    rgt.DESCRIPTION2 as KANTON_GRUPPE2, ge.PERSON_RESPONSIBLE as KANTON_SACHBEARBEITER,
                    ge.COMPLETION_DATE as KANTON_VORL_ABSCHLUSS, rcct.DESCRIPTION as KANTON_ABSCHLUSSCODE,
                    ge.COMPLETION_DURATION as KANTON_DAUER, ge.EXTERNAL_BUSINESS_CASE as KANTON_LWAG_NR,
                    ge.KA_BAN_KNZ as KANTON_KANALISATION, ge.MAWALD_KNZ AS KANTON_MAWALD_KNZ, ge.SNDF_ENTW_KNZ AS KANTON_SNDF_ENTW_KNZ,
                    ge.GWABSNK_KNZ AS KANTON_GWABSNK_KNZ, ge.AWA_KNZ AS KANTON_AWA_KNZ, ge.BVWALD_KNZ AS KANTON_BVWALD_KNZ,
                    ge.HWG_KNZ AS KANTON_HWG_KNZ, ge.DENKMAL_KNZ AS KANTON_DENKMAL_KNZ, ge.WANDERWEGE_KNZ AS KANTON_WANDERWEGE_KNZ,
                    ge.ORTSBILD AS KANTON_ORTSBILD, ge.STOER_KNZ AS KANTON_STOER_KNZ, ge.ARCH_KNZ AS KANTON_ARCH_KNZ,
                    ge.VERKEHR_KNZ AS KANTON_VERKEHR_KNZ, ge.LSMERF_KNZ AS KANTON_LSMERF_KNZ, ge.MATABB_KNZ AS KANTON_MATABB_KNZ,
                    ge.AGV_KNZ AS KANTON_AGV_KNZ, ge.RADWEGE_KNZ AS KANTON_RADWEGE_KNZ,
                    ge.FLACHENVERBRAUCH AS KANTON_FLACHENVERBRAUCH, ge.KOKO_DATUM AS KANTON_KOKO_DATUM, ge.KOKO_STATUS AS KANTON_KOKO_STATUS,
                    ge.BESCHLUSS_GEMEINDE AS KANTON_BESCHLUSS_GEMEINDE, ge.BESCHLUSS_ART AS KANTON_BESCHLUSS_ART,
                    ge.VERZOGERUNG AS KANTON_VERZOGERUNG, ge.BEGRUNDUNG AS KANTON_BEGRUNDUNG, ge.NACHTR_GESUCH_KNZ AS KANTON_NACHTR_GESUCH_KNZ,
                    ge.KANTSTR_KNZ AS KANTON_KANTSTR_KNZ, ge.OEFFGW_KNZ AS KANTON_OEFFGW_KNZ
                    from ZEBP_GESUCH g
                             left join ZEB2_A_REQUEST ge on g.GESUCH_ID = ge.GESUCH_ID
                             left join TJ30T t on t.ESTAT = g.ESTAT and t.STSMA = 'ZEBP'
                             left join TJ30T te on te.ESTAT = ge.KANTON_STATUS and te.STSMA = 'ZEB2_REQ'
                             left join ZEZS_CITY city on city.CITY_ID = g.GEMEINDE_ID
                             left join ZEB2_C_REQ_TYPET rt on ge.REQUEST_TYPE = rt.REQUEST_TYPE
                             left join ZEB2_C_GRUPPET rgt on ge.GROUP_ID = rgt.id
                             left join ZEB2_C_COMPCODET rcct on ge.COMPLETION_CODE = rcct.COMPLETION_CODE
                             """

PARAM_GESUCH_ID = "gesuch_id"

QUERY_LOCATIONS = f"""select ZEBP_STORT.*, ZEZS_CITY.*
                        from ZEBP_STORT
                                 left join ZEZS_CITY on ZEBP_STORT.CITY_ID = ZEZS_CITY.CITY_ID
                        where ZEBP_STORT.GESUCH_ID = :{PARAM_GESUCH_ID}
                    """

QUERY_PLOTS = f"""select ZEBP_PARZ.*, ZEZS_CITY.*
                        from ZEBP_PARZ
                                 left join ZEZS_CITY on ZEBP_PARZ.CITY_ID = ZEZS_CITY.CITY_ID
                        where ZEBP_PARZ.GESUCH_ID = :{PARAM_GESUCH_ID}
                    """

QUERY_CONTACTS = f"""select ZEBP_KONTAKT.*
                        from ZEBP_KONTAKT
                        where ZEBP_KONTAKT.GESUCH_ID = :{PARAM_GESUCH_ID}
                    """

QUERY_DATES = f"""select ZEZS_DATES.*
                    from ZEZS_DATES
                    where process_id = 'ZEBP' and
                    ZEZS_DATES.EXTERN_ID = :{PARAM_GESUCH_ID}
                """

QUERY_ENTSCHEID = f"""select ZEBP_ENTSCHEID.*
                    from ZEBP_ENTSCHEID
                    where ZEBP_ENTSCHEID.EXTERN_ID = :{PARAM_GESUCH_ID}
                """

QUERY_WOHNUTZ = f"""select ZEBP_WOHNUTZ.*
                    from ZEBP_WOHNUTZ
                    where ZEBP_WOHNUTZ.GESUCH_ID = :{PARAM_GESUCH_ID}
                """

QUERY_VERFSTAND = f"""select ZEZS_VERFSTAND.*
                      from ZEZS_VERFSTAND
                      where ZEZS_VERFSTAND.PROCESS_ID = 'ZEBP'
                        and ZEZS_VERFSTAND.EXTERN_ID = :{PARAM_GESUCH_ID}
                """

QUERY_KOMMENTARE = f"""select ZEBP_KOMMENTARE.*
                      from ZEBP_KOMMENTARE
                      where ZEBP_KOMMENTARE.GESUCH_ID = :{PARAM_GESUCH_ID}
                """

QUERY_DWFLOW = f"""select *
                   from ZEZS_DWFLOW dwf
                   where dwf.extern_id = :{PARAM_GESUCH_ID}
                """

QUERY_DWFLOW_DOC = f"""select *
                       from ZEZS_DWFLOW_DOC dwfd
                       where dwfd.extern_id = :{PARAM_GESUCH_ID}
                """

QUERY_DWFLOW_REC = f"""select *
                   from ZEZS_DWFLOW_REC dwfr
                  where dwfr.extern_id = :{PARAM_GESUCH_ID}
                """

QUERY_BERECHT = f"""select *
                   from ZEBP_BERECHT b
                  where b.GESUCH_ID = :{PARAM_GESUCH_ID}
                """

QUERY_KANTON_STATUSVERLAUF = f"""select a.source, a.tstampl, a.whotxt, a.kommentar, a.doc_id, a.doc_version, att.action_txt, att.step_txt
                                    from ZEB2_A_ACTION a
                                    join ZEB2_C_ACTION_T att on att.ACTION_CODE = a.ACTION_CODE
                                    where a.REQUEST = :{PARAM_GESUCH_ID}
                                    order by a.tstampl asc
                """

QUERY_KANTON_KOMMENTARE = f"""select f.timestamp, f.user_id, f.text
                                from ZEB2_A_FORUM f
                                where f.REQUEST_ID = :{PARAM_GESUCH_ID}
                """

QUERY_KANTON_GESUCHSCODES = f"""select BAUG_ID, DESCRIPTION from ZEB2_A_RQ_BGSTYP
                                left join zeb2_c_baugstypt on ZEB2_A_RQ_BGSTYP.BAUG_ID = zeb2_c_baugstypt.id
                                where REQUEST_ID = :{PARAM_GESUCH_ID}
                """

QUERY_KANTON_NUTZUNGSZONEN = f"""select DESCRIPTION from ZEB2_A_RQ_NTZONE
                                    left join zeb2_c_ntzonet on ZEB2_A_RQ_NTZONE.zone_id = ZEB2_C_NTZONET.id
                                    where REQUEST_ID = :{PARAM_GESUCH_ID}
                """

QUERY_KANTON_SCHUTZZONEN = f"""select DESCRIPTION from ZEB2_A_RQ_SZZONE
                                    left join ZEB2_C_SCHZZONET on ZEB2_A_RQ_SZZONE.zone_id = ZEB2_C_SCHZZONET.id
                                    where REQUEST_ID = :{PARAM_GESUCH_ID}
                """

QUERY_KANTON_STRASSEN = f"""select description, road_number from ZEB2_A_RQ_STRTYP
                            left join zeb2_c_strtypt on ZEB2_A_RQ_STRTYP.street_type = ZEB2_C_STRTYPT.street_type
                            where REQUEST_ID =  :{PARAM_GESUCH_ID}
                """

QUERY_KANTON_BAHNEN = f"""select description from ZEB2_A_RQ_BAHN
                            left join ZEB2_C_BAHNT on ZEB2_A_RQ_BAHN.bahn_id = ZEB2_C_BAHNT.id
                            where REQUEST_ID =  :{PARAM_GESUCH_ID}
                """

QUERY_KANTON_GEWAESSER = f"""select river_id, river_name from ZEB2_A_RQ_GEWAS
                                where REQUEST_ID =  :{PARAM_GESUCH_ID}
                """

QUERY_KANTON_GEBUEHREN = f"""select gc.COST_TYPE, ctt.DESCRIPTION, cs.calculation_scheme, CALC_SCHEME_POSITION,
                        request_task_id, UNIT_PRICE, AMOUNT, MSEHI, TAKE, SHOW_IN_GV, COMMENT_FS, COMMENT_AFB
                        from ZEB2_A_GESCOST gc
                            left join ZEB2_C_COSTTYPET ctt on gc.cost_type = ctt.cost_type
                            left join ZEB2_C_CSCHEMEH cs on gc.calc_scheme_id = cs.calc_scheme_id
                        where REQUEST_ID =  :{PARAM_GESUCH_ID}
                """

QUERY_KANTON_SISTIERUNGEN = f"""select DATVON, DATBIS, NOTE, REASON, t.TXT30 as prev_status, created_on, created_by, resume_date, resume_by
                                from ZEB2_A_SUSPENS s
                                    LEFT JOIN TJ30T t on s.PREVIOUS_STATUS = t.ESTAT AND t.STSMA = 'ZEB2_REQ' AND t.SPRAS = 'D'
                                where s.REQUEST_ID =  :{PARAM_GESUCH_ID}
                """

QUERY_DOK_STATUS = (
    f"""select * from ZEBP_DOK_STATUS where EXTERN_ID = :{PARAM_GESUCH_ID}"""
)

QUERIES_PER_DOSSIER = {
    "STANDORTE": QUERY_LOCATIONS,
    "PARZELLEN": QUERY_PLOTS,
    "KONTAKTE": QUERY_CONTACTS,
    "DATES": QUERY_DATES,
    "ENTSCHEID": QUERY_ENTSCHEID,
    "WOHNUTZ": QUERY_WOHNUTZ,
    "VERFSTAND": QUERY_VERFSTAND,
    "KOMMENTARE": QUERY_KOMMENTARE,
    "DWFLOW": QUERY_DWFLOW,
    "DWFLOW_DOC": QUERY_DWFLOW_DOC,
    "DWFLOW_REC": QUERY_DWFLOW_REC,
    "BERECHT": QUERY_BERECHT,
    "KANTON_STATUSVERLAUF": QUERY_KANTON_STATUSVERLAUF,
    "KANTON_KOMMENTARE": QUERY_KANTON_KOMMENTARE,
    "KANTON_GESUCHSCODES": QUERY_KANTON_GESUCHSCODES,
    "KANTON_NUTZUNGSZONEN": QUERY_KANTON_NUTZUNGSZONEN,
    "KANTON_SCHUTZZONEN": QUERY_KANTON_SCHUTZZONEN,
    "KANTON_STRASSEN": QUERY_KANTON_STRASSEN,
    "KANTON_BAHNEN": QUERY_KANTON_BAHNEN,
    "KANTON_GEWAESSER": QUERY_KANTON_GEWAESSER,
    "KANTON_GEBUEHREN": QUERY_KANTON_GEBUEHREN,
    "KANTON_SISTIERUNGEN": QUERY_KANTON_SISTIERUNGEN,
    "DOK_STATUS": QUERY_DOK_STATUS,
}


class SAPAccess:  # pragma: no cover
    def __init__(
        self,
        enabled: bool,
        json_target_dir: Path,
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
        self.json_target_dir = Path(json_target_dir)

        if enabled:
            self._schema = schema
            # Initialize SAP HANA connection parameters
            self._connection = dbapi.connect(
                address=host,
                port=port,
                user=user,
                password=password,
                databaseName=db_name,
            )
            print("Connected to SAP HANA successfully.")
            self.soap_client = EBauSoapClient(soap_server, soap_user, soap_password)

    def list_dossier_count_per_municipality(self, filter: Optional[str] = None):
        if self._connection:
            return self._query_dossier_counts_grouped_by_municipality(filter)
        return self._get_municipalities_counts_from_file()

    @Timer("query_dossiers", logger=None)
    def query_dossiers(
        self,
        filter: Optional[str] = None,
        batch_size: Optional[int] = 500,
        limit: Optional[int] = None,
        dossier_or_segment: Optional[str] = None,
        only_dossier_ids: Optional[List[str]] = None,
    ) -> Generator[Dict, None, None]:
        if self._connection:
            return self._run_query(
                QUERY_DOSSIERS,
                QUERIES_PER_DOSSIER,
                batch_size=batch_size,
                filter=filter,
                limit=limit,
                dossier_or_segment=dossier_or_segment,
            )
        return self._read_dossiers_from_json(
            dossier_or_segment=dossier_or_segment, only_dossier_ids=only_dossier_ids
        )

    def _query_dossier_counts_grouped_by_municipality(
        self, filter: Optional[str] = None
    ):
        return self._run_query(
            """select city.CITY, city.CITY_ID, count(*) as COUNT
                        from ZEBP_GESUCH g
                                 left join ZEB2_A_REQUEST ge on g.GESUCH_ID = ge.GESUCH_ID
                                 left join TJ30T t on t.ESTAT = g.ESTAT and t.STSMA = 'ZEBP'
                                 left join TJ30T te on te.ESTAT = ge.KANTON_STATUS and te.STSMA = 'ZEB2_REQ'
                                 left join ZEZS_CITY city on city.CITY_ID = g.GEMEINDE_ID
        """,
            filter=filter,
            order_or_group="""group by city.CITY, city.CITY_ID
        order by city.CITY""",
        )

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

    def _run_query(
        self,
        query: str,
        queries_per_dossier=None,
        filter=None,
        batch_size=100,
        limit=None,
        dossier_or_segment=None,
        order_or_group=None,
    ) -> Generator[Dict, None, None]:
        if queries_per_dossier is None:
            queries_per_dossier = {}

        with self._managed_cursor() as cursor, self._managed_cursor() as sub_cursor:
            cursor.execute(f"SET SCHEMA {self._schema}")

            if dossier_or_segment:
                filter = " AND ".join(
                    [f for f in [filter, f"GESUCH_ID = {dossier_or_segment}"] if f]
                )

            if filter:
                query = f"{query} WHERE {filter}"
            if order_or_group:
                query = f"{query}\n{order_or_group}"

            print(f"Executing query: {query[:30]}... .")
            print(
                f"Using batch size: {batch_size}, every '.' represents end of a batch."
            )
            dossier_rows = self._execute(
                cursor, query, batch_size=batch_size, limit=limit
            )
            for row in dossier_rows:
                for aggregation_key, query in queries_per_dossier.items():
                    row[aggregation_key] = list(
                        self._execute(
                            sub_cursor,
                            query,
                            {PARAM_GESUCH_ID: row["GESUCH_ID"]},
                            is_subquery=True,
                        )
                    )
                if row.get("GESUCH_ID"):
                    row.update(self.soap_client.get_dossier_texts(row["GESUCH_ID"]))
                self._translate_sap_domain_codes(row, FIELD_CODES)
                yield row

    def _translate_sap_domain_codes(self, row, field_codes):
        for property_name, translations in field_codes.items():
            if value := row.get(property_name):
                if isinstance(value, list):
                    row[property_name] = [
                        self._translate_sap_domain_codes(
                            agg_row, field_codes.get(property_name)
                        )
                        for agg_row in value
                    ]
                else:
                    row[property_name] = translations.get(value) or value
        return row

    def _execute(
        self,
        cursor: Cursor,
        query: str,
        params: Dict[str, str] = None,
        batch_size: int = 100,
        limit: int = None,
        is_subquery: bool = False,
    ):
        if limit:
            query = f"{query} LIMIT {limit}"
        cursor.execute(query, params)

        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            if not is_subquery:
                print(".", end="")
            yield from (dict(zip(r.column_names, r.column_values)) for r in rows)

    @staticmethod
    def _encode(obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj == obj.to_integral() else float(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return obj

    def _write_json_file(self, data: str, dirname, filename):
        target_dir = self.json_target_dir
        if dirname:
            target_dir = os.path.join(target_dir, dirname)
        os.makedirs(target_dir, exist_ok=True)

        file_path = os.path.join(target_dir, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(data)

    def _write_municipalities_to_json(self, filter):
        result = list(self.list_dossier_count_per_municipality(filter=filter))

        total = sum(int(item.get("COUNT", 0)) for item in result)
        print(f"\nExporting a total of {total} dossiers.")

        json_str = json.dumps(result, indent=4)
        self._write_json_file(json_str, None, MUNICIPALITIES_COUNTS_FILE)

    def _write_dossiers_to_json(self, filter=None):
        result = self.query_dossiers(filter=filter)
        i = 0
        for r in result:
            i += 1
            json_str = json.dumps(r, indent=4, default=self._encode)
            self._write_json_file(json_str, r["CITY"], f"{r['GESUCH_ID']}.json")
        print(f"Read {i} Gesuche from database")

    def _read_dossiers_from_json(self, dossier_or_segment=None, only_dossier_ids=None):
        if not dossier_or_segment:
            dossier_or_segment = self.json_target_dir / "**/*.json"

        file_paths = self._get_file_paths(dossier_or_segment)
        for json_file in file_paths:
            if (
                json_file
                and only_dossier_ids is not None
                and os.path.splitext(os.path.basename(json_file))[0]
                not in only_dossier_ids
            ):
                continue

            with Timer(name="json.load", logger=None):
                with open(json_file, "r", encoding="utf-8") as file:
                    yield {
                        **json.load(file),
                        "json_path": json_file,
                    }

    def _get_file_paths(self, dossier_or_segment):
        if os.path.isfile(dossier_or_segment):
            file_paths = [dossier_or_segment]
        elif os.path.isdir(self.json_target_dir / dossier_or_segment):
            dossier_or_segment = (
                f"{self.json_target_dir}/{dossier_or_segment}/**/*.json"
            )
            file_paths = glob.glob(dossier_or_segment, recursive=True)
        else:
            # support patterns (inkl. rekursive search with `**`)
            file_paths = glob.glob(dossier_or_segment, recursive=True)
        file_paths = sorted(file_paths, key=lambda p: os.path.basename(p))
        return file_paths

    def get_dossier_ids(self, segment) -> List[str]:
        return [
            os.path.splitext(os.path.basename(p))[0]
            for p in self._get_file_paths(segment)
        ]

    def _get_municipalities_counts_from_file(self):
        json_file = os.path.join(self.json_target_dir, MUNICIPALITIES_COUNTS_FILE)
        with open(json_file, "r", encoding="utf-8") as file:
            return [
                (entry["CITY"], entry["CITY_ID"], entry["COUNT"])
                for entry in json.load(file)
            ]


def resolve_filter(filter: str) -> str:  # pragma: no cover
    if os.path.isfile(filter):
        with open(filter, encoding="utf-8") as f:
            return f.read()
    return filter


def zip_json_target_dir(json_target_dir: Path):  # pragma: no cover
    suffix = ".zip"
    if str(json_target_dir).endswith("kt_ag_json"):
        suffix = "_zip.zip"

    zip_path = json_target_dir.parent / f"{json_target_dir.name}{suffix}"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for path in json_target_dir.rglob("*"):
            if path.is_file():
                arcname = path.relative_to(json_target_dir)
                zipf.write(path, arcname)
    print(f"Zipped the files to {zip_path}")


def export_dossiers_for_segment_from_env(env):  # pragma: no cover
    load_dotenv(f".env.{env}", override=True)
    print(f"================== {env} ==============================================")

    host = os.getenv("HANA_HOST", "unknown")
    port = int(os.getenv("HANA_PORT", -1))
    user = os.getenv("HANA_USER", "unknown")
    password = os.getenv("HANA_PASSWORD", "unknown")
    dbname = os.getenv("HANA_DBNAME", "unknown")
    schema = os.getenv("HANA_SCHEMA", "unknown")

    soap_server = os.getenv("SOAP_SERVER", "unknown")
    soap_user = os.getenv("SOAP_USER", "unknown")
    soap_password = os.getenv("SOAP_PASSWORD", "unknown")

    filter = resolve_filter(os.getenv("FILTER", None))
    print("Using filter query:")
    print(filter)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_target_dir = Path(
        os.path.join(
            base_dir,
            f"../../../tests/data/{'kt_ag_json' if env == 'test' else env}",
        )
    )

    db_client = SAPAccess(
        enabled=True,
        json_target_dir=json_target_dir,
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
        db_client._write_municipalities_to_json(filter=filter)
        #  filter = "crdat >= 20250200 or crdat <20190000"
        execution_time = timeit.timeit(
            lambda: db_client._write_dossiers_to_json(filter=filter),
            number=1,
        )
        json_target_dir = json_target_dir.resolve(True)
        print(
            f"Writing Gesuche to JSON {json_target_dir} took {execution_time} seconds."
        )
        zip_json_target_dir(json_target_dir)
    finally:
        db_client.close_connection()
        print()


if __name__ == "__main__":  # pragma: no cover
    envs = ["test"]

    if len(sys.argv) > 1:
        envs = sys.argv[1:]
    if len(sys.argv) == 2 and " " in sys.argv[1]:
        envs = sys.argv[1].split()

    print(f"Environments: {envs}")

    for env in envs:
        export_dossiers_for_segment_from_env(env)
