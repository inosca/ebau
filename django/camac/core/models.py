from django.db import models


class ACheckquery(models.Model):
    action = models.OneToOneField('Action', models.CASCADE,
                                  db_column='ACTION_ID', primary_key=True,
                                  related_name='+')
    query = models.CharField(db_column='QUERY', max_length=4000)

    class Meta:
        managed = True
        db_table = 'A_CHECKQUERY'


class ACirculationEmail(models.Model):
    action = models.OneToOneField('Action', models.CASCADE,
                                  db_column='ACTION_ID', primary_key=True,
                                  related_name='+')
    sender_name = models.CharField(db_column='SENDER_NAME', max_length=50)
    sender_email = models.CharField(db_column='SENDER_EMAIL', max_length=50)
    title = models.CharField(db_column='TITLE', max_length=200)
    text = models.CharField(db_column='TEXT', max_length=2000)

    class Meta:
        managed = True
        db_table = 'A_CIRCULATION_EMAIL'


class ACirculationtransition(models.Model):
    action = models.OneToOneField('Action', models.CASCADE,
                                  db_column='ACTION_ID', primary_key=True,
                                  related_name='+')
    current_circulation_state = models.ForeignKey(
        'CirculationState', models.CASCADE,
        db_column='CURRENT_CIRCULATION_STATE_ID', related_name='+', blank=True,
        null=True)
    next_circulation_state = models.ForeignKey(
        'CirculationState', models.CASCADE,
        db_column='NEXT_CIRCULATION_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'A_CIRCULATIONTRANSITION'


class ACopyanswer(models.Model):
    action = models.OneToOneField('Action', models.CASCADE,
                                  db_column='ACTION_ID', primary_key=True,
                                  related_name='+')

    class Meta:
        managed = True
        db_table = 'A_COPYANSWER'


class ACopyanswerMapping(models.Model):
    a_copyanswer_mapping_id = models.AutoField(
        db_column='A_COPYANSWER_MAPPING_ID', primary_key=True)
    action = models.ForeignKey(
        ACopyanswer, models.CASCADE, db_column='ACTION_ID',
        related_name='+')
    source_chapter = models.ForeignKey(
        'Chapter', models.CASCADE, db_column='SOURCE_CHAPTER_ID',
        related_name='+', blank=True, null=True)
    source_question = models.ForeignKey(
        'Question', models.CASCADE, db_column='SOURCE_QUESTION_ID',
        related_name='+', blank=True, null=True)
    destination_chapter = models.ForeignKey(
        'Chapter', models.CASCADE, db_column='DESTINATION_CHAPTER_ID',
        related_name='+')
    destination_question = models.ForeignKey(
        'Question', models.CASCADE, db_column='DESTINATION_QUESTION_ID',
        related_name='+')
    get_name = models.PositiveSmallIntegerField(db_column='GET_NAME')

    class Meta:
        managed = True
        db_table = 'A_COPYANSWER_MAPPING'


class ACopydata(models.Model):
    action = models.OneToOneField('Action', models.CASCADE,
                                  db_column='ACTION_ID', primary_key=True,
                                  related_name='+')

    class Meta:
        managed = True
        db_table = 'A_COPYDATA'


class ACopydataMapping(models.Model):
    a_copydata_mapping_id = models.AutoField(
        db_column='A_COPYDATA_MAPPING_ID', primary_key=True)
    action = models.ForeignKey(
        ACopydata, models.CASCADE, db_column='ACTION_ID', related_name='+')
    question = models.ForeignKey('Question', models.CASCADE,
                                 db_column='QUESTION_ID', related_name='+',
                                 blank=True, null=True)
    chapter = models.ForeignKey('Chapter', models.CASCADE,
                                db_column='CHAPTER_ID', related_name='+',
                                blank=True, null=True)
    table_name = models.CharField(db_column='TABLE_NAME', max_length=30)
    column_name = models.CharField(db_column='COLUMN_NAME', max_length=30)
    get_name = models.PositiveSmallIntegerField(db_column='GET_NAME')

    class Meta:
        managed = True
        db_table = 'A_COPYDATA_MAPPING'


class ADeleteCirculation(models.Model):
    action = models.OneToOneField('Action', models.CASCADE,
                                  db_column='ACTION_ID', primary_key=True,
                                  related_name='+')
    delete_level = models.IntegerField(db_column='DELETE_LEVEL')

    class Meta:
        managed = True
        db_table = 'A_DELETE_CIRCULATION'


class AEmail(models.Model):
    action = models.OneToOneField('Action', models.CASCADE,
                                  db_column='ACTION_ID', primary_key=True,
                                  related_name='+')
    sender_name = models.CharField(db_column='SENDER_NAME', max_length=50)
    sender_email = models.CharField(db_column='SENDER_EMAIL', max_length=50)
    query = models.CharField(db_column='QUERY', max_length=4000)
    title = models.CharField(db_column='TITLE', max_length=200)
    text = models.CharField(db_column='TEXT', max_length=2000)

    class Meta:
        managed = True
        db_table = 'A_EMAIL'


class AFormtransition(models.Model):
    action = models.OneToOneField('Action', models.CASCADE,
                                  db_column='ACTION_ID', primary_key=True,
                                  related_name='+')
    current_instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='CURRENT_INSTANCE_STATE_ID', related_name='+', blank=True,
        null=True)
    next_instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='NEXT_INSTANCE_STATE_ID',
        related_name='+', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'A_FORMTRANSITION'


class ANotification(models.Model):
    action = models.OneToOneField('core.Action', models.CASCADE,
                                  db_column='ACTION_ID', primary_key=True,
                                  related_name='+')
    template = models.ForeignKey('notification.NotificationTemplate',
                                 models.CASCADE, db_column='TEMPLATE_ID',
                                 related_name='+')
    recipient_type = models.CharField(
        db_column='RECIPIENT_TYPE', max_length=160
    )
    processor = models.CharField(db_column='PROCESSOR', max_length=160)

    class Meta:
        managed  = True
        db_table = 'ACTION_NOTIFICATION'


class ALocation(models.Model):
    action = models.OneToOneField('Action', models.CASCADE,
                                  db_column='ACTION_ID', primary_key=True,
                                  related_name='+')

    class Meta:
        managed = True
        db_table = 'A_LOCATION'


class ALocationQc(models.Model):
    a_location_qc_id = models.AutoField(
        db_column='A_LOCATION_QC_ID', primary_key=True)
    action = models.ForeignKey(
        ALocation, models.CASCADE, db_column='ACTION_ID', related_name='+')
    question = models.ForeignKey(
        'Question', models.CASCADE, db_column='QUESTION_ID',
        related_name='+')
    chapter = models.ForeignKey(
        'Chapter', models.CASCADE, db_column='CHAPTER_ID',
        related_name='+')

    class Meta:
        managed = True
        db_table = 'A_LOCATION_QC'


class ANotice(models.Model):
    action = models.OneToOneField('Action', models.CASCADE,
                                  db_column='ACTION_ID', primary_key=True,
                                  related_name='+')
    notice_type = models.ForeignKey(
        'NoticeType', models.CASCADE, db_column='NOTICE_TYPE_ID',
        related_name='+')
    query = models.CharField(db_column='QUERY', max_length=4000)

    class Meta:
        managed = True
        db_table = 'A_NOTICE'


class APageredirect(models.Model):
    action = models.OneToOneField('Action', models.CASCADE,
                                  db_column='ACTION_ID', primary_key=True,
                                  related_name='+')
    resource = models.ForeignKey(
        'Resource', models.CASCADE, db_column='RESOURCE_ID',
        related_name='+')
    instance_resource = models.ForeignKey('InstanceResource',
                                          models.CASCADE,
                                          db_column='INSTANCE_RESOURCE_ID',
                                          related_name='+', blank=True,
                                          null=True)
    air_action_name = models.CharField(
        db_column='AIR_ACTION_NAME', max_length=25, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'A_PAGEREDIRECT'


class APhp(models.Model):
    action = models.OneToOneField('Action', models.CASCADE,
                                  db_column='ACTION_ID', primary_key=True,
                                  related_name='+')
    php_class = models.CharField(db_column='PHP_CLASS', max_length=500)

    class Meta:
        managed = True
        db_table = 'A_PHP'


class AProposal(models.Model):
    action = models.OneToOneField('Action', models.CASCADE,
                                  db_column='ACTION_ID', primary_key=True,
                                  related_name='+')
    circulation_type = models.ForeignKey(
        'CirculationType', models.CASCADE, db_column='CIRCULATION_TYPE_ID',
        related_name='+')
    circulation_state = models.ForeignKey(
        'CirculationState', models.CASCADE,
        db_column='CIRCULATION_STATE_ID', related_name='+')
    deadline_days = models.IntegerField(db_column='DEADLINE_DAYS')
    reason = models.CharField(
        db_column='REASON', max_length=50, blank=True, null=True)
    is_working_days = models.PositiveSmallIntegerField(
        db_column='IS_WORKING_DAYS')

    class Meta:
        managed = True
        db_table = 'A_PROPOSAL'


class AProposalHoliday(models.Model):
    a_proposal_holiday_id = models.AutoField(
        db_column='A_PROPOSAL_HOLIDAY_ID', primary_key=True)
    holiday_date = models.DateTimeField(db_column='HOLIDAY_DATE')

    class Meta:
        managed = True
        db_table = 'A_PROPOSAL_HOLIDAY'


class ASavepdf(models.Model):
    action = models.OneToOneField('Action', models.CASCADE,
                                  db_column='ACTION_ID', primary_key=True,
                                  related_name='+')
    form = models.ForeignKey('instance.Form', models.CASCADE,
                             db_column='FORM_ID', related_name='+')
    page_form_group = models.ForeignKey('PageFormGroup', models.CASCADE,
                                        db_column='PAGE_FORM_GROUP_ID',
                                        related_name='+', blank=True,
                                        null=True)
    show_all_page_form_mode = models.PositiveSmallIntegerField(
        db_column='SHOW_ALL_PAGE_FORM_MODE')
    template = models.CharField(db_column='TEMPLATE', max_length=500)
    pdf_class = models.CharField(db_column='PDF_CLASS', max_length=500)

    class Meta:
        managed = True
        db_table = 'A_SAVEPDF'


class AValidate(models.Model):
    action = models.OneToOneField('Action', models.CASCADE,
                                  db_column='ACTION_ID', primary_key=True,
                                  related_name='+')
    page_form_group = models.ForeignKey('PageFormGroup', models.CASCADE,
                                        db_column='PAGE_FORM_GROUP_ID',
                                        related_name='+', blank=True,
                                        null=True)

    class Meta:
        managed = True
        db_table = 'A_VALIDATE'


class Action(models.Model):
    action_id = models.AutoField(db_column='ACTION_ID', primary_key=True)
    available_action = models.ForeignKey(
        'AvailableAction', models.CASCADE, db_column='AVAILABLE_ACTION_ID',
        related_name='+')
    button = models.ForeignKey(
        'Button', models.CASCADE, db_column='BUTTON_ID', related_name='+')
    name = models.CharField(db_column='NAME', max_length=50)
    description = models.CharField(
        db_column='DESCRIPTION', max_length=1000, blank=True, null=True)
    success_message = models.CharField(
        db_column='SUCCESS_MESSAGE', max_length=1000, blank=True, null=True)
    error_message = models.CharField(
        db_column='ERROR_MESSAGE', max_length=1000, blank=True, null=True)
    execute_always = models.PositiveSmallIntegerField(
        db_column='EXECUTE_ALWAYS')
    sort = models.IntegerField(db_column='SORT')

    class Meta:
        managed = True
        db_table = 'ACTION'


class Activation(models.Model):
    activation_id = models.AutoField(
        db_column='ACTIVATION_ID', primary_key=True)
    circulation = models.ForeignKey(
        'Circulation', models.DO_NOTHING, db_column='CIRCULATION_ID',
        related_name='activations')
    service = models.ForeignKey(
        'user.Service', models.DO_NOTHING, db_column='SERVICE_ID',
        related_name='+')
    service_parent = models.ForeignKey(
        'user.Service', models.DO_NOTHING, db_column='SERVICE_PARENT_ID',
        related_name='+')
    circulation_state = models.ForeignKey(
        'CirculationState', models.DO_NOTHING,
        db_column='CIRCULATION_STATE_ID', related_name='+')
    user = models.ForeignKey('user.User', models.DO_NOTHING,
                             db_column='USER_ID', related_name='+', blank=True,
                             null=True)
    circulation_answer = models.ForeignKey(
        'CirculationAnswer', models.DO_NOTHING,
        db_column='CIRCULATION_ANSWER_ID', related_name='+', blank=True,
        null=True)
    start_date = models.DateTimeField(db_column='START_DATE')
    deadline_date = models.DateTimeField(db_column='DEADLINE_DATE')
    suspension_date = models.DateTimeField(
        db_column='SUSPENSION_DATE', blank=True, null=True)
    end_date = models.DateTimeField(
        db_column='END_DATE', blank=True, null=True)
    version = models.IntegerField(db_column='VERSION')
    reason = models.CharField(
        db_column='REASON', max_length=50, blank=True, null=True)
    activation_parent = models.ForeignKey(
        'self', models.DO_NOTHING, db_column='ACTIVATION_PARENT_ID',
        related_name='+', blank=True, null=True)
    email_sent = models.PositiveSmallIntegerField(
        db_column='EMAIL_SENT', default=1)

    class Meta:
        managed = True
        db_table = 'ACTIVATION'


class ActivationAnswer(models.Model):
    activation = models.ForeignKey(
        Activation, models.DO_NOTHING, db_column='ACTIVATION_ID',
        related_name='+')
    question = models.ForeignKey(
        'Question', models.DO_NOTHING, db_column='QUESTION_ID',
        related_name='+')
    chapter = models.ForeignKey(
        'Chapter', models.DO_NOTHING, db_column='CHAPTER_ID', related_name='+')
    item = models.IntegerField(db_column='ITEM')
    answer = models.CharField(db_column='ANSWER', max_length=4000)

    class Meta:
        managed = True
        db_table = 'ACTIVATION_ANSWER'
        unique_together = (('activation', 'question', 'chapter', 'item'),)


class ActivationAnswerLog(models.Model):
    activation_answer_log_id = models.AutoField(
        db_column='ACTIVATION_ANSWER_LOG_ID', primary_key=True)
    modification_date = models.DateTimeField(db_column='MODIFICATION_DATE')
    user_id = models.IntegerField(db_column='USER_ID')
    action = models.CharField(db_column='ACTION', max_length=500)
    data = models.TextField(db_column='DATA')
    id1 = models.IntegerField(db_column='ID1')
    field1 = models.CharField(db_column='FIELD1', max_length=30)
    id2 = models.IntegerField(db_column='ID2')
    field2 = models.CharField(db_column='FIELD2', max_length=30)
    id3 = models.IntegerField(db_column='ID3')
    field3 = models.CharField(db_column='FIELD3', max_length=30)
    id4 = models.IntegerField(db_column='ID4')
    field4 = models.CharField(db_column='FIELD4', max_length=30)

    class Meta:
        managed = True
        db_table = 'ACTIVATION_ANSWER_LOG'


class ActivationLog(models.Model):
    activation_log_id = models.AutoField(
        db_column='ACTIVATION_LOG_ID', primary_key=True)
    id = models.IntegerField(db_column='ID')
    user_id = models.IntegerField(db_column='USER_ID')
    action = models.CharField(db_column='ACTION', max_length=500)
    data = models.TextField(db_column='DATA', blank=True, null=True)
    modification_date = models.DateTimeField(db_column='MODIFICATION_DATE')

    class Meta:
        managed = True
        db_table = 'ACTIVATION_LOG'


class AirAction(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    available_instance_resource = models.ForeignKey(
        'AvailableInstanceResource', models.CASCADE,
        db_column='AVAILABLE_INSTANCE_RESOURCE_ID', related_name='+')
    action_name = models.CharField(db_column='ACTION_NAME', max_length=50)
    hidden = models.PositiveSmallIntegerField(db_column='HIDDEN')

    class Meta:
        managed = True
        db_table = 'AIR_ACTION'
        unique_together = (('available_instance_resource', 'action_name'),)


class Answer(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instance = models.ForeignKey(
        'instance.Instance', models.DO_NOTHING, db_column='INSTANCE_ID',
        related_name='+')
    question = models.ForeignKey(
        'Question', models.DO_NOTHING, db_column='QUESTION_ID',
        related_name='+')
    chapter = models.ForeignKey(
        'Chapter', models.DO_NOTHING, db_column='CHAPTER_ID', related_name='+')
    item = models.IntegerField(db_column='ITEM')
    answer = models.CharField(db_column='ANSWER', max_length=4000)

    class Meta:
        managed = True
        db_table = 'ANSWER'
        unique_together = (('instance', 'question', 'chapter', 'item'),)


class AnswerList(models.Model):
    answer_list_id = models.AutoField(
        db_column='ANSWER_LIST_ID', primary_key=True)
    question = models.ForeignKey(
        'Question', models.CASCADE, db_column='QUESTION_ID',
        related_name='+')
    value = models.CharField(db_column='VALUE', max_length=20)
    name = models.CharField(db_column='NAME', max_length=300)
    sort = models.IntegerField(db_column='SORT')

    class Meta:
        managed = True
        db_table = 'ANSWER_LIST'


class AnswerLog(models.Model):
    answer_log_id = models.AutoField(
        db_column='ANSWER_LOG_ID', primary_key=True)
    modification_date = models.DateTimeField(db_column='MODIFICATION_DATE')
    user_id = models.IntegerField(db_column='USER_ID')
    action = models.CharField(db_column='ACTION', max_length=500)
    data = models.TextField(db_column='DATA', blank=True, null=True)
    id1 = models.IntegerField(db_column='ID1')
    field1 = models.CharField(db_column='FIELD1', max_length=30)
    id2 = models.IntegerField(db_column='ID2')
    field2 = models.CharField(db_column='FIELD2', max_length=30)
    id3 = models.IntegerField(db_column='ID3')
    field3 = models.CharField(db_column='FIELD3', max_length=30)
    id4 = models.IntegerField(db_column='ID4')
    field4 = models.CharField(db_column='FIELD4', max_length=30)

    class Meta:
        managed = True
        db_table = 'ANSWER_LOG'


class AnswerQuery(models.Model):
    answer_query_id = models.AutoField(
        db_column='ANSWER_QUERY_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=50)
    query = models.CharField(db_column='QUERY', max_length=4000)

    class Meta:
        managed = True
        db_table = 'ANSWER_QUERY'


class ArAction(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    available_resource = models.ForeignKey(
        'AvailableResource', models.CASCADE,
        db_column='AVAILABLE_RESOURCE_ID', related_name='+')
    action_name = models.CharField(db_column='ACTION_NAME', max_length=50)
    hidden = models.PositiveSmallIntegerField(db_column='HIDDEN')

    class Meta:
        managed = True
        db_table = 'AR_ACTION'
        unique_together = (('available_resource', 'action_name'),)


class Authority(models.Model):
    authority_id = models.AutoField(db_column='AUTHORITY_ID', primary_key=True)
    name = models.CharField(
        db_column='NAME', max_length=128, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'AUTHORITY'


class AuthorityAuthorityType(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    authority = models.ForeignKey(
        Authority, models.CASCADE,
        db_column='AUTHORITY_ID', related_name='+'
    )
    authority_type = models.ForeignKey(
        'AuthorityType', models.CASCADE,
        db_column='AUTHORITY_TYPE_ID', related_name='+'
    )

    class Meta:
        managed = True
        db_table = 'AUTHORITY_AUTHORITY_TYPE'


class AuthorityLocation(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    authority = models.ForeignKey(
        Authority, models.CASCADE, db_column='AUTHORITY_ID',
        related_name='+')
    location = models.ForeignKey(
        'user.Location', models.CASCADE, db_column='LOCATION_ID',
        related_name='+')

    class Meta:
        managed = True
        db_table = 'AUTHORITY_LOCATION'
        unique_together = (('authority', 'location'),)


class AuthorityType(models.Model):
    authority_type_id = models.AutoField(
        db_column='AUTHORITY_TYPE_ID', primary_key=True)
    tag = models.CharField(db_column='TAG', max_length=8)
    name = models.CharField(db_column='NAME', max_length=128)

    class Meta:
        managed = True
        db_table = 'AUTHORITY_TYPE'


class AvailableAction(models.Model):
    available_action_id = models.CharField(
        db_column='AVAILABLE_ACTION_ID', primary_key=True, max_length=25)
    module_name = models.CharField(db_column='MODULE_NAME', max_length=50)
    description = models.CharField(
        db_column='DESCRIPTION', max_length=1000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'AVAILABLE_ACTION'


class AvailableInstanceResource(models.Model):
    available_instance_resource_id = models.CharField(
        db_column='AVAILABLE_INSTANCE_RESOURCE_ID', primary_key=True,
        max_length=25)
    module_name = models.CharField(db_column='MODULE_NAME', max_length=50)
    controller_name = models.CharField(
        db_column='CONTROLLER_NAME', max_length=50)
    description = models.CharField(
        db_column='DESCRIPTION', max_length=1000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'AVAILABLE_INSTANCE_RESOURCE'


class AvailableResource(models.Model):
    available_resource_id = models.CharField(
        db_column='AVAILABLE_RESOURCE_ID', primary_key=True, max_length=25)
    module_name = models.CharField(db_column='MODULE_NAME', max_length=50)
    controller_name = models.CharField(
        db_column='CONTROLLER_NAME', max_length=50)
    description = models.CharField(
        db_column='DESCRIPTION', max_length=1000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'AVAILABLE_RESOURCE'


class BGroupAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    button = models.ForeignKey(
        'Button', models.CASCADE, db_column='BUTTON_ID', related_name='+')
    group = models.ForeignKey(
        'user.Group', models.CASCADE, db_column='GROUP_ID',
        related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'B_GROUP_ACL'
        unique_together = (('button', 'group', 'instance_state'),)


class BRoleAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    button = models.ForeignKey(
        'Button', models.CASCADE, db_column='BUTTON_ID', related_name='+')
    role = models.ForeignKey('user.Role', models.CASCADE,
                             db_column='ROLE_ID', related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'B_ROLE_ACL'
        unique_together = (('button', 'role', 'instance_state'),)


class BServiceAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    button = models.ForeignKey(
        'Button', models.CASCADE, db_column='BUTTON_ID', related_name='+')
    service = models.ForeignKey(
        'user.Service', models.CASCADE, db_column='SERVICE_ID',
        related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'B_SERVICE_ACL'
        unique_together = (('button', 'service', 'instance_state'),)


class BUserAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    button = models.ForeignKey(
        'Button', models.CASCADE, db_column='BUTTON_ID', related_name='+')
    user = models.ForeignKey('user.User', models.CASCADE,
                             db_column='USER_ID', related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'B_USER_ACL'
        unique_together = (('button', 'user', 'instance_state'),)


class BabUsage(models.Model):
    instance = models.ForeignKey(
        'instance.Instance', models.DO_NOTHING, db_column='INSTANCE_ID',
        related_name='+')
    usage_type = models.IntegerField(db_column='USAGE_TYPE')
    usage = models.FloatField(db_column='USAGE')

    class Meta:
        managed = True
        db_table = 'BAB_USAGE'
        unique_together = (('instance', 'usage_type'),)


class BillingAccount(models.Model):
    billing_account_id = models.AutoField(
        db_column='BILLING_ACCOUNT_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=500)
    account_number = models.CharField(
        db_column='ACCOUNT_NUMBER', max_length=50, blank=True, null=True)
    department = models.CharField(
        db_column='DEPARTMENT', max_length=255, blank=True, null=True)
    predefined = models.PositiveSmallIntegerField(db_column='PREDEFINED',
                                                  default=0)
    service_group = models.ForeignKey('user.ServiceGroup', models.CASCADE,
                                      db_column='SERVICE_GROUP_ID',
                                      related_name='+', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'BILLING_ACCOUNT'


class BillingAccountState(models.Model):
    billing_account_state_id = models.AutoField(
        db_column='BILLING_ACCOUNT_STATE_ID', primary_key=True)
    billing_account = models.ForeignKey(
        BillingAccount, models.CASCADE, db_column='BILLING_ACCOUNT_ID',
        related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'BILLING_ACCOUNT_STATE'


class BillingConfig(models.Model):
    billing_config_id = models.AutoField(
        db_column='BILLING_CONFIG_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=100)
    value = models.CharField(db_column='VALUE', max_length=300)

    class Meta:
        managed = True
        db_table = 'BILLING_CONFIG'


class BillingEntry(models.Model):
    billing_entry_id = models.AutoField(
        db_column='BILLING_ENTRY_ID', primary_key=True)
    amount = models.FloatField(db_column='AMOUNT')
    billing_account = models.ForeignKey(
        BillingAccount, models.DO_NOTHING, db_column='BILLING_ACCOUNT_ID',
        related_name='+')
    user = models.ForeignKey('user.User', models.CASCADE,
                             db_column='USER_ID',
                             related_name='+', default=1)
    instance = models.ForeignKey('instance.Instance', models.DO_NOTHING,
                                 db_column='INSTANCE_ID',
                                 related_name='billing_entries')
    service = models.ForeignKey('user.Service', models.DO_NOTHING,
                                db_column='SERVICE_ID', related_name='+',
                                blank=True, null=True)
    created = models.DateTimeField(db_column='CREATED', null=True)
    amount_type = models.PositiveSmallIntegerField(db_column='AMOUNT_TYPE')
    type = models.PositiveSmallIntegerField(db_column='TYPE')
    reason = models.CharField(
        db_column='REASON', max_length=300, blank=True, null=True)
    invoiced = models.PositiveSmallIntegerField(db_column='INVOICED')
    invoice = models.ForeignKey('BillingInvoice', models.DO_NOTHING,
                                db_column='INVOICE_ID', null=True,
                                related_name='billing_entries')

    class Meta:
        managed = True
        db_table = 'BILLING_ENTRY'


class BillingInvoice(models.Model):
    billing_invoice_id = models.AutoField(
        db_column='BILLING_INVOICE_ID', primary_key=True)
    created = models.DateTimeField(db_column='CREATED')
    attachment = models.ForeignKey('document.Attachment', models.DO_NOTHING,
                                   db_column='ATTACHMENT_ID',
                                   related_name='billing_invoices')
    type = models.TextField(db_column='TYPE')

    class Meta:
        managed = True
        db_table = 'BILLING_INVOICE'


class BuildingAuthorityButton(models.Model):
    building_authority_button_id = models.AutoField(
        db_column='BUILDING_AUTHORITY_BUTTON_ID', primary_key=True)
    label = models.CharField(db_column='LABEL', max_length=512)

    class Meta:
        managed = True
        db_table = 'BUILDING_AUTHORITY_BUTTON'


class BuildingAuthorityButtonstate(models.Model):
    ba_button_state_id = models.AutoField(
        db_column='BA_BUTTON_STATE_ID', primary_key=True)
    building_authority_button = models.ForeignKey(
        BuildingAuthorityButton, models.DO_NOTHING,
        db_column='BUILDING_AUTHORITY_BUTTON_ID', related_name='+')
    instance = models.ForeignKey(
        'instance.Instance', models.CASCADE, db_column='INSTANCE_ID',
        related_name='+')
    is_clicked = models.PositiveSmallIntegerField(db_column='IS_CLICKED',
                                                  default=0)
    is_disabled = models.PositiveSmallIntegerField(db_column='IS_DISABLED',
                                                   default=0)

    class Meta:
        managed = True
        db_table = 'BUILDING_AUTHORITY_BUTTONSTATE'


class BuildingAuthorityComment(models.Model):
    building_authority_comment_id = models.AutoField(
        db_column='BUILDING_AUTHORITY_COMMENT_ID', primary_key=True)
    building_authority_section = models.ForeignKey(
        'BuildingAuthoritySection', models.DO_NOTHING,
        db_column='BUILDING_AUTHORITY_SECTION_ID', related_name='+')
    text = models.CharField(
        db_column='TEXT', max_length=4000, blank=True, null=True)
    group = models.FloatField(db_column='GROUP')
    instance = models.ForeignKey(
        'instance.Instance', models.DO_NOTHING, db_column='INSTANCE_ID')

    class Meta:
        managed = True
        db_table = 'BUILDING_AUTHORITY_COMMENT'
        unique_together = (
            ('building_authority_section', 'group', 'instance'),)


class BuildingAuthorityDoc(models.Model):
    building_authority_doc_id = models.AutoField(
        db_column='BUILDING_AUTHORITY_DOC_ID', primary_key=True)
    building_authority_button = models.ForeignKey(
        BuildingAuthorityButton, models.CASCADE,
        db_column='BUILDING_AUTHORITY_BUTTON_ID', related_name='+')
    template_class = models.ForeignKey(
        'DocgenTemplateClass', models.CASCADE,
        db_column='TEMPLATE_CLASS_ID', related_name='+')
    template = models.ForeignKey(
        'DocgenTemplate', models.CASCADE, db_column='TEMPLATE_ID',
        related_name='+')

    class Meta:
        managed = True
        db_table = 'BUILDING_AUTHORITY_DOC'


class BuildingAuthorityEmail(models.Model):
    building_authority_email_id = models.AutoField(
        db_column='BUILDING_AUTHORITY_EMAIL_ID', primary_key=True)
    building_authority_button = models.ForeignKey(
        BuildingAuthorityButton, models.CASCADE,
        db_column='BUILDING_AUTHORITY_BUTTON_ID', related_name='+')
    email_text = models.CharField(
        db_column='EMAIL_TEXT', max_length=4000, blank=True, null=True)
    receiver_query = models.CharField(
        db_column='RECEIVER_QUERY', max_length=4000, blank=True, null=True)
    email_subject = models.CharField(
        db_column='EMAIL_SUBJECT', max_length=400, blank=True, null=True)
    from_email = models.CharField(
        db_column='FROM_EMAIL', max_length=400, blank=True, null=True)
    from_name = models.CharField(
        db_column='FROM_NAME', max_length=400, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'BUILDING_AUTHORITY_EMAIL'


class BuildingAuthorityItemDis(models.Model):
    ba_item_dis_id = models.AutoField(
        db_column='BA_ITEM_DIS_ID', primary_key=True)
    workflow_item = models.ForeignKey(
        'WorkflowItem', models.DO_NOTHING, db_column='WORKFLOW_ITEM_ID',
        related_name='+')
    instance = models.ForeignKey(
        'instance.Instance', models.DO_NOTHING, db_column='INSTANCE_ID',
        related_name='+')
    group = models.FloatField(db_column='GROUP')

    class Meta:
        managed = True
        db_table = 'BUILDING_AUTHORITY_ITEM_DIS'


class BuildingAuthoritySection(models.Model):
    building_authority_section_id = models.AutoField(
        db_column='BUILDING_AUTHORITY_SECTION_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=128)

    class Meta:
        managed = True
        db_table = 'BUILDING_AUTHORITY_SECTION'


class BuildingAuthoritySectionDis(models.Model):
    ba_section_dis_id = models.AutoField(
        db_column='BA_SECTION_DIS_ID', primary_key=True)
    instance = models.ForeignKey(
        'instance.Instance', models.DO_NOTHING, db_column='INSTANCE_ID',
        related_name='+')
    ba_section = models.ForeignKey(
        BuildingAuthoritySection, models.DO_NOTHING, db_column='BA_SECTION_ID',
        related_name='+')

    class Meta:
        managed = True
        db_table = 'BUILDING_AUTHORITY_SECTION_DIS'


class Button(models.Model):
    button_id = models.AutoField(db_column='BUTTON_ID', primary_key=True)
    instance_resource = models.ForeignKey(
        'InstanceResource', models.CASCADE,
        db_column='INSTANCE_RESOURCE_ID', related_name='+')
    name = models.CharField(db_column='NAME', max_length=50)
    description = models.CharField(
        db_column='DESCRIPTION', max_length=1000, blank=True, null=True)
    # Field renamed because it was a Python reserved word.
    class_field = models.CharField(
        db_column='CLASS', max_length=200, blank=True, null=True)
    hidden = models.PositiveSmallIntegerField(db_column='HIDDEN')
    sort = models.IntegerField(db_column='SORT')

    class Meta:
        managed = True
        db_table = 'BUTTON'


class Chapter(models.Model):
    chapter_id = models.AutoField(db_column='CHAPTER_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=500)
    description = models.CharField(
        db_column='DESCRIPTION', max_length=1000, blank=True, null=True)
    javascript = models.CharField(
        db_column='JAVASCRIPT', max_length=4000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'CHAPTER'


class ChapterPage(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    chapter = models.ForeignKey(
        Chapter, models.CASCADE, db_column='CHAPTER_ID', related_name='+')
    page = models.ForeignKey('Page', models.CASCADE,
                             db_column='PAGE_ID', related_name='+')
    sort = models.IntegerField(db_column='SORT')

    class Meta:
        managed = True
        db_table = 'CHAPTER_PAGE'
        unique_together = (('chapter', 'page'),)


class ChapterPageGroupAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    chapter = models.ForeignKey(
        ChapterPage, models.CASCADE, db_column='CHAPTER_ID',
        related_name='+')
    page = models.ForeignKey(
        ChapterPage, models.CASCADE, db_column='PAGE_ID', related_name='+')
    group = models.ForeignKey(
        'user.Group', models.CASCADE, db_column='GROUP_ID',
        related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'CHAPTER_PAGE_GROUP_ACL'
        unique_together = (('chapter', 'page', 'group', 'instance_state'),)


class ChapterPageRoleAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    chapter = models.ForeignKey(
        ChapterPage, models.CASCADE, db_column='CHAPTER_ID',
        related_name='+')
    page = models.ForeignKey(
        ChapterPage, models.CASCADE, db_column='PAGE_ID', related_name='+')
    role = models.ForeignKey('user.Role', models.CASCADE,
                             db_column='ROLE_ID', related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'CHAPTER_PAGE_ROLE_ACL'
        unique_together = (('chapter', 'page', 'role', 'instance_state'),)


class ChapterPageServiceAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    chapter = models.ForeignKey(
        ChapterPage, models.CASCADE, db_column='CHAPTER_ID',
        related_name='+')
    page = models.ForeignKey(
        ChapterPage, models.CASCADE, db_column='PAGE_ID', related_name='+')
    service = models.ForeignKey(
        'user.Service', models.CASCADE, db_column='SERVICE_ID',
        related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'CHAPTER_PAGE_SERVICE_ACL'
        unique_together = (('chapter', 'page', 'service', 'instance_state'),)


class ChapterPageUserAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    chapter = models.ForeignKey(
        ChapterPage, models.CASCADE, db_column='CHAPTER_ID',
        related_name='+')
    page = models.ForeignKey(
        ChapterPage, models.CASCADE, db_column='PAGE_ID', related_name='+')
    user = models.ForeignKey('user.User', models.CASCADE,
                             db_column='USER_ID', related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'CHAPTER_PAGE_USER_ACL'
        unique_together = (('chapter', 'page', 'user', 'instance_state'),)


class Circulation(models.Model):
    circulation_id = models.AutoField(
        db_column='CIRCULATION_ID', primary_key=True)
    # While this "should" be a foreign key, we decouple to be able
    # to separate config from data models
    # references IrEditcirculation
    instance_resource_id = models.IntegerField(
        db_column='INSTANCE_RESOURCE_ID', db_index=True)
    instance = models.ForeignKey(
        'instance.Instance', models.DO_NOTHING, db_column='INSTANCE_ID',
        related_name='circulations')
    name = models.CharField(db_column='NAME', max_length=50)

    class Meta:
        managed = True
        db_table = 'CIRCULATION'


class CirculationAnswer(models.Model):
    circulation_answer_id = models.AutoField(
        db_column='CIRCULATION_ANSWER_ID', primary_key=True)
    circulation_type = models.ForeignKey(
        'CirculationType', models.CASCADE, db_column='CIRCULATION_TYPE_ID',
        related_name='+')
    circulation_answer_type = models.ForeignKey(
        'CirculationAnswerType', models.CASCADE,
        db_column='CIRCULATION_ANSWER_TYPE_ID', related_name='+')
    name = models.CharField(db_column='NAME', max_length=50)
    sort = models.IntegerField(db_column='SORT')

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'CIRCULATION_ANSWER'


class CirculationAnswerType(models.Model):
    circulation_answer_type_id = models.AutoField(
        db_column='CIRCULATION_ANSWER_TYPE_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=50)

    class Meta:
        managed = True
        db_table = 'CIRCULATION_ANSWER_TYPE'


class CirculationLog(models.Model):
    circulation_log_id = models.AutoField(
        db_column='CIRCULATION_LOG_ID', primary_key=True)
    id = models.IntegerField(db_column='ID')
    user_id = models.IntegerField(db_column='USER_ID')
    action = models.CharField(db_column='ACTION', max_length=500)
    data = models.TextField(db_column='DATA', blank=True, null=True)
    modification_date = models.DateTimeField(db_column='MODIFICATION_DATE')

    class Meta:
        managed = True
        db_table = 'CIRCULATION_LOG'


class CirculationReason(models.Model):
    circulation_reason_id = models.AutoField(
        db_column='CIRCULATION_REASON_ID', primary_key=True)
    circulation_type = models.ForeignKey(
        'CirculationType', models.CASCADE, db_column='CIRCULATION_TYPE_ID',
        related_name='+')
    name = models.CharField(db_column='NAME', max_length=50)
    sort = models.IntegerField(db_column='SORT')

    class Meta:
        managed = True
        db_table = 'CIRCULATION_REASON'


class CirculationState(models.Model):
    circulation_state_id = models.AutoField(
        db_column='CIRCULATION_STATE_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=100)
    sort = models.IntegerField(db_column='SORT')

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'CIRCULATION_STATE'


class CirculationType(models.Model):
    circulation_type_id = models.AutoField(
        db_column='CIRCULATION_TYPE_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=50)
    # While this "should" be a foreign key, we decouple to be able
    # to separate config from data models
    # references Page
    page_id = models.IntegerField(
        db_column='PAGE_ID', db_index=True, null=True)
    parent_specific_activations = models.PositiveSmallIntegerField(
        db_column='PARENT_SPECIFIC_ACTIVATIONS')

    class Meta:
        managed = True
        db_table = 'CIRCULATION_TYPE'


class CommissionAssignment(models.Model):
    commission_assignment_id = models.AutoField(
        db_column='COMMISSION_ASSIGNMENT_ID', primary_key=True)
    group = models.ForeignKey(
        'user.Group', models.DO_NOTHING, db_column='GROUP_ID',
        related_name='+')
    instance = models.ForeignKey(
        'instance.Instance', models.DO_NOTHING, db_column='INSTANCE_ID',
        related_name='+')
    adder_id = models.FloatField(db_column='ADDER_ID')
    date = models.DateTimeField(db_column='DATE')

    class Meta:
        managed = True
        db_table = 'COMMISSION_ASSIGNMENT'
        unique_together = (('group', 'instance'),)


class DocgenActivationAction(models.Model):
    docgen_activation_action_id = models.AutoField(
        db_column='DOCGEN_ACTIVATION_ACTION_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=255)

    class Meta:
        managed = True
        db_table = 'DOCGEN_ACTIVATION_ACTION'


class DocgenActivationDocket(models.Model):
    docgen_activation_docket_id = models.AutoField(
        db_column='DOCGEN_ACTIVATION_DOCKET_ID', primary_key=True)
    instance = models.ForeignKey(
        'instance.Instance', models.CASCADE, db_column='INSTANCE_ID',
        related_name='+')
    activation = models.ForeignKey(
        Activation, models.CASCADE, db_column='ACTIVATION_ID',
        related_name='+', blank=True, null=True)
    text = models.TextField(db_column='TEXT')

    class Meta:
        managed = True
        db_table = 'DOCGEN_ACTIVATION_DOCKET'


class DocgenActivationactionAction(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    docgen_activation_action = models.ForeignKey(
        DocgenActivationAction, models.CASCADE,
        db_column='DOCGEN_ACTIVATION_ACTION_ID', related_name='+')
    action = models.ForeignKey(
        Action, models.CASCADE, db_column='ACTION_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'DOCGEN_ACTIVATIONACTION_ACTION'
        unique_together = (('docgen_activation_action', 'action'),)


class DocgenDocxAction(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    docgen_template = models.ForeignKey(
        'DocgenTemplate', models.CASCADE, db_column='DOCGEN_TEMPLATE_ID',
        related_name='+')
    docgen_template_class = models.ForeignKey(
        'DocgenTemplateClass', models.CASCADE,
        db_column='DOCGEN_TEMPLATE_CLASS_ID', related_name='+')
    action = models.ForeignKey(
        Action, models.CASCADE, db_column='ACTION_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'DOCGEN_DOCX_ACTION'
        unique_together = (
            ('docgen_template', 'docgen_template_class', 'action'),)


class TemplateGenerateAction(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    template = models.ForeignKey(
        'document.Template', models.CASCADE, db_column='TEMPLATE_ID',
        related_name='+')
    action = models.ForeignKey(
        Action, models.CASCADE, db_column='ACTION_ID', related_name='+')
    as_pdf = models.PositiveSmallIntegerField(db_column='AS_PDF', default=0)

    class Meta:
        managed = True
        db_table = 'TEMPLATE_GENERATE_ACTION'
        unique_together = (
            ('as_pdf', 'template', 'action'),)


class DocgenPdfAction(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    docgen_template = models.ForeignKey(
        'DocgenTemplate', models.CASCADE, db_column='DOCGEN_TEMPLATE_ID',
        related_name='+')
    docgen_template_class = models.ForeignKey(
        'DocgenTemplateClass', models.CASCADE,
        db_column='DOCGEN_TEMPLATE_CLASS_ID', related_name='+')
    action = models.ForeignKey(
        Action, models.CASCADE, db_column='ACTION_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'DOCGEN_PDF_ACTION'
        unique_together = (
            ('docgen_template', 'docgen_template_class', 'action'),)


class DocgenTemplate(models.Model):
    docgen_template_id = models.AutoField(
        db_column='DOCGEN_TEMPLATE_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=255)
    path = models.CharField(db_column='PATH', max_length=255)
    type = models.FloatField(db_column='TYPE')

    class Meta:
        managed = True
        db_table = 'DOCGEN_TEMPLATE'


class DocgenTemplateClass(models.Model):
    docgen_template_class_id = models.AutoField(
        db_column='DOCGEN_TEMPLATE_CLASS_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=255)
    path = models.CharField(db_column='PATH', max_length=255)
    type = models.FloatField(db_column='TYPE')

    class Meta:
        managed = True
        db_table = 'DOCGEN_TEMPLATE_CLASS'


class FormGroup(models.Model):
    form_group_id = models.AutoField(
        db_column='FORM_GROUP_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=500)
    description = models.CharField(
        db_column='DESCRIPTION', max_length=1000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'FORM_GROUP'


class FormGroupForm(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    form_group = models.ForeignKey(
        FormGroup, models.CASCADE, db_column='FORM_GROUP_ID',
        related_name='forms')
    form = models.ForeignKey('instance.Form', models.CASCADE,
                             db_column='FORM_ID', related_name='form_group')

    class Meta:
        managed = True
        db_table = 'FORM_GROUP_FORM'
        unique_together = (('form_group', 'form'),)


class GlossaryCategory(models.Model):
    glossary_category_id = models.AutoField(
        db_column='GLOSSARY_CATEGORY_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=80)
    role_id = models.FloatField(db_column='ROLE_ID', blank=True, null=True)
    service_id = models.FloatField(
        db_column='SERVICE_ID', blank=True, null=True)
    user_id = models.FloatField(db_column='USER_ID', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'GLOSSARY_CATEGORY'


class GlossarySentence(models.Model):
    glossary_sentence_id = models.AutoField(
        db_column='GLOSSARY_SENTENCE_ID', primary_key=True)
    glossary_category_id = models.FloatField(db_column='GLOSSARY_CATEGORY_ID')
    title = models.CharField(db_column='TITLE', max_length=500)
    sentence = models.CharField(db_column='SENTENCE', max_length=4000)
    role_id = models.FloatField(db_column='ROLE_ID', blank=True, null=True)
    service_id = models.FloatField(
        db_column='SERVICE_ID', blank=True, null=True)
    user_id = models.FloatField(db_column='USER_ID', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'GLOSSARY_SENTENCE'


class InstanceDemo(models.Model):
    instance_demo = models.OneToOneField(
        'instance.Instance', models.DO_NOTHING, db_column='INSTANCE_DEMO_ID',
        primary_key=True, related_name='+')
    value = models.CharField(
        db_column='VALUE', max_length=1000, blank=True, null=True)
    automatic_date = models.DateTimeField(
        db_column='AUTOMATIC_DATE', blank=True, null=True)
    form_date = models.DateTimeField(
        db_column='FORM_DATE', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'INSTANCE_DEMO'


class InstanceDemoLog(models.Model):
    instance_demo_log_id = models.AutoField(
        db_column='INSTANCE_DEMO_LOG_ID', primary_key=True)
    modification_date = models.DateTimeField(db_column='MODIFICATION_DATE')
    user_id = models.IntegerField(db_column='USER_ID')
    action = models.CharField(db_column='ACTION', max_length=500)
    data = models.TextField(db_column='DATA')
    id = models.IntegerField(db_column='ID')

    class Meta:
        managed = True
        db_table = 'INSTANCE_DEMO_LOG'


class InstanceFormPdf(models.Model):
    instance_form_pdf_id = models.AutoField(
        db_column='INSTANCE_FORM_PDF_ID', primary_key=True)
    instance = models.ForeignKey(
        'instance.Instance', models.DO_NOTHING, db_column='INSTANCE_ID',
        related_name='+')
    action = models.ForeignKey(
        Action, models.DO_NOTHING, db_column='ACTION_ID', related_name='+')
    user = models.ForeignKey('user.User', models.DO_NOTHING,
                             db_column='USER_ID', related_name='+')
    modification_date = models.DateTimeField(db_column='MODIFICATION_DATE')
    name = models.CharField(db_column='NAME', max_length=50)
    filename = models.CharField(db_column='FILENAME', max_length=50)

    class Meta:
        managed = True
        db_table = 'INSTANCE_FORM_PDF'


class InstanceGuest(models.Model):
    instance = models.OneToOneField(
        'instance.Instance', models.DO_NOTHING, db_column='INSTANCE_ID',
        primary_key=True, related_name='+')
    session_id = models.CharField(db_column='SESSION_ID', max_length=128)
    modification_date = models.DateTimeField(db_column='MODIFICATION_DATE')

    class Meta:
        managed = True
        db_table = 'INSTANCE_GUEST'


class InstanceLocation(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    location = models.ForeignKey(
        'user.Location', models.DO_NOTHING, db_column='LOCATION_ID',
        related_name='+')
    instance = models.ForeignKey(
        'instance.Instance', models.DO_NOTHING, db_column='INSTANCE_ID',
        related_name='+')

    class Meta:
        managed = True
        db_table = 'INSTANCE_LOCATION'
        unique_together = (('location', 'instance'),)


class InstanceLocationLog(models.Model):
    instance_location_log_id = models.AutoField(
        db_column='INSTANCE_LOCATION_LOG_ID', primary_key=True)
    modification_date = models.DateTimeField(db_column='MODIFICATION_DATE')
    user_id = models.IntegerField(db_column='USER_ID')
    action = models.CharField(db_column='ACTION', max_length=500)
    data = models.TextField(db_column='DATA', blank=True, null=True)
    id1 = models.IntegerField(db_column='ID1')
    field1 = models.CharField(db_column='FIELD1', max_length=30)
    id2 = models.IntegerField(db_column='ID2')
    field2 = models.CharField(db_column='FIELD2', max_length=30)

    class Meta:
        managed = True
        db_table = 'INSTANCE_LOCATION_LOG'


class InstanceLog(models.Model):
    instance_log_id = models.AutoField(
        db_column='INSTANCE_LOG_ID', primary_key=True)
    modification_date = models.DateTimeField(db_column='MODIFICATION_DATE')
    user_id = models.IntegerField(db_column='USER_ID')
    action = models.CharField(db_column='ACTION', max_length=500)
    data = models.TextField(db_column='DATA', blank=True, null=True)
    id = models.IntegerField(db_column='ID')

    class Meta:
        managed = True
        db_table = 'INSTANCE_LOG'


class InstancePortal(models.Model):
    instance_id = models.AutoField(db_column='INSTANCE_ID', primary_key=True)
    portal_identifier = models.CharField(
        db_column='PORTAL_IDENTIFIER', max_length=256)

    class Meta:
        managed = True
        db_table = 'INSTANCE_PORTAL'


class InstanceResource(models.Model):
    instance_resource_id = models.AutoField(
        db_column='INSTANCE_RESOURCE_ID', primary_key=True)
    available_instance_resource = models.ForeignKey(
        AvailableInstanceResource, models.CASCADE,
        db_column='AVAILABLE_INSTANCE_RESOURCE_ID', related_name='+')
    resource = models.ForeignKey(
        'Resource', models.CASCADE, db_column='RESOURCE_ID',
        related_name='+')
    name = models.CharField(db_column='NAME', max_length=50)
    description = models.CharField(
        db_column='DESCRIPTION', max_length=1000, blank=True, null=True)
    template = models.CharField(
        db_column='TEMPLATE', max_length=500, blank=True, null=True)
    # Field renamed because it was a Python reserved word.
    class_field = models.CharField(
        db_column='CLASS', max_length=25, blank=True, null=True)
    hidden = models.PositiveSmallIntegerField(db_column='HIDDEN')
    sort = models.IntegerField(db_column='SORT')
    form_group = models.ForeignKey(FormGroup, models.CASCADE,
                                   db_column='FORM_GROUP_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'INSTANCE_RESOURCE'


class InstanceResourceAction(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    available_instance_resource = models.ForeignKey(
        AvailableInstanceResource, models.CASCADE,
        db_column='AVAILABLE_INSTANCE_RESOURCE_ID', related_name='+')
    available_action = models.ForeignKey(
        AvailableAction, models.CASCADE, db_column='AVAILABLE_ACTION_ID',
        related_name='+')

    class Meta:
        managed = True
        db_table = 'INSTANCE_RESOURCE_ACTION'
        unique_together = (
            ('available_instance_resource', 'available_action'),)


class IrAllformpages(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource, models.CASCADE, db_column='INSTANCE_RESOURCE_ID',
        primary_key=True, related_name='+')
    page_form_group = models.ForeignKey('PageFormGroup', models.CASCADE,
                                        db_column='PAGE_FORM_GROUP_ID',
                                        related_name='+', blank=True,
                                        null=True)
    pdf_class = models.CharField(
        db_column='PDF_CLASS', max_length=500, blank=True, null=True)
    show_all_page_form_mode = models.PositiveSmallIntegerField(
        db_column='SHOW_ALL_PAGE_FORM_MODE')

    class Meta:
        managed = True
        db_table = 'IR_ALLFORMPAGES'


class IrCirculation(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource, models.CASCADE, db_column='INSTANCE_RESOURCE_ID',
        primary_key=True, related_name='+')
    circulation_type = models.ForeignKey(
        CirculationType, models.CASCADE, db_column='CIRCULATION_TYPE_ID',
        related_name='+')
    service = models.ForeignKey('user.Service', models.CASCADE,
                                db_column='SERVICE_ID', related_name='+',
                                blank=True, null=True)
    draft_circulation_answer = models.ForeignKey(
        CirculationAnswer, models.CASCADE,
        db_column='DRAFT_CIRCULATION_ANSWER_ID', related_name='+', blank=True,
        null=True)
    show_notice = models.PositiveSmallIntegerField(db_column='SHOW_NOTICE')
    show_history = models.PositiveSmallIntegerField(db_column='SHOW_HISTORY')
    show_all_children = models.PositiveSmallIntegerField(
        db_column='SHOW_ALL_CHILDREN')
    read_notice_template = models.CharField(
        db_column='READ_NOTICE_TEMPLATE', max_length=500, blank=True,
        null=True)
    pdf_class = models.CharField(
        db_column='PDF_CLASS', max_length=500, blank=True, null=True)
    service_to_be_interpreted = models.CharField(
        db_column='SERVICE_TO_BE_INTERPRETED', max_length=50, blank=True,
        null=True)

    class Meta:
        managed = True
        db_table = 'IR_CIRCULATION'


class IrEditcirculation(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource, models.CASCADE, db_column='INSTANCE_RESOURCE_ID',
        primary_key=True, related_name='+')
    circulation_type = models.ForeignKey(
        CirculationType, models.CASCADE, db_column='CIRCULATION_TYPE_ID',
        related_name='+')
    draft_circulation_answer = models.ForeignKey(
        CirculationAnswer, models.CASCADE,
        db_column='DRAFT_CIRCULATION_ANSWER_ID', related_name='+', blank=True,
        null=True)
    show_notice = models.PositiveSmallIntegerField(db_column='SHOW_NOTICE')
    add_template = models.CharField(
        db_column='ADD_TEMPLATE', max_length=500, blank=True, null=True)
    add_activation_template = models.CharField(
        db_column='ADD_ACTIVATION_TEMPLATE', max_length=500, blank=True,
        null=True)
    read_notice_template = models.CharField(
        db_column='READ_NOTICE_TEMPLATE', max_length=500, blank=True,
        null=True)
    pdf_class = models.CharField(
        db_column='PDF_CLASS', max_length=500, blank=True, null=True)
    default_circulation_name = models.CharField(
        db_column='DEFAULT_CIRCULATION_NAME', max_length=500, blank=True,
        null=True)
    single_circulation = models.PositiveSmallIntegerField(
        db_column='SINGLE_CIRCULATION')
    inherit_notices = models.PositiveSmallIntegerField(
        db_column='INHERIT_NOTICES')
    display_first_circulation = models.PositiveSmallIntegerField(
        db_column='DISPLAY_FIRST_CIRCULATION')
    circulation_email_action_id = models.ForeignKey(
        Action, models.CASCADE, db_column='CIRCULATION_EMAIL_ACTION_ID',
        related_name='+', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'IR_EDITCIRCULATION'


class IrEditcirculationSg(models.Model):
    ir_editcirculation_sg_id = models.AutoField(
        db_column='IR_EDITCIRCULATION_SG_ID', primary_key=True)
    instance_resource = models.ForeignKey(
        IrEditcirculation, models.CASCADE, db_column='INSTANCE_RESOURCE_ID',
        related_name='+')
    service_group = models.ForeignKey(
        'user.ServiceGroup', models.CASCADE, db_column='SERVICE_GROUP_ID',
        related_name='+')
    localized = models.PositiveSmallIntegerField(db_column='LOCALIZED')

    class Meta:
        managed = True
        db_table = 'IR_EDITCIRCULATION_SG'


class IrEditformpage(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource, models.CASCADE, db_column='INSTANCE_RESOURCE_ID',
        primary_key=True, related_name='+')
    page = models.ForeignKey('Page', models.CASCADE,
                             db_column='PAGE_ID', related_name='+')
    pdf_class = models.CharField(
        db_column='PDF_CLASS', max_length=500, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'IR_EDITFORMPAGE'


class IrEditformpages(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource, models.CASCADE, db_column='INSTANCE_RESOURCE_ID',
        primary_key=True, related_name='+')
    page_form_group = models.ForeignKey('PageFormGroup', models.CASCADE,
                                        db_column='PAGE_FORM_GROUP_ID',
                                        related_name='+', blank=True,
                                        null=True)
    pdf_class = models.CharField(
        db_column='PDF_CLASS', max_length=500, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'IR_EDITFORMPAGES'


class IrEditletter(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource, models.CASCADE, db_column='INSTANCE_RESOURCE_ID',
        primary_key=True, related_name='+')
    pdf_class = models.CharField(
        db_column='PDF_CLASS', max_length=500, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'IR_EDITLETTER'


class IrEditletterAnswer(models.Model):
    ir_editletter_answer_id = models.AutoField(
        db_column='IR_EDITLETTER_ANSWER_ID', primary_key=True)
    instance_resource = models.ForeignKey(
        IrEditletter, models.CASCADE, db_column='INSTANCE_RESOURCE_ID',
        related_name='+')
    name = models.CharField(db_column='NAME', max_length=50)

    class Meta:
        managed = True
        db_table = 'IR_EDITLETTER_ANSWER'


class IrEditnotice(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource, models.CASCADE, db_column='INSTANCE_RESOURCE_ID',
        primary_key=True, related_name='+')
    circulation_type = models.ForeignKey(
        CirculationType, models.CASCADE, db_column='CIRCULATION_TYPE_ID',
        related_name='+')
    editable_after_deadline = models.PositiveSmallIntegerField(
        db_column='EDITABLE_AFTER_DEADLINE')
    pdf_class = models.CharField(
        db_column='PDF_CLASS', max_length=500, blank=True, null=True)
    edit_notice_template = models.CharField(
        db_column='EDIT_NOTICE_TEMPLATE', max_length=500, blank=True,
        null=True)
    hide_answered_notices = models.PositiveSmallIntegerField(
        db_column='HIDE_ANSWERED_NOTICES')
    is_always_editable = models.PositiveSmallIntegerField(
        db_column='IS_ALWAYS_EDITABLE')

    class Meta:
        managed = True
        db_table = 'IR_EDITNOTICE'


class IrFormerror(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource, models.CASCADE, db_column='INSTANCE_RESOURCE_ID',
        primary_key=True, related_name='+')
    ir_editformpages = models.ForeignKey(
        IrEditformpages, models.CASCADE, db_column='IR_EDITFORMPAGES_ID',
        related_name='+')

    class Meta:
        managed = True
        db_table = 'IR_FORMERROR'


class IrFormpage(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource, models.CASCADE, db_column='INSTANCE_RESOURCE_ID',
        primary_key=True, related_name='+')
    page = models.ForeignKey('Page', models.CASCADE,
                             db_column='PAGE_ID', related_name='+')
    pdf_class = models.CharField(
        db_column='PDF_CLASS', max_length=500, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'IR_FORMPAGE'


class IrFormpages(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource, models.CASCADE, db_column='INSTANCE_RESOURCE_ID',
        primary_key=True, related_name='+')
    page_form_group = models.ForeignKey('PageFormGroup', models.CASCADE,
                                        db_column='PAGE_FORM_GROUP_ID',
                                        related_name='+', blank=True,
                                        null=True)
    pdf_class = models.CharField(
        db_column='PDF_CLASS', max_length=500, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'IR_FORMPAGES'


class IrFormwizard(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource, models.CASCADE, db_column='INSTANCE_RESOURCE_ID',
        primary_key=True, related_name='+')
    page_form_group = models.ForeignKey(
        'PageFormGroup', models.CASCADE, db_column='PAGE_FORM_GROUP_ID',
        related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')
    show_captcha = models.PositiveSmallIntegerField(db_column='SHOW_CAPTCHA')
    summary = models.CharField(
        db_column='SUMMARY', max_length=4000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'IR_FORMWIZARD'


class IrGroupAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instance_resource = models.ForeignKey(
        InstanceResource, models.CASCADE, db_column='INSTANCE_RESOURCE_ID',
        related_name='+')
    group = models.ForeignKey('user.Group', models.CASCADE,
                              db_column='GROUP_ID', related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'IR_GROUP_ACL'
        unique_together = (('instance_resource', 'group', 'instance_state'),)


class IrLetter(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource, models.CASCADE, db_column='INSTANCE_RESOURCE_ID',
        primary_key=True, related_name='+')
    ir_editletter_id = models.IntegerField(
        db_column='IR_EDITLETTER_ID', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'IR_LETTER'


class IrNewform(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource, models.CASCADE, db_column='INSTANCE_RESOURCE_ID',
        primary_key=True, related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')
    page_form_group = models.ForeignKey('PageFormGroup', models.CASCADE,
                                        db_column='PAGE_FORM_GROUP_ID',
                                        related_name='+', blank=True,
                                        null=True)

    class Meta:
        managed = True
        db_table = 'IR_NEWFORM'


class IrPage(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource, models.CASCADE, db_column='INSTANCE_RESOURCE_ID',
        primary_key=True, related_name='+')
    pdf_class = models.CharField(
        db_column='PDF_CLASS', max_length=500, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'IR_PAGE'


class IrRoleAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instance_resource = models.ForeignKey(
        InstanceResource, models.CASCADE, db_column='INSTANCE_RESOURCE_ID',
        related_name='+')
    role = models.ForeignKey('user.Role', models.CASCADE,
                             db_column='ROLE_ID', related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'IR_ROLE_ACL'
        unique_together = (('instance_resource', 'role', 'instance_state'),)


class IrServiceAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instance_resource = models.ForeignKey(
        InstanceResource, models.CASCADE, db_column='INSTANCE_RESOURCE_ID',
        related_name='+')
    service = models.ForeignKey(
        'user.Service', models.CASCADE, db_column='SERVICE_ID',
        related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'IR_SERVICE_ACL'
        unique_together = (('instance_resource', 'service', 'instance_state'),)


class IrUserAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instance_resource = models.ForeignKey(
        InstanceResource, models.CASCADE, db_column='INSTANCE_RESOURCE_ID',
        related_name='+')
    user = models.ForeignKey('user.User', models.CASCADE,
                             db_column='USER_ID', related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'IR_USER_ACL'
        unique_together = (('instance_resource', 'user', 'instance_state'),)


class Letter(models.Model):
    instance = models.ForeignKey(
        'instance.Instance', models.DO_NOTHING, db_column='INSTANCE_ID',
        related_name='+')
    instance_resource = models.ForeignKey(
        IrEditletter, models.DO_NOTHING, db_column='INSTANCE_RESOURCE_ID',
        related_name='+')
    user = models.ForeignKey('user.User', models.DO_NOTHING,
                             db_column='USER_ID', related_name='+')
    ir_editletter_answer = models.ForeignKey(
        IrEditletterAnswer, models.DO_NOTHING,
        db_column='IR_EDITLETTER_ANSWER_ID', related_name='+', blank=True,
        null=True)
    date = models.DateTimeField(db_column='DATE')
    name = models.CharField(db_column='NAME', max_length=50)
    content = models.TextField(db_column='CONTENT')
    modification_date = models.DateTimeField(db_column='MODIFICATION_DATE')

    class Meta:
        managed = True
        db_table = 'LETTER'
        unique_together = (('instance', 'instance_resource'),)


class LetterImage(models.Model):
    letter_image_id = models.AutoField(
        db_column='LETTER_IMAGE_ID', primary_key=True)
    instance = models.ForeignKey(
        'instance.Instance', models.DO_NOTHING,
        db_column='INSTANCE_ID', related_name='+')
    instance_resource = models.ForeignKey(
        InstanceResource, models.DO_NOTHING, db_column='INSTANCE_RESOURCE_ID',
        related_name='+')
    user = models.ForeignKey('user.User', models.DO_NOTHING,
                             db_column='USER_ID', related_name='+')
    modification_date = models.DateTimeField(db_column='MODIFICATION_DATE')
    name = models.CharField(db_column='NAME', max_length=50)
    filename = models.CharField(db_column='FILENAME', max_length=50)

    class Meta:
        managed = True
        db_table = 'LETTER_IMAGE'


class LoginAttempt(models.Model):
    login_attempt_id = models.AutoField(
        db_column='LOGIN_ATTEMPT_ID', primary_key=True)
    ip = models.CharField(db_column='IP', max_length=45)
    attempt_date = models.DateTimeField(db_column='ATTEMPT_DATE')
    username = models.CharField(
        db_column='USERNAME', max_length=250, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'LOGIN_ATTEMPT'


class Mapping(models.Model):
    mapping_id = models.AutoField(db_column='MAPPING_ID', primary_key=True)
    table_name = models.CharField(db_column='TABLE_NAME', max_length=30)
    column_name = models.CharField(db_column='COLUMN_NAME', max_length=30)

    class Meta:
        managed = True
        db_table = 'MAPPING'


class Notice(models.Model):
    notice_type = models.ForeignKey(
        'NoticeType', models.DO_NOTHING, db_column='NOTICE_TYPE_ID',
        related_name='+')
    activation = models.ForeignKey(
        Activation, models.DO_NOTHING, db_column='ACTIVATION_ID',
        related_name='notices')
    content = models.TextField(db_column='CONTENT', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'NOTICE'
        unique_together = (('notice_type', 'activation'),)


class NoticeImage(models.Model):
    notice_image_id = models.AutoField(
        db_column='NOTICE_IMAGE_ID', primary_key=True)
    instance = models.ForeignKey(
        'instance.Instance', models.DO_NOTHING, db_column='INSTANCE_ID',
        related_name='+')
    instance_resource = models.ForeignKey(
        IrEditnotice, models.DO_NOTHING,
        db_column='INSTANCE_RESOURCE_ID', related_name='+')
    user = models.ForeignKey('user.User', models.DO_NOTHING,
                             db_column='USER_ID', related_name='+')
    activation = models.ForeignKey(
        Activation, models.DO_NOTHING, db_column='ACTIVATION_ID',
        related_name='+')
    modification_date = models.DateTimeField(db_column='MODIFICATION_DATE')
    name = models.CharField(db_column='NAME', max_length=50)
    filename = models.CharField(db_column='FILENAME', max_length=50)

    class Meta:
        managed = True
        db_table = 'NOTICE_IMAGE'


class NoticeLog(models.Model):
    notice_log_id = models.AutoField(
        db_column='NOTICE_LOG_ID', primary_key=True)
    modification_date = models.DateTimeField(db_column='MODIFICATION_DATE')
    user_id = models.IntegerField(db_column='USER_ID')
    action = models.CharField(db_column='ACTION', max_length=500)
    data = models.TextField(db_column='DATA', blank=True, null=True)
    id1 = models.IntegerField(db_column='ID1')
    field1 = models.CharField(db_column='FIELD1', max_length=30)
    id2 = models.IntegerField(db_column='ID2')
    field2 = models.CharField(db_column='FIELD2', max_length=30)

    class Meta:
        managed = True
        db_table = 'NOTICE_LOG'


class NoticeType(models.Model):
    notice_type_id = models.AutoField(
        db_column='NOTICE_TYPE_ID', primary_key=True)
    circulation_type = models.ForeignKey(
        CirculationType, models.CASCADE, db_column='CIRCULATION_TYPE_ID',
        related_name='+')
    name = models.CharField(db_column='NAME', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'NOTICE_TYPE'


class Page(models.Model):
    page_id = models.AutoField(db_column='PAGE_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=500)
    description = models.CharField(
        db_column='DESCRIPTION', max_length=1000, blank=True, null=True)
    javascript = models.CharField(
        db_column='JAVASCRIPT', max_length=4000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'PAGE'


class PageAnswerActivation(models.Model):
    page_answer_activation_id = models.AutoField(
        db_column='PAGE_ANSWER_ACTIVATION_ID', primary_key=True)
    form = models.ForeignKey(
        'PageForm', models.CASCADE, db_column='FORM_ID', related_name='+')
    chapter = models.ForeignKey(
        'Chapter', models.CASCADE, db_column='CHAPTER_ID',
        related_name='+')
    question = models.ForeignKey(
        'Question', models.CASCADE, db_column='QUESTION_ID',
        related_name='+')
    page = models.ForeignKey(
        'PageForm', models.CASCADE, db_column='PAGE_ID', related_name='+')
    answer = models.CharField(db_column='ANSWER', max_length=4000)

    class Meta:
        managed = True
        db_table = 'PAGE_ANSWER_ACTIVATION'


class PageForm(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    page = models.ForeignKey(Page, models.CASCADE,
                             db_column='PAGE_ID', related_name='+')
    form = models.ForeignKey('instance.Form', models.CASCADE,
                             db_column='FORM_ID', related_name='+')
    page_form_mode = models.ForeignKey(
        'PageFormMode', models.CASCADE, db_column='PAGE_FORM_MODE_ID',
        related_name='+')
    page_form_group = models.ForeignKey('PageFormGroup', models.CASCADE,
                                        db_column='PAGE_FORM_GROUP_ID',
                                        related_name='+', blank=True,
                                        null=True)
    sort = models.IntegerField(db_column='SORT')

    class Meta:
        managed = True
        db_table = 'PAGE_FORM'
        unique_together = (('page', 'form'),)


class PageFormGroup(models.Model):
    page_form_group_id = models.AutoField(
        db_column='PAGE_FORM_GROUP_ID', primary_key=True)
    name = models.CharField(
        db_column='NAME', max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'PAGE_FORM_GROUP'


class PageFormGroupAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    page = models.ForeignKey(PageForm, models.CASCADE,
                             db_column='PAGE_ID', related_name='+')
    form = models.ForeignKey(PageForm, models.CASCADE,
                             db_column='FORM_ID', related_name='+')
    group = models.ForeignKey('user.Group', models.CASCADE,
                              db_column='GROUP_ID', related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'PAGE_FORM_GROUP_ACL'
        unique_together = (('page', 'form', 'group', 'instance_state'),)


class PageFormMode(models.Model):
    page_form_mode_id = models.AutoField(
        db_column='PAGE_FORM_MODE_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=50)

    class Meta:
        managed = True
        db_table = 'PAGE_FORM_MODE'


class PageFormRoleAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    page = models.ForeignKey(PageForm, models.CASCADE,
                             db_column='PAGE_ID', related_name='+')
    form = models.ForeignKey(PageForm, models.CASCADE,
                             db_column='FORM_ID', related_name='+')
    role = models.ForeignKey('user.Role', models.CASCADE,
                             db_column='ROLE_ID', related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'PAGE_FORM_ROLE_ACL'
        unique_together = (('page', 'form', 'role', 'instance_state'),)


class PageFormServiceAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    page = models.ForeignKey(PageForm, models.CASCADE,
                             db_column='PAGE_ID', related_name='+')
    form = models.ForeignKey(PageForm, models.CASCADE,
                             db_column='FORM_ID', related_name='+')
    service = models.ForeignKey(
        'user.Service', models.CASCADE, db_column='SERVICE_ID',
        related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'PAGE_FORM_SERVICE_ACL'
        unique_together = (('page', 'form', 'service', 'instance_state'),)


class PageFormUserAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    page = models.ForeignKey(PageForm, models.CASCADE,
                             db_column='PAGE_ID', related_name='+')
    form = models.ForeignKey(PageForm, models.CASCADE,
                             db_column='FORM_ID', related_name='+')
    user = models.ForeignKey('user.User', models.CASCADE,
                             db_column='USER_ID', related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'PAGE_FORM_USER_ACL'
        unique_together = (('page', 'form', 'user', 'instance_state'),)


class PortalSession(models.Model):
    portal_session_id = models.CharField(
        db_column='PORTAL_SESSION_ID', primary_key=True, max_length=256)
    portal_identifier = models.CharField(
        db_column='PORTAL_IDENTIFIER', max_length=256)
    last_active = models.DateTimeField(db_column='LAST_ACTIVE')

    class Meta:
        managed = True
        db_table = 'PORTAL_SESSION'


class ProposalActivation(models.Model):
    proposal_activation_id = models.AutoField(
        db_column='PROPOSAL_ACTIVATION_ID', primary_key=True)
    instance = models.ForeignKey(
        'instance.Instance', models.DO_NOTHING,
        db_column='INSTANCE_ID', related_name='+')
    circulation_type = models.ForeignKey(
        CirculationType, models.DO_NOTHING, db_column='CIRCULATION_TYPE_ID',
        related_name='+')
    service = models.ForeignKey(
        'user.Service', models.DO_NOTHING, db_column='SERVICE_ID',
        related_name='+')
    circulation_state = models.ForeignKey(
        CirculationState, models.DO_NOTHING, db_column='CIRCULATION_STATE_ID',
        related_name='+')
    deadline_date = models.DateTimeField(db_column='DEADLINE_DATE')
    reason = models.CharField(
        db_column='REASON', max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'PROPOSAL_ACTIVATION'


class PublicationEntry(models.Model):
    publication_entry_id = models.AutoField(
        db_column='PUBLICATION_ENTRY_ID', primary_key=True)
    instance = models.ForeignKey(
        'instance.Instance', models.DO_NOTHING,
        db_column='INSTANCE_ID', related_name='+')
    note = models.FloatField(db_column='NOTE')
    publication_date = models.DateTimeField(db_column='PUBLICATION_DATE')
    is_published = models.PositiveSmallIntegerField(db_column='IS_PUBLISHED')
    text = models.TextField(db_column='TEXT', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'PUBLICATION_ENTRY'


class PublicationSetting(models.Model):
    publication_setting_id = models.AutoField(
        db_column='PUBLICATION_SETTING_ID', primary_key=True)
    key = models.CharField(db_column='KEY', max_length=64)
    value = models.CharField(
        db_column='VALUE', max_length=4000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'PUBLICATION_SETTING'


class Question(models.Model):
    question_id = models.AutoField(db_column='QUESTION_ID', primary_key=True)
    question_type = models.ForeignKey(
        'QuestionType', models.CASCADE, db_column='QUESTION_TYPE_ID',
        related_name='+')
    mapping = models.ForeignKey(
        Mapping, models.CASCADE, db_column='MAPPING_ID', related_name='+',
        blank=True, null=True)
    answer_query = models.ForeignKey(
        AnswerQuery, models.CASCADE, db_column='ANSWER_QUERY_ID',
        related_name='+', blank=True, null=True)
    name = models.CharField(db_column='NAME', max_length=500)
    description = models.CharField(
        db_column='DESCRIPTION', max_length=1000, blank=True, null=True)
    javascript = models.CharField(
        db_column='JAVASCRIPT', max_length=4000, blank=True, null=True)
    regex = models.CharField(
        db_column='REGEX', max_length=1000, blank=True, null=True)
    default_answer = models.CharField(
        db_column='DEFAULT_ANSWER', max_length=4000, blank=True, null=True)
    # Field renamed because it was a Python reserved word.
    class_field = models.CharField(
        db_column='CLASS', max_length=25, blank=True, null=True)
    validation = models.CharField(
        db_column='VALIDATION', max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'QUESTION'


class QuestionChapter(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    question = models.ForeignKey(
        Question, models.CASCADE, db_column='QUESTION_ID', related_name='+')
    chapter = models.ForeignKey(
        Chapter, models.CASCADE, db_column='CHAPTER_ID', related_name='+')
    required = models.PositiveSmallIntegerField(db_column='REQUIRED')
    item = models.IntegerField(db_column='ITEM')
    sort = models.IntegerField(db_column='SORT')

    class Meta:
        managed = True
        db_table = 'QUESTION_CHAPTER'
        unique_together = (('question', 'chapter'),)


class QuestionChapterGroupAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    question = models.ForeignKey(
        Question, models.CASCADE, db_column='QUESTION_ID',
        related_name='+')
    chapter = models.ForeignKey(
        Chapter, models.CASCADE, db_column='CHAPTER_ID',
        related_name='+')
    group = models.ForeignKey('user.Group', models.CASCADE,
                              db_column='GROUP_ID', related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'QUESTION_CHAPTER_GROUP_ACL'
        unique_together = (('question', 'chapter', 'group', 'instance_state'),)


class QuestionChapterRoleAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    question = models.ForeignKey(
        Question, models.CASCADE, db_column='QUESTION_ID',
        related_name='+')
    chapter = models.ForeignKey(
        Chapter, models.CASCADE, db_column='CHAPTER_ID',
        related_name='+')
    role = models.ForeignKey('user.Role', models.CASCADE,
                             db_column='ROLE_ID', related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'QUESTION_CHAPTER_ROLE_ACL'
        unique_together = (('question', 'chapter', 'role', 'instance_state'),)


class QuestionChapterServiceAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    question = models.ForeignKey(
        Question, models.CASCADE, db_column='QUESTION_ID',
        related_name='+')
    chapter = models.ForeignKey(
        Chapter, models.CASCADE, db_column='CHAPTER_ID',
        related_name='+')
    service = models.ForeignKey(
        'user.Service', models.CASCADE, db_column='SERVICE_ID',
        related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'QUESTION_CHAPTER_SERVICE_ACL'
        unique_together = (
            ('question', 'chapter', 'service', 'instance_state'),)


class QuestionChapterUserAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    question = models.ForeignKey(
        Question, models.CASCADE, db_column='QUESTION_ID',
        related_name='+')
    chapter = models.ForeignKey(
        Chapter, models.CASCADE, db_column='CHAPTER_ID',
        related_name='+')
    user = models.ForeignKey('user.User', models.CASCADE,
                             db_column='USER_ID', related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'QUESTION_CHAPTER_USER_ACL'
        unique_together = (('question', 'chapter', 'user', 'instance_state'),)


class QuestionType(models.Model):
    question_type_id = models.AutoField(
        db_column='QUESTION_TYPE_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=20)
    sort = models.IntegerField(db_column='SORT', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'QUESTION_TYPE'


class RApiListInstanceState(models.Model):
    resource = models.ForeignKey(
        'Resource', models.CASCADE,
        db_column='RESOURCE_ID', related_name='+')
    instance_state = models.ForeignKey(
        'instance.InstanceState', models.CASCADE,
        db_column='INSTANCE_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'R_API_LIST_INSTANCE_STATE'
        unique_together = (('resource', 'instance_state'),)


class RApiListCirculationState(models.Model):
    resource = models.ForeignKey(
        'Resource', models.CASCADE,
        db_column='RESOURCE_ID', related_name='+')
    circulation_state = models.ForeignKey(
        'CirculationState', models.CASCADE,
        db_column='CIRCULATION_STATE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'R_API_LIST_CIRCULATION_STATE'
        unique_together = (('resource', 'circulation_state'),)


class RApiListCirculationType(models.Model):
    resource = models.ForeignKey(
        'Resource', models.CASCADE,
        db_column='RESOURCE_ID', related_name='+')
    circulation_type = models.ForeignKey(
        'CirculationType', models.CASCADE,
        db_column='CIRCULATION_TYPE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'R_API_LIST_CIRCULATION_TYPE'
        unique_together = (('resource', 'circulation_type'),)


class RFormlist(models.Model):
    resource = models.OneToOneField('Resource', models.CASCADE,
                                    db_column='RESOURCE_ID', primary_key=True,
                                    related_name='+')
    form = models.ForeignKey('instance.Form', models.CASCADE,
                             db_column='FORM_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'R_FORMLIST'


class RGroupAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    resource = models.ForeignKey(
        'Resource', models.CASCADE, db_column='RESOURCE_ID',
        related_name='+')
    group = models.ForeignKey('user.Group', models.CASCADE,
                              db_column='GROUP_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'R_GROUP_ACL'
        unique_together = (('resource', 'group'),)


class RList(models.Model):
    resource = models.OneToOneField('Resource', models.CASCADE,
                                    db_column='RESOURCE_ID', primary_key=True,
                                    related_name='+')
    query = models.CharField(db_column='QUERY', max_length=4000)

    class Meta:
        managed = True
        db_table = 'R_LIST'


class RListColumn(models.Model):
    r_list_column_id = models.AutoField(
        db_column='R_LIST_COLUMN_ID', primary_key=True)
    resource = models.ForeignKey(
        RList, models.CASCADE, db_column='RESOURCE_ID', related_name='+')
    column_name = models.CharField(db_column='COLUMN_NAME', max_length=30)
    alias = models.CharField(db_column='ALIAS', max_length=30)
    sort = models.IntegerField(db_column='SORT')

    class Meta:
        managed = True
        db_table = 'R_LIST_COLUMN'


class RPage(models.Model):
    resource = models.OneToOneField('Resource', models.CASCADE,
                                    db_column='RESOURCE_ID', primary_key=True,
                                    related_name='+')
    pdf_class = models.CharField(
        db_column='PDF_CLASS', max_length=500, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'R_PAGE'


class RRoleAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    resource = models.ForeignKey(
        'Resource', models.CASCADE, db_column='RESOURCE_ID',
        related_name='+')
    role = models.ForeignKey('user.Role', models.CASCADE,
                             db_column='ROLE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'R_ROLE_ACL'
        unique_together = (('resource', 'role'),)


class RSearch(models.Model):
    resource = models.OneToOneField('Resource', models.CASCADE,
                                    db_column='RESOURCE_ID', primary_key=True,
                                    related_name='+')
    result_template = models.CharField(
        db_column='RESULT_TEMPLATE', max_length=500, blank=True, null=True)
    query = models.TextField(db_column='QUERY')
    pdf_class = models.CharField(
        db_column='PDF_CLASS', max_length=500, blank=True, null=True)
    preserve_result = models.PositiveSmallIntegerField(
        db_column='PRESERVE_RESULT')

    class Meta:
        managed = True
        db_table = 'R_SEARCH'


class RSearchColumn(models.Model):
    r_search_column_id = models.AutoField(
        db_column='R_SEARCH_COLUMN_ID', primary_key=True)
    resource = models.ForeignKey(
        RSearch, models.CASCADE, db_column='RESOURCE_ID', related_name='+')
    column_name = models.CharField(db_column='COLUMN_NAME', max_length=30)
    alias = models.CharField(db_column='ALIAS', max_length=30)
    sort = models.IntegerField(db_column='SORT')

    class Meta:
        managed = True
        db_table = 'R_SEARCH_COLUMN'


class RSearchFilter(models.Model):
    r_search_filter_id = models.AutoField(
        db_column='R_SEARCH_FILTER_ID', primary_key=True)
    resource = models.ForeignKey(
        RSearch, models.CASCADE, db_column='RESOURCE_ID', related_name='+')
    question = models.ForeignKey(
        Question, models.CASCADE, db_column='QUESTION_ID', related_name='+',
        blank=True, null=True)
    field_name = models.CharField(db_column='FIELD_NAME', max_length=50)
    label = models.CharField(db_column='LABEL', max_length=1000)
    query = models.CharField(db_column='QUERY', max_length=4000)
    wildcard = models.PositiveSmallIntegerField(db_column='WILDCARD')
    # Field renamed because it was a Python reserved word.
    class_field = models.CharField(
        db_column='CLASS', max_length=25, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'R_SEARCH_FILTER'


class RServiceAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    resource = models.ForeignKey(
        'Resource', models.CASCADE, db_column='RESOURCE_ID',
        related_name='+')
    service = models.ForeignKey(
        'user.Service', models.CASCADE, db_column='SERVICE_ID',
        related_name='+')

    class Meta:
        managed = True
        db_table = 'R_SERVICE_ACL'
        unique_together = (('resource', 'service'),)


class RSimpleList(models.Model):
    resource_id = models.AutoField(db_column='RESOURCE_ID', primary_key=True)
    instance_states = models.CharField(
        db_column='INSTANCE_STATES', max_length=100)

    class Meta:
        managed = True
        db_table = 'R_SIMPLE_LIST'


class RUserAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    resource = models.ForeignKey(
        'Resource', models.CASCADE, db_column='RESOURCE_ID',
        related_name='+')
    user = models.ForeignKey('user.User', models.CASCADE,
                             db_column='USER_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'R_USER_ACL'
        unique_together = (('resource', 'user'),)


class Resource(models.Model):
    resource_id = models.AutoField(db_column='RESOURCE_ID', primary_key=True)
    available_resource = models.ForeignKey(
        AvailableResource, models.CASCADE,
        db_column='AVAILABLE_RESOURCE_ID', related_name='+')
    name = models.CharField(db_column='NAME', max_length=50)
    description = models.CharField(
        db_column='DESCRIPTION', max_length=1000, blank=True, null=True)
    template = models.CharField(
        db_column='TEMPLATE', max_length=500, blank=True, null=True)
    # Field renamed because it was a Python reserved word.
    class_field = models.CharField(
        db_column='CLASS', max_length=25, blank=True, null=True)
    hidden = models.PositiveSmallIntegerField(db_column='HIDDEN')
    sort = models.IntegerField(db_column='SORT')

    class Meta:
        managed = True
        db_table = 'RESOURCE'


class Sanction(models.Model):
    sanction_id = models.AutoField(db_column='SANCTION_ID', primary_key=True)
    instance = models.ForeignKey(
        'instance.Instance', models.DO_NOTHING,
        db_column='INSTANCE_ID', related_name='+')
    service = models.ForeignKey(
        'user.Service', models.DO_NOTHING, db_column='SERVICE_ID',
        related_name='+')
    user = models.ForeignKey('user.User', models.DO_NOTHING,
                             db_column='USER_ID', related_name='+')
    text = models.CharField(db_column='TEXT', max_length=4000)
    start_date = models.DateTimeField(db_column='START_DATE')
    deadline_date = models.DateTimeField(
        db_column='DEADLINE_DATE', blank=True, null=True)
    end_date = models.DateTimeField(
        db_column='END_DATE', blank=True, null=True)
    notice = models.CharField(
        db_column='NOTICE', max_length=500, blank=True, null=True)
    is_finished = models.PositiveSmallIntegerField(db_column='IS_FINISHED')
    finished_by_user = models.ForeignKey(
        'user.User', models.DO_NOTHING, db_column='FINISHED_BY_USER_ID',
        related_name='+', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'SANCTION'


class ServiceAnswerActivation(models.Model):
    service_answer_activation_id = models.AutoField(
        db_column='SERVICE_ANSWER_ACTIVATION_ID', primary_key=True)
    form = models.ForeignKey('instance.Form', models.DO_NOTHING,
                             db_column='FORM_ID', related_name='+')
    chapter = models.ForeignKey(
        Chapter, models.DO_NOTHING, db_column='CHAPTER_ID',
        related_name='+')
    question = models.ForeignKey(
        Question, models.DO_NOTHING, db_column='QUESTION_ID',
        related_name='+')
    service = models.ForeignKey(
        'user.Service', models.DO_NOTHING, db_column='SERVICE_ID',
        related_name='+')
    answer = models.CharField(db_column='ANSWER', max_length=4000)

    class Meta:
        managed = True
        db_table = 'SERVICE_ANSWER_ACTIVATION'


class WorkflowAction(models.Model):
    action = models.OneToOneField(
        Action, models.CASCADE, db_column='ACTION_ID', primary_key=True,
        related_name='+')
    workflow_item = models.ForeignKey(
        'WorkflowItem', models.CASCADE, db_column='WORKFLOW_ITEM_ID',
        related_name='+')
    multi_value = models.PositiveSmallIntegerField(db_column='MULTI_VALUE')

    class Meta:
        managed = True
        db_table = 'WORKFLOW_ACTION'


class WorkflowEntry(models.Model):
    workflow_entry_id = models.AutoField(
        db_column='WORKFLOW_ENTRY_ID', primary_key=True)
    workflow_date = models.DateTimeField(db_column='WORKFLOW_DATE')
    instance = models.ForeignKey(
        'instance.Instance', models.DO_NOTHING, db_column='INSTANCE_ID')
    workflow_item = models.ForeignKey(
        'WorkflowItem', models.DO_NOTHING, db_column='WORKFLOW_ITEM_ID',
        related_name='+')
    group = models.IntegerField(db_column='GROUP')

    class Meta:
        managed = True
        db_table = 'WORKFLOW_ENTRY'


class WorkflowItem(models.Model):
    workflow_item_id = models.AutoField(
        db_column='WORKFLOW_ITEM_ID', primary_key=True)
    position = models.IntegerField(db_column='POSITION')
    name = models.CharField(db_column='NAME', max_length=255)
    automatical = models.PositiveSmallIntegerField(db_column='AUTOMATICAL')
    different_color = models.PositiveSmallIntegerField(
        db_column='DIFFERENT_COLOR')
    is_workflow = models.PositiveSmallIntegerField(db_column='IS_WORKFLOW')
    is_building_authority = models.PositiveSmallIntegerField(
        db_column='IS_BUILDING_AUTHORITY')
    workflow_section = models.ForeignKey('WorkflowSection', models.CASCADE,
                                         db_column='WORKFLOW_SECTION_ID',
                                         related_name='+', blank=True,
                                         null=True)

    class Meta:
        managed = True
        db_table = 'WORKFLOW_ITEM'


class WorkflowRole(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    workflow_item = models.ForeignKey(
        WorkflowItem, models.CASCADE, db_column='WORKFLOW_ITEM_ID',
        related_name='+')
    role = models.ForeignKey('user.Role', models.CASCADE,
                             db_column='ROLE_ID', related_name='+')

    class Meta:
        managed = True
        db_table = 'WORKFLOW_ROLE'
        unique_together = (('role', 'workflow_item'),)


class WorkflowSection(models.Model):
    workflow_section_id = models.AutoField(
        db_column='WORKFLOW_SECTION_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=60)
    sort = models.IntegerField(db_column='SORT', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'WORKFLOW_SECTION'


class AttachmentExtension(models.Model):
    attachment_extension_id = models.AutoField(
        db_column='ATTACHMENT_EXTENSION_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=10)

    class Meta:
        managed = True
        db_table = 'ATTACHMENT_EXTENSION'


class AttachmentExtensionRole(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    attachment_extension = models.ForeignKey(
        AttachmentExtension, models.CASCADE,
        db_column='ATTACHMENT_EXTENSION_ID', related_name='+')
    role = models.ForeignKey('user.Role', models.CASCADE,
                             db_column='ROLE_ID', related_name='+')
    mode = models.CharField(
        db_column='MODE', max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ATTACHMENT_EXTENSION_ROLE'
        unique_together = (('attachment_extension', 'role'),)


class AttachmentExtensionService(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    attachment_extension = models.ForeignKey(
        AttachmentExtension, models.CASCADE,
        db_column='ATTACHMENT_EXTENSION_ID', related_name='+')
    service = models.ForeignKey(
        'user.Service', models.CASCADE, db_column='SERVICE_ID',
        related_name='+')
    mode = models.CharField(
        db_column='MODE', max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ATTACHMENT_EXTENSION_SERVICE'
        unique_together = (('attachment_extension', 'service'),)
