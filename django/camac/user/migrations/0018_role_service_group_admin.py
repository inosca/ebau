# Generated by Django 3.2.15 on 2022-10-12 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_django_admin'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='role',
            options={'managed': True, 'verbose_name': 'Rolle', 'verbose_name_plural': 'Rollen'},
        ),
        migrations.AlterModelOptions(
            name='servicegroup',
            options={'managed': True, 'verbose_name': 'Organisationstyp', 'verbose_name_plural': 'Organisationstypen'},
        ),
        migrations.AlterField(
            model_name='role',
            name='group_prefix',
            field=models.CharField(blank=True, db_column='GROUP_PREFIX', max_length=100, null=True, verbose_name='Gruppenpräfix'),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(blank=True, db_column='NAME', max_length=100, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='role',
            name='role_id',
            field=models.AutoField(db_column='ROLE_ID', primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='role',
            name='role_parent',
            field=models.ForeignKey(blank=True, db_column='ROLE_PARENT_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='user.role', verbose_name='Übergeordnete Rolle'),
        ),
        migrations.AlterField(
            model_name='rolet',
            name='group_prefix',
            field=models.CharField(blank=True, db_column='GROUP_PREFIX', max_length=100, null=True, verbose_name='Gruppenpräfix'),
        ),
        migrations.AlterField(
            model_name='rolet',
            name='language',
            field=models.CharField(db_column='LANGUAGE', max_length=2, verbose_name='Sprache'),
        ),
        migrations.AlterField(
            model_name='rolet',
            name='name',
            field=models.CharField(blank=True, db_column='NAME', max_length=100, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='servicegroup',
            name='name',
            field=models.CharField(blank=True, db_column='NAME', max_length=100, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='servicegroup',
            name='service_group_id',
            field=models.AutoField(db_column='SERVICE_GROUP_ID', primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='servicegroupt',
            name='language',
            field=models.CharField(db_column='LANGUAGE', max_length=2, verbose_name='Sprache'),
        ),
        migrations.AlterField(
            model_name='servicegroupt',
            name='name',
            field=models.CharField(blank=True, db_column='NAME', max_length=100, null=True, verbose_name='Name'),
        ),
    ]