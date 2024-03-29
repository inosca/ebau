# Generated by Django 3.2.15 on 2022-10-11 10:41

from django.conf import settings
import django.contrib.postgres.fields.citext
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_set_superuser_and_is_staff'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'managed': True, 'verbose_name': 'Gruppe', 'verbose_name_plural': 'Gruppen'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'managed': True, 'ordering': ['service_group__name'], 'verbose_name': 'Organisation', 'verbose_name_plural': 'Organisationen'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'managed': True, 'verbose_name': 'Benutzer', 'verbose_name_plural': 'Benutzer'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.AlterField(
            model_name='group',
            name='address',
            field=models.CharField(blank=True, db_column='ADDRESS', max_length=100, null=True, verbose_name='Adresse'),
        ),
        migrations.AlterField(
            model_name='group',
            name='city',
            field=models.CharField(blank=True, db_column='CITY', max_length=100, null=True, verbose_name='Ort'),
        ),
        migrations.AlterField(
            model_name='group',
            name='disabled',
            field=models.PositiveSmallIntegerField(db_column='DISABLED', default=0, verbose_name='Deaktiviert?'),
        ),
        migrations.AlterField(
            model_name='group',
            name='email',
            field=models.CharField(blank=True, db_column='EMAIL', max_length=100, null=True, verbose_name='E-Mail-Adresse'),
        ),
        migrations.AlterField(
            model_name='group',
            name='group_id',
            field=models.AutoField(db_column='GROUP_ID', primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='group',
            name='locations',
            field=models.ManyToManyField(through='user.GroupLocation', to='user.Location', verbose_name='Standorte'),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(blank=True, db_column='NAME', max_length=100, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='group',
            name='phone',
            field=models.CharField(blank=True, db_column='PHONE', max_length=100, null=True, verbose_name='Telefon'),
        ),
        migrations.AlterField(
            model_name='group',
            name='role',
            field=models.ForeignKey(db_column='ROLE_ID', on_delete=django.db.models.deletion.PROTECT, related_name='groups', to='user.role', verbose_name='Rolle'),
        ),
        migrations.AlterField(
            model_name='group',
            name='service',
            field=models.ForeignKey(blank=True, db_column='SERVICE_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='groups', to='user.service', verbose_name='Organisation'),
        ),
        migrations.AlterField(
            model_name='group',
            name='website',
            field=models.CharField(blank=True, db_column='WEBSITE', max_length=1000, null=True, verbose_name='Website'),
        ),
        migrations.AlterField(
            model_name='group',
            name='zip',
            field=models.CharField(blank=True, db_column='ZIP', max_length=10, null=True, verbose_name='PLZ'),
        ),
        migrations.AlterField(
            model_name='grouplocation',
            name='group',
            field=models.ForeignKey(db_column='GROUP_ID', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='user.group', verbose_name='Gruppe'),
        ),
        migrations.AlterField(
            model_name='grouplocation',
            name='location',
            field=models.ForeignKey(db_column='LOCATION_ID', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='user.location', verbose_name='Standort'),
        ),
        migrations.AlterField(
            model_name='groupt',
            name='city',
            field=models.CharField(blank=True, db_column='CITY', max_length=100, null=True, verbose_name='Ort'),
        ),
        migrations.AlterField(
            model_name='groupt',
            name='group',
            field=models.ForeignKey(db_column='GROUP_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='user.group', verbose_name='Gruppe'),
        ),
        migrations.AlterField(
            model_name='groupt',
            name='language',
            field=models.CharField(db_column='LANGUAGE', max_length=2, verbose_name='Sprache'),
        ),
        migrations.AlterField(
            model_name='groupt',
            name='name',
            field=models.CharField(blank=True, db_column='NAME', max_length=200, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='service',
            name='address',
            field=models.CharField(blank=True, db_column='ADDRESS', max_length=100, null=True, verbose_name='Adresse'),
        ),
        migrations.AlterField(
            model_name='service',
            name='city',
            field=models.CharField(blank=True, db_column='CITY', max_length=100, null=True, verbose_name='Ort'),
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.CharField(blank=True, db_column='DESCRIPTION', max_length=255, null=True, verbose_name='Beschreibung'),
        ),
        migrations.AlterField(
            model_name='service',
            name='disabled',
            field=models.PositiveSmallIntegerField(db_column='DISABLED', default=0, verbose_name='Deaktiviert?'),
        ),
        migrations.AlterField(
            model_name='service',
            name='email',
            field=models.CharField(blank=True, db_column='EMAIL', max_length=1000, null=True, verbose_name='E-Mail-Adresse'),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(blank=True, db_column='NAME', max_length=100, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='service',
            name='notification',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Notifikationen empfangen?'),
        ),
        migrations.AlterField(
            model_name='service',
            name='phone',
            field=models.CharField(blank=True, db_column='PHONE', max_length=100, null=True, verbose_name='Telefon'),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_group',
            field=models.ForeignKey(db_column='SERVICE_GROUP_ID', on_delete=django.db.models.deletion.PROTECT, related_name='+', to='user.servicegroup', verbose_name='Organisationstyp'),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_id',
            field=models.AutoField(db_column='SERVICE_ID', primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_parent',
            field=models.ForeignKey(blank=True, db_column='SERVICE_PARENT_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='user.service', verbose_name='Übergeordnete Organisation'),
        ),
        migrations.AlterField(
            model_name='service',
            name='website',
            field=models.CharField(blank=True, db_column='WEBSITE', max_length=1000, null=True, verbose_name='Website'),
        ),
        migrations.AlterField(
            model_name='service',
            name='zip',
            field=models.CharField(blank=True, db_column='ZIP', max_length=10, null=True, verbose_name='PLZ'),
        ),
        migrations.AlterField(
            model_name='servicet',
            name='city',
            field=models.CharField(blank=True, db_column='CITY', max_length=100, null=True, verbose_name='Ort'),
        ),
        migrations.AlterField(
            model_name='servicet',
            name='description',
            field=models.CharField(blank=True, db_column='DESCRIPTION', max_length=255, null=True, verbose_name='Beschreibung'),
        ),
        migrations.AlterField(
            model_name='servicet',
            name='language',
            field=models.CharField(db_column='LANGUAGE', max_length=2, verbose_name='Sprache'),
        ),
        migrations.AlterField(
            model_name='servicet',
            name='name',
            field=models.CharField(blank=True, db_column='NAME', max_length=200, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, db_column='ADDRESS', max_length=100, null=True, verbose_name='Adresse'),
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, db_column='CITY', max_length=100, null=True, verbose_name='Ort'),
        ),
        migrations.AlterField(
            model_name='user',
            name='disabled',
            field=models.PositiveSmallIntegerField(db_column='DISABLED', default=0, verbose_name='Deaktiviert?'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=django.contrib.postgres.fields.citext.CIEmailField(blank=True, db_column='EMAIL', max_length=100, null=True, verbose_name='E-Mail-Adresse'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(db_column='USER_ID', primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(db_column='LANGUAGE', max_length=2, verbose_name='Sprache'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, db_column='LAST_REQUEST_DATE', null=True, verbose_name='Letztes Login'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(db_column='NAME', max_length=100, verbose_name='Vorname'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, db_column='PHONE', max_length=100, null=True, verbose_name='Telefon'),
        ),
        migrations.AlterField(
            model_name='user',
            name='surname',
            field=models.CharField(db_column='SURNAME', max_length=100, verbose_name='Nachname'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(db_column='USERNAME', max_length=250, unique=True, verbose_name='Benutzername'),
        ),
        migrations.AlterField(
            model_name='user',
            name='zip',
            field=models.CharField(blank=True, db_column='ZIP', max_length=10, null=True, verbose_name='PLZ'),
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='default_group',
            field=models.PositiveSmallIntegerField(db_column='DEFAULT_GROUP', verbose_name='Standardgruppe?'),
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='group',
            field=models.ForeignKey(db_column='GROUP_ID', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='user.group', verbose_name='Gruppe'),
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='user',
            field=models.ForeignKey(db_column='USER_ID', on_delete=django.db.models.deletion.CASCADE, related_name='user_groups', to=settings.AUTH_USER_MODEL, verbose_name='Benutzer'),
        ),
    ]
