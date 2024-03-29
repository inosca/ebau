# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-26 08:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_fix_reversion_foreign_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acirculationemailt',
            name='action',
            field=models.ForeignKey(db_column='ACTION_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.ACirculationEmail'),
        ),
        migrations.AlterField(
            model_name='actiont',
            name='action',
            field=models.ForeignKey(db_column='ACTION_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.Action'),
        ),
        migrations.AlterField(
            model_name='aemailt',
            name='action',
            field=models.ForeignKey(db_column='ACTION_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.AEmail'),
        ),
        migrations.AlterField(
            model_name='aproposalt',
            name='action',
            field=models.ForeignKey(db_column='ACTION_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.AProposal'),
        ),
        migrations.AlterField(
            model_name='buttont',
            name='button',
            field=models.ForeignKey(db_column='BUTTON_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.Button'),
        ),
        migrations.AlterField(
            model_name='circulationanswert',
            name='circulation_answer',
            field=models.ForeignKey(db_column='CIRCULATION_ANSWER_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.CirculationAnswer'),
        ),
        migrations.AlterField(
            model_name='circulationanswertypet',
            name='circulation_answer_type',
            field=models.ForeignKey(db_column='CIRCULATION_ANSWER_TYPE_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.CirculationAnswerType'),
        ),
        migrations.AlterField(
            model_name='circulationreasont',
            name='circulation_reason',
            field=models.ForeignKey(db_column='CIRCULATION_REASON_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.CirculationReason'),
        ),
        migrations.AlterField(
            model_name='circulationstatet',
            name='circulation_state_id',
            field=models.ForeignKey(db_column='CIRCULATION_STATE_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.CirculationState'),
        ),
        migrations.AlterField(
            model_name='circulationtypet',
            name='circulation_type',
            field=models.ForeignKey(db_column='CIRCULATION_TYPE_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.CirculationType'),
        ),
        migrations.AlterField(
            model_name='formgroupt',
            name='form_group',
            field=models.ForeignKey(db_column='FORM_GROUP_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.FormGroup'),
        ),
        migrations.AlterField(
            model_name='instanceresourcet',
            name='instance_resource',
            field=models.ForeignKey(db_column='INSTANCE_RESOURCE_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.InstanceResource'),
        ),
        migrations.AlterField(
            model_name='ireditcirculationt',
            name='instance_resource',
            field=models.ForeignKey(db_column='INSTANCE_RESOURCE_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.IrEditcirculation'),
        ),
        migrations.AlterField(
            model_name='ireditletteranswert',
            name='ir_editletter_answer',
            field=models.ForeignKey(db_column='IR_EDITLETTER_ANSWER_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.IrEditletterAnswer'),
        ),
        migrations.AlterField(
            model_name='irformwizardt',
            name='instance_resource',
            field=models.ForeignKey(db_column='INSTANCE_RESOURCE_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.IrFormwizard'),
        ),
        migrations.AlterField(
            model_name='journalactionconfigt',
            name='action',
            field=models.ForeignKey(db_column='ACTION_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.JournalActionConfig'),
        ),
        migrations.AlterField(
            model_name='noticetypet',
            name='notice_type',
            field=models.ForeignKey(db_column='NOTICE_TYPE_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.NoticeType'),
        ),
        migrations.AlterField(
            model_name='pageformgroupt',
            name='page_form_group',
            field=models.ForeignKey(db_column='PAGE_FORM_GROUP_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.PageFormGroup'),
        ),
        migrations.AlterField(
            model_name='resourcet',
            name='resource',
            field=models.ForeignKey(db_column='RESOURCE_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.Resource'),
        ),
        migrations.AlterField(
            model_name='rlistcolumnt',
            name='r_list_column',
            field=models.ForeignKey(db_column='R_LIST_COLUMN_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.RListColumn'),
        ),
        migrations.AlterField(
            model_name='rsearchcolumnt',
            name='r_search_column',
            field=models.ForeignKey(db_column='R_SEARCH_COLUMN_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.RSearchColumn'),
        ),
        migrations.AlterField(
            model_name='rsearchfiltert',
            name='r_search_filter',
            field=models.ForeignKey(db_column='R_SEARCH_FILTER_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='core.RSearchFilter'),
        ),
    ]
