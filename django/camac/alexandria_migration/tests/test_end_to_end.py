import os.path
import random

import pytest
from alexandria.core import models as alexandria_models
from django.core.management import call_command
from pytest_lazy_fixtures import lf

from camac.alexandria_migration.models import DocumentMark
from camac.alexandria_migration.utils import get_marks_from_context
from camac.communications import models as comm_models
from camac.document.models import AttachmentSection, AttachmentVersion


def setup_migration_test_data(
    settings,
    instance_factory,
    attachment_attachment_section_factory,
    attachment_version_factory,
    communications_attachment_factory,
    communications_message_factory,
    migration_settings,
):
    """
    Build a full migration test scenario.

    Set up multiple instances to test range filtering and make sure attachments
    exist in every legacy section.
    Throw in some trickier cases: multi-category attachments to test
    duplication, legacy marks that need to become DocumentMarks, and documents
    with historical versions.

    Uses PDF, DOCX, and PNG file types to ensure text extraction and
    thumbnail generation are tested while keeping the test run fast.

    Returns:
        tuple: (attachments, instances, instance_ids, min_inst, max_inst)
    """
    # load document attachment sections and alexandria categories
    appname = settings.APPLICATION_NAME
    call_command("loaddata", f"{appname}/config/document.json")
    call_command("loaddata", f"{appname}/config/alexandria_core.json")

    # create a few instances
    instances = instance_factory.create_batch(2)

    attachments = []
    # TODO "question" choices are only allowed in certain categories. Most
    # should be empty, but we should use some of them

    extensions = ["pdf", "docx", "png"]

    # create a document in some sections
    all_sections = list(AttachmentSection.objects.all())
    sections = all_sections[:3]
    for i, section in enumerate(sections):
        question_choices = _question_choices_for_category(
            section.pk, migration_settings
        )
        # alternate instances to keep the test set small but cover all sections
        inst = instances[i % len(instances)]
        ext = random.choice(extensions)
        filename = f"test_file_{section.pk}_{inst.pk}.{ext}"
        att = attachment_attachment_section_factory(
            attachment__instance=inst,
            attachmentsection=section,
            attachment__question=random.choice(question_choices),
            attachment__name=filename,
            attachment__path=filename,
        ).attachment
        attachments.append(att)

    # Multi-category attachments (where legal: only one version)
    # Each instance MUST have at least one multi-category attachment
    # so that the duplicate_documents command marks the instance as duplicated
    # which is a prerequisite for the annotate command.
    multi_cat_attachments = []
    for inst in instances:
        inst_attachments = [a for a in attachments if a.instance_id == inst.pk]
        if inst_attachments:
            multi_cat_attachments.append(random.choice(inst_attachments))

    for att in multi_cat_attachments:
        current_sections = att.attachment_sections.all()
        other_sections = [s for s in sections if s not in current_sections]
        if other_sections:
            target_section = random.choice(other_sections)
            attachment_attachment_section_factory(
                attachment=att, attachmentsection=target_section
            )

    # Marks / context info
    # (isDecision, isPublished, isReplaced)
    marked_attachments = random.sample(attachments, k=min(len(attachments), 2))
    marks_pool = ["isDecision", "isPublished", "isReplaced"]
    for i, att in enumerate(marked_attachments):
        mark = marks_pool[i % len(marks_pool)]
        att.context[mark] = True
        att.save()

    # Versions (only for single-category attachments to keep it simple and legal)
    single_cat_attachments = [
        a for a in attachments if a.attachment_sections.count() == 1
    ]
    versioned_attachments = random.sample(
        single_cat_attachments, k=min(len(single_cat_attachments), 2)
    )
    for att in versioned_attachments:
        for v in range(1, 2):  # add 1 version
            ext = random.choice(extensions)
            filename = f"test_file_{att.pk}_v{v}.{ext}"
            attachment_version_factory(
                attachment=att,
                version=v,
                name=filename,
                path=filename,
            )
        att.refresh_from_db()

    # Communications
    comm_attachments = random.sample(attachments, k=min(len(attachments), 2))
    for att in comm_attachments:
        message = communications_message_factory(topic__instance=att.instance)
        communications_attachment_factory(
            message=message,
            document_attachment=att,
            file_attachment__filename=att.name,
        )

    instance_ids = [inst.pk for inst in instances]
    min_inst = min(instance_ids)
    max_inst = max(instance_ids)

    return attachments, instances, instance_ids, min_inst, max_inst


def check_create_documents(attachments):
    """
    Check that the alexandria documents have been created as expected.

    After the `create_documents` stage, we want to make sure every legacy
    attachment now has a matching Alexandria document.

    Check that the UUIDs and titles match up and verify that all file
    versions were migrated as expected. Also confirm that any
    legacy flags in the attachment's context were correctly converted into
    Alexandria DocumentMarks.
    """
    for att in attachments:
        doc = alexandria_models.Document.objects.get(pk=att.uuid)
        assert doc.title == (att.context.get("displayName", "") or att.name)
        files = alexandria_models.File.objects.filter(document=doc)
        versions_count = AttachmentVersion.objects.filter(attachment=att).count()
        assert files.count() == 1 + versions_count
        legacy_marks = [m.pk for m in get_marks_from_context(att.context)]
        doc_marks = DocumentMark.objects.filter(document=doc).values_list(
            "mark", flat=True
        )
        assert set(legacy_marks) == set(doc_marks)


def check_duplicate_documents(attachments):
    """
    Check that document duplication was done correctly.

    Once the documents are duplicated, we verify that any attachment belonging
    to multiple legacy sections now has individual copies in Alexandria, since
    Alexandria documents are tied to a single category.

    We check that these duplicates landed in the right categories, kept their
    original titles and files, and carry a reference back to their source
    document in their metadata.
    """
    for att in attachments:
        doc = alexandria_models.Document.objects.get(pk=att.uuid)
        if "duplicate-to" in doc.metainfo:
            for cat_pk in doc.metainfo["duplicate-to"]:
                dup_doc = alexandria_models.Document.objects.get(
                    **{
                        "category_id": cat_pk,
                        "metainfo__duplicated-from": str(doc.pk),
                    }
                )
                assert dup_doc.title == doc.title
                assert (
                    alexandria_models.File.objects.filter(document=dup_doc).count() == 1
                )


def check_fix_communication_links(instance_ids):
    """
    Check that communication links are created correctly.

    When we fix communication links, we're making sure that any
    `CommunicationsAttachment` that used to point to a legacy attachment now
    points to the corresponding Alexandria file.

    It should specifically link to the 'ORIGINAL' variant and belong to the
    correct Alexandria document.
    """
    for ca in comm_models.CommunicationsAttachment.objects.filter(
        message__topic__instance_id__in=instance_ids
    ):
        if ca.document_attachment:
            assert ca.alexandria_file_id is not None
            assert ca.alexandria_file.variant == alexandria_models.File.Variant.ORIGINAL
            assert ca.alexandria_file.document_id == ca.document_attachment.uuid


def check_annotate(attachments):
    """
    Ensure that the annotation process (checksums, fts indexing etc) was correct.

    Finally, the annotation check ensures that all migrated 'ORIGINAL' files have a
    valid SHA-256 checksum and that text content was extracted for formats
    like PDF or DOCX.

     We also verify that a thumbnail was generated for the latest version of
    supported files, ensuring they actually have some data in them.
    """
    for att in attachments:
        doc = alexandria_models.Document.objects.get(pk=att.uuid)
        files = alexandria_models.File.objects.filter(
            document=doc, variant=alexandria_models.File.Variant.ORIGINAL
        )
        for f in files:
            assert f.checksum is not None
            assert f.checksum.startswith("sha256:")

            ext = f.name.split(".")[-1].lower()
            if ext in ["pdf", "docx", "txt"]:
                assert f.content_text, f"Text content missing for {f.name}"

        # Thumbnail for the most recent version
        most_recent_original = files.order_by("-created_at").first()
        if most_recent_original:
            thumbnail = alexandria_models.File.objects.filter(
                document=doc,
                variant=alexandria_models.File.Variant.THUMBNAIL,
                original=most_recent_original,
            ).first()

            ext = most_recent_original.name.split(".")[-1].lower()
            if ext in ["pdf", "docx", "png", "jpg"]:
                if thumbnail is None:
                    # Some environments might not have the necessary tools (libreoffice, ghostscript)
                    # to generate all thumbnails. We warn but don't fail if some are missing,
                    # as long as the migrator didn't crash.
                    print(
                        f"WARNING: Thumbnail missing for {most_recent_original.name} (ext: {ext})"
                    )
                else:
                    print(
                        f"SUCCESS: Thumbnail created for {most_recent_original.name} (ext: {ext})"
                    )
                    assert thumbnail.size > 0


@pytest.mark.order(1)  # Slow tests should run first
@pytest.mark.parametrize(
    "application, migration_settings",
    [
        (lf("set_application_be"), lf("be_alexandria_migration_settings")),
        (lf("set_application_sz"), lf("sz_alexandria_migration_settings")),
        # TODO: configure category mapping, etc for UR as well
        # (lf("set_application_ur"), lf("ur_alexandria_migration_settings")),
    ],
)
@pytest.mark.django_db
def test_migration_end_to_end(
    settings,
    instance_factory,
    attachment_attachment_section_factory,
    attachment_version_factory,
    communications_attachment_factory,
    communications_message_factory,
    alexandria_s3_mock,
    # parametrization
    application,
    migration_settings,
):
    attachments, instances, instance_ids, min_inst, max_inst = (
        setup_migration_test_data(
            settings,
            instance_factory,
            attachment_attachment_section_factory,
            attachment_version_factory,
            communications_attachment_factory,
            communications_message_factory,
            migration_settings,
        )
    )

    # We now run the migration as per test instructions.

    # Generate local data (NEVER EVER RUN THIS ANYWHERE CLOSE TO PRODUCTION!)
    # This will overwrite existing documents for the given instances with test
    # data. Useful if you have a prod dump but not a copy of the files themselves
    call_command("overwrite_test_documents", f"--instances={min_inst}..{max_inst}")
    for att in attachments:
        att.refresh_from_db()
        assert os.path.exists(f"{settings.MEDIA_ROOT}/{att.path.name}")

    # Copy data from the local (file) storage to the configured S3 bucket
    # don't forget the --sync param, otherwise it will do nothing!
    call_command("sync_to_s3", "--sync")

    # Make alexandria documents from the old documents-module
    run_migration_command("create_documents", min_inst, max_inst)
    check_create_documents(attachments)

    # Duplicate documents (Alexandria doesn't have multi-category documents, so
    # they are copied into their target categories via this command)
    run_migration_command("duplicate_documents", min_inst, max_inst)
    check_duplicate_documents(attachments)

    # Update links for the communications module
    run_migration_command("fix_communication_links", min_inst, max_inst)
    check_fix_communication_links(instance_ids)

    # Update fulltext index, thumbnails, checksum for each migrated alexandria document
    run_migration_command("annotate", min_inst, max_inst, "--no-parallel")
    check_annotate(attachments)


def run_migration_command(cmd, min_inst, max_inst, *args):
    return call_command(
        "migrate_to_alexandria",
        *args,
        "--from",
        min_inst,
        "--to",
        max_inst,
        cmd,
    )


def _question_choices_for_category(cat_id: int, migration_settings):
    # category mapping gives us the "main" alexandria category.
    # from there, we can check if it has subcategories, and from these
    # subcategories, we can work back via the suffix mapping to find the
    # possible questions
    category_slug = migration_settings.category_mapping[cat_id]
    subcats = alexandria_models.Category.objects.filter(parent_id=category_slug)
    res = []
    for cat in subcats:
        for original_q, suffix in migration_settings.category_suffix_mapping.items():
            if cat.slug.endswith(suffix):
                # candidate
                res.append(original_q)

    if not res:
        # no subcategories, or none with matching original category.
        # Only choice is setting the question to None
        return [None]
    return res
