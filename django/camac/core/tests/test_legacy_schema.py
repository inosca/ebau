import re
from pathlib import Path

import pytest
from django.core.management import call_command

from camac.settings.env import ROOT_DIR

COMMITTED_SCHEMA = ROOT_DIR("../elixir-ebau/priv/repo/ebau_schema.sql")

VERSION_COMMENT_RE = re.compile(r"^-- Dumped .*\n", re.MULTILINE)
RESTRICT_LINE_RE = re.compile(r"^\\restrict .*\n", re.MULTILINE)


def normalize(content):
    content = VERSION_COMMENT_RE.sub("", content)
    content = RESTRICT_LINE_RE.sub("", content)
    return content


@pytest.mark.django_db
def test_legacy_schema_up_to_date(db, tmp_path):
    dump_path = tmp_path / "ebau_schema.sql"

    call_command("dump_legacy_schema", output=str(dump_path))

    fresh = normalize(dump_path.read_text())
    committed = normalize(Path(COMMITTED_SCHEMA).read_text())

    assert fresh == committed, (
        "ebau_schema.sql is out of date. Run: python manage.py dump_legacy_schema"
    )
