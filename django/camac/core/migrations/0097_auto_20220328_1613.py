# Generated by Django 3.2.12 on 2022-03-28 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0096_add_ordering_to_resource_and_instance_resource'),
    ]

    operations = [
        migrations.AlterField(
            model_name='irroleacl',
            name='instance_resource',
            field=models.ForeignKey(db_column='INSTANCE_RESOURCE_ID', on_delete=django.db.models.deletion.CASCADE, related_name='role_acls', to='core.instanceresource'),
        ),
        migrations.AlterField(
            model_name='rroleacl',
            name='resource',
            field=models.ForeignKey(db_column='RESOURCE_ID', on_delete=django.db.models.deletion.CASCADE, related_name='role_acls', to='core.resource'),
        ),
    ]
