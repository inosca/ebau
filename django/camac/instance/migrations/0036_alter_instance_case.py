# Generated by Django 3.2.12 on 2022-04-04 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('caluma_workflow', '0029_task_continue_async'),
        ('instance', '0035_form_family'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instance',
            name='case',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='instance', to='caluma_workflow.case'),
        ),
    ]
