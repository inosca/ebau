import re
import sqlite3
import subprocess
from functools import lru_cache
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

from django.conf import settings
from django.core.management.base import BaseCommand


class S3CMD:
    _default_proc_args = {
        "stdin": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
        "stdout": subprocess.DEVNULL,
    }

    def __init__(self):

        # These are the ones we need for sync. Note this will only work for
        # synchronizing document module data (for now), DMS and communications
        # have their own buckets, so it would end up in the wrong place.
        self.endpoint_url = settings.ALEXANDRIA_S3_ENDPOINT_URL
        self.bucket_name = settings.ALEXANDRIA_S3_BUCKET_NAME
        self.access_key = settings.ALEXANDRIA_S3_ACCESS_KEY
        self.secret_key = settings.ALEXANDRIA_S3_SECRET_KEY

        # Alexandria provides these additional options to configure S3 access.
        #  - settings.ALEXANDRIA_S3_USE_SSL
        #  - settings.ALEXANDRIA_S3_VERIFY
        #  - settings.ALEXANDRIA_S3_REGION_NAME
        #  - settings.ALEXANDRIA_S3_OBJECT_PARAMETERS

        self.use_ssl = self.endpoint_url.startswith("https://")

        self.bucket_path = f"s3://{self.bucket_name}"

    def run(self, *args, **popen_kwargs) -> subprocess.Popen:
        """
        Run an S3 command.

        You can pass any arguments, which will be run via `subprocess.Popen`,
        which is then returned.

        You can pass `s3cmd.bucket_path` if you need to refer to the bucket
        """

        # Note: We're passing all the secrets and config via commandline. While
        # this is theoretically insecure, we intend to run this in a secured
        # environment, so we're choosing the simpler option.

        config = [
            f"--access_key={self.access_key}",
            f"--secret_key={self.secret_key}",
            f"--host={self.endpoint_url}",
            f"--host-bucket={self.endpoint_url}",
            "--ssl" if self.use_ssl else "--no-ssl",
        ]

        cmdline = ["s3cmd", *config, *args]

        # TODO deal with stdout,stdin etc
        return subprocess.Popen(cmdline, **{**self._default_proc_args, **popen_kwargs})

    def run_cmd_and_wait(self, *args):
        cmd = self.run(*args)
        cmd.communicate()
        cmd.wait()

    def put(self, in_filename, path_in_bucket):
        to_put = f"{self.bucket_path}/{path_in_bucket}"

        self.run_cmd_and_wait("put", in_filename, to_put)

    def get(self, path_in_bucket, out_filename):
        to_get = f"{self.bucket_path}/{path_in_bucket}"
        self.run_cmd_and_wait("get", to_get, out_filename)

    def delete(self, path_in_bucket):
        to_del = f"{self.bucket_path}/{path_in_bucket}"
        self.run_cmd_and_wait("del", to_del)

    def sync(self, local_path, path_in_bucket, *args):
        target = f"{self.bucket_path}/{path_in_bucket}"
        if not target.endswith("/"):
            target = f"{target}/"

        self.run_cmd_and_wait("sync", local_path, target, *args)

    def clean_s3(self, path_in_bucket, *args):
        target = f"{self.bucket_path}/{path_in_bucket}"
        if not target.endswith("/"):
            target = f"{target}/"

        self.run_cmd_and_wait("delete", "--recursive", target, *args)

    def validate(self, local_path, path_in_bucket):
        while local_path.endswith("/"):
            local_path = local_path[:-1]

        target = f"{self.bucket_path}/{path_in_bucket}"
        if not target.endswith("/"):
            target = f"{target}/"

        list_file_s3 = NamedTemporaryFile()
        list_file_fs = NamedTemporaryFile()

        s3cmd = self.run("ls", "--recursive", "--list-md5", target, stdout=list_file_s3)

        finder = subprocess.Popen(
            [
                "find",
                local_path,
                # "-print0",
                "-type",
                "f",
            ],
            stdout=subprocess.PIPE,
        )
        localcmd = subprocess.Popen(
            [
                "xargs",
                # "-0",
                "md5sum",
            ],
            stdin=finder.stdout,
            stdout=list_file_fs,
        )

        finder.wait()  # ensure stdin is consumed, cmd is run
        localcmd.wait()
        s3cmd.wait()

        dbfile = NamedTemporaryFile(suffix=".db")
        db = sqlite3.Connection(dbfile.name)
        # We don't create indexes, as we basically only do some very few lookups before
        # ditching the DB again
        db.execute("create table s3(id bigint primary key, hash varchar, path varchar)")
        db.execute("create table fs(id bigint primary key, hash varchar, path varchar)")

        # Load files and compare results
        list_file_s3.seek(0)
        list_file_fs.seek(0)

        # fsdata entry format: md5<tab>path\n
        # s3data entry format: date time      size  md5     s3://path
        re_fs = re.compile(rf"(\w+)\s+{local_path}/(.*)\n$")
        re_s3 = re.compile(
            rf"([0-9-]+)\s+([0-9:]+)\s+(\d+)\s+([\w]+)\s+{target}([^\s]+)$"
        )

        def parse_fs(line):
            matchy = re_fs.match(line.decode("utf8"))
            return (matchy.group(2), matchy.group(1)) if matchy else (None, None)

        def parse_s3(line):
            matchy = re_s3.match(line.decode("utf8"))
            return (matchy.group(5), matchy.group(4)) if matchy else (None, None)

        with db:
            self._load_validation_logs(list_file_s3, parse_s3, db, "s3")
            self._load_validation_logs(list_file_fs, parse_fs, db, "fs")
        return self._validate(db)

    def _validate(self, db):
        """Validate check results from DB vs S3.

        Log any mismatch detected, and return a tuple of:

        (num_missing_in_s3, num_missing_in_fs, num_equal, num_hash_mismatches)
        """
        missing_in_s3 = db.execute("""
           select fs.id, fs.path, fs.hash
           from fs left join s3 on fs.path=s3.path
           where s3.id is null
        """)

        missing_in_fs = db.execute("""
           select s3.id, s3.path, s3.hash
           from s3 left join fs on s3.path=fs.path
           where fs.id is null
        """)

        equal = db.execute("""
           select count(*)
           from fs left join s3 on fs.path=s3.path and fs.hash=s3.hash
           where s3.id is NOT null
        """)

        hash_mismatch = db.execute("""
           select fs.id, fs.path, fs.hash, s3.hash
           from fs left join s3 on fs.path=s3.path and fs.hash != s3.hash
           where s3.id is NOT null
        """)

        num_missing_in_s3 = 0
        num_missing_in_fs = 0
        num_equal = equal.fetchone()[0]
        num_hash_mismatches = 0
        for _id, path, hash in missing_in_s3:
            num_missing_in_s3 += 1
            print(f"Warn: FS entry missing in S3: {path} (md5: {hash})")
        for _id, path, hash in missing_in_fs:
            num_missing_in_fs += 1
            print(f"Warn: S3 entry missing in FS: {path} (md5: {hash})")
        for _id, fspath, fshash, s3hash in hash_mismatch:
            num_hash_mismatches += 1
            print(f"Warn: Hash mismatch: FS:{fshash} S3:{s3hash} - {fspath}")

        return (num_missing_in_s3, num_missing_in_fs, num_equal, num_hash_mismatches)

    def _load_validation_logs(self, logfile, parser, db, to_table):
        for line in logfile:
            path, hash = parser(line)
            if not path:
                continue
            db.execute(
                f"insert into {to_table} (path, hash) values (?, ?)", [path, hash]
            )


class Command(BaseCommand):
    help = """Sync filesystem-storage data to S3.

    Migrate application data from filesystem storage to S3, verify the migration
    and check the configuration.

    By default, nothing is done - every action needs to be explicitly requested
    via the arguments.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--check-config",
            action="store_true",
            dest="check_config",
            default=False,
            help="Check storage backend and S3 credentials are configured correctly",
            required=False,
        )
        parser.add_argument(
            "--sync",
            action="store_true",
            dest="do_sync",
            default=None,
            help="Synchronize data from filesystem to S3",
            required=False,
        )
        parser.add_argument(
            "--clean-s3-before-sync",
            action="store_true",
            dest="clean_before_sync",
            default=None,
            help="Clean any data in S3 before sync. Use with great care!",
            required=False,
        )
        parser.add_argument(
            "--validate",
            action="store_true",
            dest="validate",
            help="Compare data on filesystem with S3, report any differences",
            required=False,
        )

    @property
    @lru_cache
    def s3(self) -> S3CMD:
        """Return the S3 cmd client object."""
        return S3CMD()

    def handle(self, *args, **options):
        if options["check_config"]:
            self.check_config()

        if options["clean_before_sync"]:
            self.s3.clean_s3("")
        if options["do_sync"]:
            self.s3.sync(settings.MEDIA_ROOT, "")

        if options["validate"]:
            self.s3.validate(settings.MEDIA_ROOT, "")

    def check_config(self):
        # Note: This checks the django storages backend config. Alexandria
        # has it's own config to access S3 that bypasses the regular storages
        # config. This is only used to verify it for the other
        # modules (documents, communications, dossier import, ...)

        errors = 0
        backend = settings.STORAGES["default"]["BACKEND"]
        storage_opts = settings.STORAGES["default"].get("OPTIONS", {})

        if not backend == "storages.backends.s3.S3Storage":
            print("Error: S3 backend not configured")
            errors += 1

        required_keys = {
            "endpoint_url": "EBAU_S3_ENDPOINT_URL",
            "bucket_name": "EBAU_STORAGE_BUCKET_NAME",
            "access_key": "EBAU_S3_ACCESS_KEY_ID",
            "secret_key": "EBAU_S3_SECRET_KEY_ID",
        }
        for key, env_var_name in required_keys.items():
            option = storage_opts.get(key)
            if option is None:
                print(f"Error: S3 option {key} ({env_var_name}) is not configured")
                errors += 1

        if errors:
            return False

        # OK, config is complete, but does it work?
        print("S3 configuration seems to be in order")
        # TODO: use regular S3 client to create and remove a temporary object
        # to ensure our "normal" client works as well

        tmp_in = NamedTemporaryFile()
        test_value = b"Testing content"
        tmp_in.write(test_value)
        tmp_in.seek(0)
        with TemporaryDirectory() as tmpdir:
            tmpout = Path(tmpdir) / "test_out"

            self.s3.put(tmp_in.name, tmp_in.name)  # use tmp_in as "filename in bucket"
            self.s3.get(tmp_in.name, str(tmpout))
            self.s3.delete(tmp_in.name)

            read_write_ok = tmpout.open().read() == test_value
            return read_write_ok
