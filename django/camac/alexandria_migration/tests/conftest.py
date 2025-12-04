import pytest
from django.core.management import call_command

from camac.alexandria_migration.utils import get_available_categories
from camac.document.models import AttachmentSection


@pytest.fixture
def clear_category_cache():
    get_available_categories.cache_clear()


@pytest.fixture
def be_category_setup(db, settings, clear_category_cache):
    call_command("loaddata", settings.ROOT_DIR("kt_bern/config/document.json"))
    call_command("loaddata", settings.ROOT_DIR("kt_bern/config/alexandria_core.json"))

    # Taken from php/kt_bern/configs/application.ini
    buckets = [
        "dokument-grundstucksangaben",
        "dokument-gutachten-nachweise-begrundungen",
        "dokument-projektplane-projektbeschrieb",
        "dokument-weitere-gesuchsunterlagen",
        "dokument-amts-fachstellen",
        "dokument-merkblaetter",
        "dokument-rechtsbegehren",
        "dokument-stellungnahmen-verfahrensbeteiligte",
        "dokument-leitbehoerde",
        "dokument-entscheid",
    ]

    return AttachmentSection.objects.order_by("sort"), buckets
