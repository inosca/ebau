from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("instance", "0037_instancealexandriadocument"),
    ]

    operations = [
        migrations.RunSQL(
            """UPDATE alexandria_core_document SET metainfo = replace(metainfo::text, '"case_id"', '"camac-instance-id"')::jsonb;""",
            """UPDATE alexandria_core_document SET metainfo = replace(metainfo::text, '"camac-instance-id"', '"case_id"')::jsonb;""",
        ),
        migrations.RunSQL(
            """CREATE INDEX "alexandria_core_document_instance_id" ON alexandria_core_document((metainfo->'camac-instance-id'));""",
            """DROP INDEX "alexandria_core_document_instance_id";""",
        ),
    ]
