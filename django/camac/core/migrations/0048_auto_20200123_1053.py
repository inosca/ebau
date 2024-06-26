# Generated by Django 2.2.8 on 2020-01-23 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0047_sanction_control_instance'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='publication_amtsblatt',
            field=models.DateField(blank=True, db_column='PUBLICATION_DATE_AMTSBLATT', null=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='publication_anzeiger_1',
            field=models.DateField(blank=True, db_column='PUBLICATION_DATE_1_ANZEIGER', null=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='publication_anzeiger_2',
            field=models.DateField(blank=True, db_column='PUBLICATION_DATE_2_ANZEIGER', null=True),
        ),
    ]
