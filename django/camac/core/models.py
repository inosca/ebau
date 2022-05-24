import json

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import translation


class MultilingualModel:
    """Mixin for models that have a multilingual "name" property."""

    def get_name(self, lang=None):
        return self.get_trans_attr("name", lang)

    def get_trans_attr(self, name, lang=None):
        if not settings.APPLICATION.get("IS_MULTILINGUAL", False):
            return getattr(self, name)

        match = self.get_trans_obj(lang)
        if not match:
            return getattr(self, name)
        return getattr(match, name)

    def get_trans_obj(self, lang=None):
        lang = lang or translation.get_language()

        # we filter the translation in python so we don't trigger another query
        # when the translations are already prefetched which they should be in
        # most cases
        trans = self.trans.all()
        match = next(filter(lambda t: t.language == lang, trans), None)
        if not match:
            match = next(
                filter(lambda t: t.language == settings.LANGUAGE_CODE, trans), None
            )
        return match

    def __str__(self):
        return self.get_name()


class ACheckquery(models.Model):
    action = models.OneToOneField(
        "Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )
    query = models.CharField(db_column="QUERY", max_length=4000)

    class Meta:
        managed = True
        db_table = "A_CHECKQUERY"


class ACirculationEmail(MultilingualModel, models.Model):
    action = models.OneToOneField(
        "Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )
    sender_name = models.CharField(db_column="SENDER_NAME", max_length=50)
    sender_email = models.CharField(db_column="SENDER_EMAIL", max_length=50)
    title = models.CharField(db_column="TITLE", max_length=200)
    text = models.CharField(db_column="TEXT", max_length=2000)

    def __str__(self):
        return self.get_trans_attr("title")

    class Meta:
        managed = True
        db_table = "A_CIRCULATION_EMAIL"


class ACirculationEmailT(models.Model):
    action = models.ForeignKey(
        ACirculationEmail, models.CASCADE, db_column="ACTION_ID", related_name="trans"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    title = models.CharField(db_column="TITLE", max_length=200, blank=True, null=True)
    text = models.CharField(db_column="TEXT", max_length=2000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "A_CIRCULATION_EMAIL_T"


class ACirculationtransition(models.Model):
    action = models.OneToOneField(
        "Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )
    current_circulation_state = models.ForeignKey(
        "CirculationState",
        models.CASCADE,
        db_column="CURRENT_CIRCULATION_STATE_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    next_circulation_state = models.ForeignKey(
        "CirculationState",
        models.CASCADE,
        db_column="NEXT_CIRCULATION_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "A_CIRCULATIONTRANSITION"


class ACopyanswer(models.Model):
    action = models.OneToOneField(
        "Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "A_COPYANSWER"


class ACopyanswerMapping(models.Model):
    a_copyanswer_mapping_id = models.AutoField(
        db_column="A_COPYANSWER_MAPPING_ID", primary_key=True
    )
    action = models.ForeignKey(
        ACopyanswer, models.CASCADE, db_column="ACTION_ID", related_name="+"
    )
    source_chapter = models.ForeignKey(
        "Chapter",
        models.CASCADE,
        db_column="SOURCE_CHAPTER_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    source_question = models.ForeignKey(
        "Question",
        models.CASCADE,
        db_column="SOURCE_QUESTION_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    destination_chapter = models.ForeignKey(
        "Chapter", models.CASCADE, db_column="DESTINATION_CHAPTER_ID", related_name="+"
    )
    destination_question = models.ForeignKey(
        "Question",
        models.CASCADE,
        db_column="DESTINATION_QUESTION_ID",
        related_name="+",
    )
    get_name = models.PositiveSmallIntegerField(db_column="GET_NAME")

    class Meta:
        managed = True
        db_table = "A_COPYANSWER_MAPPING"


class ACopydata(models.Model):
    action = models.OneToOneField(
        "Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "A_COPYDATA"


class ACopydataMapping(models.Model):
    a_copydata_mapping_id = models.AutoField(
        db_column="A_COPYDATA_MAPPING_ID", primary_key=True
    )
    action = models.ForeignKey(
        ACopydata, models.CASCADE, db_column="ACTION_ID", related_name="+"
    )
    question = models.ForeignKey(
        "Question",
        models.CASCADE,
        db_column="QUESTION_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    chapter = models.ForeignKey(
        "Chapter",
        models.CASCADE,
        db_column="CHAPTER_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    table_name = models.CharField(db_column="TABLE_NAME", max_length=30)
    column_name = models.CharField(db_column="COLUMN_NAME", max_length=30)
    get_name = models.PositiveSmallIntegerField(db_column="GET_NAME")

    class Meta:
        managed = True
        db_table = "A_COPYDATA_MAPPING"


class ADeleteCirculation(models.Model):
    action = models.OneToOneField(
        "Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )
    delete_level = models.IntegerField(db_column="DELETE_LEVEL")
    circulation_to_be_interpreted = models.CharField(
        db_column="CIRCULATION_TO_BE_INTERPRETED", max_length=100, blank=True, null=True
    )
    is_single_delete = models.BooleanField(db_column="IS_SINGLE_DELETE", null=True)

    class Meta:
        managed = True
        db_table = "A_DELETE_CIRCULATION"


class AEmail(MultilingualModel, models.Model):
    action = models.OneToOneField(
        "Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )
    sender_name = models.CharField(db_column="SENDER_NAME", max_length=50)
    sender_email = models.CharField(db_column="SENDER_EMAIL", max_length=50)
    query = models.CharField(db_column="QUERY", max_length=4000)
    title = models.CharField(db_column="TITLE", max_length=200, blank=True, null=True)
    text = models.CharField(db_column="TEXT", max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.get_trans_attr("title")

    class Meta:
        managed = True
        db_table = "A_EMAIL"


class AEmailT(models.Model):
    action = models.ForeignKey(
        AEmail, models.CASCADE, db_column="ACTION_ID", related_name="trans"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    title = models.CharField(db_column="TITLE", max_length=200, blank=True, null=True)
    text = models.CharField(db_column="TEXT", max_length=2000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "A_EMAIL_T"


class AFormtransition(models.Model):
    action = models.OneToOneField(
        "Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )
    current_instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="CURRENT_INSTANCE_STATE_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    next_instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="NEXT_INSTANCE_STATE_ID",
        related_name="+",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "A_FORMTRANSITION"


class ANotification(models.Model):
    action = models.OneToOneField(
        "core.Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )
    template = models.SlugField(db_column="TEMPLATE_ID", max_length=100, unique=False)
    recipient_type = models.CharField(db_column="RECIPIENT_TYPE", max_length=160)
    processor = models.CharField(db_column="PROCESSOR", max_length=160)

    class Meta:
        managed = True
        db_table = "ACTION_NOTIFICATION"


class ALocation(models.Model):
    action = models.OneToOneField(
        "Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "A_LOCATION"


class ALocationQc(models.Model):
    a_location_qc_id = models.AutoField(db_column="A_LOCATION_QC_ID", primary_key=True)
    action = models.ForeignKey(
        ALocation, models.CASCADE, db_column="ACTION_ID", related_name="+"
    )
    question = models.ForeignKey(
        "Question", models.CASCADE, db_column="QUESTION_ID", related_name="+"
    )
    chapter = models.ForeignKey(
        "Chapter", models.CASCADE, db_column="CHAPTER_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "A_LOCATION_QC"


class ANotice(models.Model):
    action = models.OneToOneField(
        "Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )
    notice_type = models.ForeignKey(
        "NoticeType", models.CASCADE, db_column="NOTICE_TYPE_ID", related_name="+"
    )
    query = models.CharField(db_column="QUERY", max_length=4000)

    class Meta:
        managed = True
        db_table = "A_NOTICE"


class APageredirect(models.Model):
    action = models.OneToOneField(
        "Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )
    resource = models.ForeignKey(
        "Resource", models.CASCADE, db_column="RESOURCE_ID", related_name="+"
    )
    instance_resource = models.ForeignKey(
        "InstanceResource",
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    air_action_name = models.CharField(
        db_column="AIR_ACTION_NAME", max_length=25, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "A_PAGEREDIRECT"


class APhp(models.Model):
    action = models.OneToOneField(
        "Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )
    php_class = models.CharField(db_column="PHP_CLASS", max_length=500)

    class Meta:
        managed = True
        db_table = "A_PHP"


class AProposal(MultilingualModel, models.Model):
    action = models.OneToOneField(
        "Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )
    circulation_type = models.ForeignKey(
        "CirculationType",
        models.CASCADE,
        db_column="CIRCULATION_TYPE_ID",
        related_name="+",
    )
    circulation_state = models.ForeignKey(
        "CirculationState",
        models.CASCADE,
        db_column="CIRCULATION_STATE_ID",
        related_name="+",
    )
    deadline_days = models.IntegerField(db_column="DEADLINE_DAYS")
    reason = models.CharField(db_column="REASON", max_length=50, blank=True, null=True)
    is_working_days = models.PositiveSmallIntegerField(db_column="IS_WORKING_DAYS")

    def __str__(self):
        return self.get_trans_attr("reason")

    class Meta:
        managed = True
        db_table = "A_PROPOSAL"


class AProposalT(models.Model):
    action = models.ForeignKey(
        AProposal, models.CASCADE, db_column="ACTION_ID", related_name="trans"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    reason = models.CharField(db_column="REASON", max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "A_PROPOSAL_T"


class AProposalHoliday(models.Model):
    a_proposal_holiday_id = models.AutoField(
        db_column="A_PROPOSAL_HOLIDAY_ID", primary_key=True
    )
    holiday_date = models.DateTimeField(db_column="HOLIDAY_DATE")

    class Meta:
        managed = True
        db_table = "A_PROPOSAL_HOLIDAY"


class ASavepdf(models.Model):
    action = models.OneToOneField(
        "Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )
    form = models.ForeignKey(
        "instance.Form", models.CASCADE, db_column="FORM_ID", related_name="+"
    )
    page_form_group = models.ForeignKey(
        "PageFormGroup",
        models.CASCADE,
        db_column="PAGE_FORM_GROUP_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    show_all_page_form_mode = models.PositiveSmallIntegerField(
        db_column="SHOW_ALL_PAGE_FORM_MODE"
    )
    template = models.CharField(db_column="TEMPLATE", max_length=500)
    pdf_class = models.CharField(db_column="PDF_CLASS", max_length=500)

    class Meta:
        managed = True
        db_table = "A_SAVEPDF"


class AValidate(models.Model):
    action = models.OneToOneField(
        "Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )
    page_form_group = models.ForeignKey(
        "PageFormGroup",
        models.CASCADE,
        db_column="PAGE_FORM_GROUP_ID",
        related_name="+",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "A_VALIDATE"


class Action(MultilingualModel, models.Model):
    action_id = models.AutoField(db_column="ACTION_ID", primary_key=True)
    available_action = models.ForeignKey(
        "AvailableAction",
        models.CASCADE,
        db_column="AVAILABLE_ACTION_ID",
        related_name="+",
    )
    button = models.ForeignKey(
        "Button", models.CASCADE, db_column="BUTTON_ID", related_name="+"
    )
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )
    success_message = models.CharField(
        db_column="SUCCESS_MESSAGE", max_length=1000, blank=True, null=True
    )
    error_message = models.CharField(
        db_column="ERROR_MESSAGE", max_length=1000, blank=True, null=True
    )
    execute_always = models.PositiveSmallIntegerField(db_column="EXECUTE_ALWAYS")
    sort = models.IntegerField(db_column="SORT")

    class Meta:
        managed = True
        db_table = "ACTION"


class ActionT(models.Model):
    action = models.ForeignKey(
        Action, models.CASCADE, db_column="ACTION_ID", related_name="trans"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )
    success_message = models.CharField(
        db_column="SUCCESS_MESSAGE", max_length=1000, blank=True, null=True
    )
    error_message = models.CharField(
        db_column="ERROR_MESSAGE", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "ACTION_T"


class Activation(models.Model):
    activation_id = models.AutoField(db_column="ACTIVATION_ID", primary_key=True)
    circulation = models.ForeignKey(
        "Circulation",
        models.CASCADE,
        db_column="CIRCULATION_ID",
        related_name="activations",
    )
    service = models.ForeignKey(
        "user.Service", models.DO_NOTHING, db_column="SERVICE_ID", related_name="+"
    )
    service_parent = models.ForeignKey(
        "user.Service",
        models.DO_NOTHING,
        db_column="SERVICE_PARENT_ID",
        related_name="+",
    )
    circulation_state = models.ForeignKey(
        "CirculationState",
        models.DO_NOTHING,
        db_column="CIRCULATION_STATE_ID",
        related_name="+",
    )
    user = models.ForeignKey(
        "user.User",
        models.DO_NOTHING,
        db_column="USER_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    circulation_answer = models.ForeignKey(
        "CirculationAnswer",
        models.DO_NOTHING,
        db_column="CIRCULATION_ANSWER_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    start_date = models.DateTimeField(db_column="START_DATE")
    deadline_date = models.DateTimeField(db_column="DEADLINE_DATE")
    suspension_date = models.DateTimeField(
        db_column="SUSPENSION_DATE", blank=True, null=True
    )
    end_date = models.DateTimeField(db_column="END_DATE", blank=True, null=True)
    version = models.IntegerField(db_column="VERSION")
    reason = models.CharField(
        db_column="REASON", max_length=4000, blank=True, null=True
    )
    activation_parent = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        db_column="ACTIVATION_PARENT_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    email_sent = models.PositiveSmallIntegerField(db_column="EMAIL_SENT", default=1)
    ech_msg_created = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = "ACTIVATION"


class ActivationAnswer(models.Model):
    activation = models.ForeignKey(
        Activation, models.CASCADE, db_column="ACTIVATION_ID"
    )
    question = models.ForeignKey(
        "Question", models.DO_NOTHING, db_column="QUESTION_ID", related_name="+"
    )
    chapter = models.ForeignKey(
        "Chapter", models.DO_NOTHING, db_column="CHAPTER_ID", related_name="+"
    )
    item = models.IntegerField(db_column="ITEM")
    answer = models.CharField(db_column="ANSWER", max_length=4000)

    class Meta:
        managed = True
        db_table = "ACTIVATION_ANSWER"
        unique_together = (("activation", "question", "chapter", "item"),)


class ActivationAnswerLog(models.Model):
    activation_answer_log_id = models.AutoField(
        db_column="ACTIVATION_ANSWER_LOG_ID", primary_key=True
    )
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")
    user_id = models.IntegerField(db_column="USER_ID")
    action = models.CharField(db_column="ACTION", max_length=500)
    data = models.TextField(db_column="DATA")
    id1 = models.IntegerField(db_column="ID1")
    field1 = models.CharField(db_column="FIELD1", max_length=30)
    id2 = models.IntegerField(db_column="ID2")
    field2 = models.CharField(db_column="FIELD2", max_length=30)
    id3 = models.IntegerField(db_column="ID3")
    field3 = models.CharField(db_column="FIELD3", max_length=30)
    id4 = models.IntegerField(db_column="ID4")
    field4 = models.CharField(db_column="FIELD4", max_length=30)

    class Meta:
        managed = True
        db_table = "ACTIVATION_ANSWER_LOG"


class ActivationLog(models.Model):
    activation_log_id = models.AutoField(
        db_column="ACTIVATION_LOG_ID", primary_key=True
    )
    id = models.IntegerField(db_column="ID")
    user_id = models.IntegerField(db_column="USER_ID")
    action = models.CharField(db_column="ACTION", max_length=500)
    data = models.TextField(db_column="DATA", blank=True, null=True)
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")

    class Meta:
        managed = True
        db_table = "ACTIVATION_LOG"


class ActivationCallbackExclude(models.Model):
    activation_callback_exclude_id = models.AutoField(
        db_column="ACTIVATION_CALLBACK_EXCLUDE_ID", primary_key=True
    )
    service_id = models.IntegerField(db_column="SERVICE_ID")

    class Meta:
        managed = True
        db_table = "ACTIVATION_CALLBACK_EXCLUDE"


class ActivationCallbackNotice(models.Model):
    activation_callback_notice_id = models.AutoField(
        db_column="ACTIVATION_CALLBACK_NOTICE_ID", primary_key=True
    )
    activation = models.ForeignKey(
        "Activation", on_delete=models.CASCADE, db_column="ACTIVATION_ID"
    )
    circulation = models.ForeignKey(
        "Circulation", on_delete=models.CASCADE, db_column="CIRCULATION_ID"
    )
    send_date = models.DateTimeField(db_column="SEND_DATE")
    reason = models.TextField(db_column="REASON")

    class Meta:
        managed = True
        db_table = "ACTIVATION_CALLBACK_NOTICE"


class AirAction(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    available_instance_resource = models.ForeignKey(
        "AvailableInstanceResource",
        models.CASCADE,
        db_column="AVAILABLE_INSTANCE_RESOURCE_ID",
        related_name="+",
    )
    action_name = models.CharField(db_column="ACTION_NAME", max_length=50)
    hidden = models.PositiveSmallIntegerField(db_column="HIDDEN")

    class Meta:
        managed = True
        db_table = "AIR_ACTION"
        unique_together = (("available_instance_resource", "action_name"),)


class Answer(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    instance = models.ForeignKey(
        "instance.Instance",
        models.CASCADE,
        db_column="INSTANCE_ID",
        related_name="answers",
    )
    question = models.ForeignKey(
        "Question", models.DO_NOTHING, db_column="QUESTION_ID", related_name="+"
    )
    chapter = models.ForeignKey(
        "Chapter", models.DO_NOTHING, db_column="CHAPTER_ID", related_name="+"
    )
    item = models.IntegerField(db_column="ITEM")
    answer = models.TextField(db_column="ANSWER")

    @staticmethod
    def get_value_by_cqi(
        instance, chapter, question, item, *, default=None, fail_on_not_found=False
    ):
        """
        Fetch CAMAC form answer specified by a CQI triplet for the given instance.

        CQI is ChapterID, QuestionID, Item and is used a lot in "old" CAMAC

        By default, returns `None` if the answer is not found, but can be told
        to raise an exception by passing `fail_on_not_found=True`. You can also
        pass in another fallback value by passing `default=your_value`.
        """

        def _json_valid_or_none(data):
            try:
                return json.loads(data)
            except json.decoder.JSONDecodeError:
                return None

        try:
            ans = Answer.objects.get(
                instance=instance, question=question, chapter=chapter, item=item
            )
            option_values = _json_valid_or_none(ans.answer)
            if option_values and ans.question.answerlist.exists():
                # make the extra effort to get the correct ordering
                option_labels = {
                    vl.value: vl.get_name()
                    for vl in ans.question.answerlist.all().filter(
                        value__in=option_values
                    )
                }
                return ", ".join(option_labels.get(val, "") for val in option_values)
            else:
                return ans.answer

        except Answer.DoesNotExist:
            if fail_on_not_found:
                raise
            return default

    class Meta:
        managed = True
        db_table = "ANSWER"
        unique_together = (("instance", "question", "chapter", "item"),)


class AnswerList(MultilingualModel, models.Model):
    answer_list_id = models.AutoField(db_column="ANSWER_LIST_ID", primary_key=True)
    question = models.ForeignKey(
        "Question", models.CASCADE, db_column="QUESTION_ID", related_name="answerlist"
    )
    value = models.CharField(db_column="VALUE", max_length=20)
    name = models.CharField(db_column="NAME", max_length=1000, blank=True, null=True)
    sort = models.IntegerField(db_column="SORT")

    class Meta:
        managed = True
        db_table = "ANSWER_LIST"


class AnswerListT(models.Model):
    answer_list = models.ForeignKey(
        AnswerList, models.CASCADE, db_column="ANSWER_LIST_ID", related_name="trans"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=1000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "ANSWER_LIST_T"


class AnswerLog(models.Model):
    answer_log_id = models.AutoField(db_column="ANSWER_LOG_ID", primary_key=True)
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")
    user_id = models.IntegerField(db_column="USER_ID")
    action = models.CharField(db_column="ACTION", max_length=500)
    data = models.TextField(db_column="DATA", blank=True, null=True)
    id1 = models.IntegerField(db_column="ID1")
    field1 = models.CharField(db_column="FIELD1", max_length=30)
    id2 = models.IntegerField(db_column="ID2")
    field2 = models.CharField(db_column="FIELD2", max_length=30)
    id3 = models.IntegerField(db_column="ID3")
    field3 = models.CharField(db_column="FIELD3", max_length=30)
    id4 = models.IntegerField(db_column="ID4")
    field4 = models.CharField(db_column="FIELD4", max_length=30)

    class Meta:
        managed = True
        db_table = "ANSWER_LOG"


class AnswerQuery(models.Model):
    answer_query_id = models.AutoField(db_column="ANSWER_QUERY_ID", primary_key=True)
    name = models.CharField(db_column="NAME", max_length=50)
    query = models.CharField(db_column="QUERY", max_length=4000)

    class Meta:
        managed = True
        db_table = "ANSWER_QUERY"


class ArAction(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    available_resource = models.ForeignKey(
        "AvailableResource",
        models.CASCADE,
        db_column="AVAILABLE_RESOURCE_ID",
        related_name="+",
    )
    action_name = models.CharField(db_column="ACTION_NAME", max_length=50)
    hidden = models.PositiveSmallIntegerField(db_column="HIDDEN")

    class Meta:
        managed = True
        db_table = "AR_ACTION"
        unique_together = (("available_resource", "action_name"),)


class Authority(models.Model):
    authority_id = models.AutoField(db_column="AUTHORITY_ID", primary_key=True)
    name = models.CharField(db_column="NAME", max_length=128, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "AUTHORITY"


class AuthorityAuthorityType(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    authority = models.ForeignKey(
        Authority, models.CASCADE, db_column="AUTHORITY_ID", related_name="+"
    )
    authority_type = models.ForeignKey(
        "AuthorityType", models.CASCADE, db_column="AUTHORITY_TYPE_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "AUTHORITY_AUTHORITY_TYPE"


class AuthorityLocation(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    authority = models.ForeignKey(
        Authority, models.CASCADE, db_column="AUTHORITY_ID", related_name="+"
    )
    location = models.ForeignKey(
        "user.Location", models.CASCADE, db_column="LOCATION_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "AUTHORITY_LOCATION"
        unique_together = (("authority", "location"),)


class AuthorityType(models.Model):
    authority_type_id = models.AutoField(
        db_column="AUTHORITY_TYPE_ID", primary_key=True
    )
    tag = models.CharField(db_column="TAG", max_length=8)
    name = models.CharField(db_column="NAME", max_length=128)

    class Meta:
        managed = True
        db_table = "AUTHORITY_TYPE"


class AvailableAction(models.Model):
    available_action_id = models.CharField(
        db_column="AVAILABLE_ACTION_ID", primary_key=True, max_length=25
    )
    module_name = models.CharField(db_column="MODULE_NAME", max_length=50)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "AVAILABLE_ACTION"


class AvailableInstanceResource(models.Model):
    available_instance_resource_id = models.CharField(
        db_column="AVAILABLE_INSTANCE_RESOURCE_ID", primary_key=True, max_length=25
    )
    module_name = models.CharField(db_column="MODULE_NAME", max_length=50)
    controller_name = models.CharField(db_column="CONTROLLER_NAME", max_length=50)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "AVAILABLE_INSTANCE_RESOURCE"


class AvailableResource(models.Model):
    available_resource_id = models.CharField(
        db_column="AVAILABLE_RESOURCE_ID", primary_key=True, max_length=25
    )
    module_name = models.CharField(db_column="MODULE_NAME", max_length=50)
    controller_name = models.CharField(db_column="CONTROLLER_NAME", max_length=50)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "AVAILABLE_RESOURCE"


class BGroupAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    button = models.ForeignKey(
        "Button", models.CASCADE, db_column="BUTTON_ID", related_name="+"
    )
    group = models.ForeignKey(
        "user.Group", models.CASCADE, db_column="GROUP_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "B_GROUP_ACL"
        unique_together = (("button", "group", "instance_state"),)


class BRoleAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    button = models.ForeignKey(
        "Button", models.CASCADE, db_column="BUTTON_ID", related_name="+"
    )
    role = models.ForeignKey(
        "user.Role", models.CASCADE, db_column="ROLE_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "B_ROLE_ACL"
        unique_together = (("button", "role", "instance_state"),)


class BServiceAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    button = models.ForeignKey(
        "Button", models.CASCADE, db_column="BUTTON_ID", related_name="+"
    )
    service = models.ForeignKey(
        "user.Service", models.CASCADE, db_column="SERVICE_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "B_SERVICE_ACL"
        unique_together = (("button", "service", "instance_state"),)


class BUserAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    button = models.ForeignKey(
        "Button", models.CASCADE, db_column="BUTTON_ID", related_name="+"
    )
    user = models.ForeignKey(
        "user.User", models.CASCADE, db_column="USER_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "B_USER_ACL"
        unique_together = (("button", "user", "instance_state"),)


class BabUsage(models.Model):
    instance = models.ForeignKey(
        "instance.Instance",
        models.DO_NOTHING,
        db_column="INSTANCE_ID",
        related_name="+",
    )
    usage_type = models.IntegerField(db_column="USAGE_TYPE")
    usage = models.FloatField(db_column="USAGE")

    class Meta:
        managed = True
        db_table = "BAB_USAGE"
        unique_together = (("instance", "usage_type"),)


class BillingAccount(models.Model):
    billing_account_id = models.AutoField(
        db_column="BILLING_ACCOUNT_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=500)
    account_number = models.CharField(
        db_column="ACCOUNT_NUMBER", max_length=50, blank=True, null=True
    )
    department = models.CharField(
        db_column="DEPARTMENT", max_length=255, blank=True, null=True
    )
    predefined = models.PositiveSmallIntegerField(db_column="PREDEFINED", default=0)
    service_group = models.ForeignKey(
        "user.ServiceGroup",
        models.CASCADE,
        db_column="SERVICE_GROUP_ID",
        related_name="+",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "BILLING_ACCOUNT"


class BillingAccountState(models.Model):
    billing_account_state_id = models.AutoField(
        db_column="BILLING_ACCOUNT_STATE_ID", primary_key=True
    )
    billing_account = models.ForeignKey(
        BillingAccount, models.CASCADE, db_column="BILLING_ACCOUNT_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "BILLING_ACCOUNT_STATE"


class BillingConfig(models.Model):
    billing_config_id = models.AutoField(
        db_column="BILLING_CONFIG_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=100)
    value = models.CharField(db_column="VALUE", max_length=300)

    class Meta:
        managed = True
        db_table = "BILLING_CONFIG"


class BillingEntry(models.Model):
    billing_entry_id = models.AutoField(db_column="BILLING_ENTRY_ID", primary_key=True)
    amount = models.FloatField(db_column="AMOUNT")
    billing_account = models.ForeignKey(
        BillingAccount,
        models.DO_NOTHING,
        db_column="BILLING_ACCOUNT_ID",
        related_name="+",
    )
    user = models.ForeignKey(
        "user.User", models.CASCADE, db_column="USER_ID", related_name="+", default=1
    )
    instance = models.ForeignKey(
        "instance.Instance",
        models.CASCADE,
        db_column="INSTANCE_ID",
        related_name="billing_entries",
    )
    service = models.ForeignKey(
        "user.Service",
        models.DO_NOTHING,
        db_column="SERVICE_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    created = models.DateTimeField(db_column="CREATED", null=True)
    amount_type = models.PositiveSmallIntegerField(db_column="AMOUNT_TYPE")
    type = models.PositiveSmallIntegerField(db_column="TYPE")
    reason = models.CharField(db_column="REASON", max_length=300, blank=True, null=True)
    invoiced = models.PositiveSmallIntegerField(db_column="INVOICED")
    invoice = models.ForeignKey(
        "BillingInvoice",
        models.DO_NOTHING,
        db_column="INVOICE_ID",
        null=True,
        related_name="billing_entries",
    )

    class Meta:
        managed = True
        db_table = "BILLING_ENTRY"


class BillingInvoice(models.Model):
    billing_invoice_id = models.AutoField(
        db_column="BILLING_INVOICE_ID", primary_key=True
    )
    created = models.DateTimeField(db_column="CREATED")
    attachment = models.ForeignKey(
        "document.Attachment",
        models.DO_NOTHING,
        db_column="ATTACHMENT_ID",
        related_name="billing_invoices",
    )
    type = models.TextField(db_column="TYPE")

    class Meta:
        managed = True
        db_table = "BILLING_INVOICE"


class BuildingAuthorityButton(models.Model):
    building_authority_button_id = models.AutoField(
        db_column="BUILDING_AUTHORITY_BUTTON_ID", primary_key=True
    )
    label = models.CharField(db_column="LABEL", max_length=512)

    class Meta:
        managed = True
        db_table = "BUILDING_AUTHORITY_BUTTON"


class BuildingAuthorityButtonstate(models.Model):
    ba_button_state_id = models.AutoField(
        db_column="BA_BUTTON_STATE_ID", primary_key=True
    )
    building_authority_button = models.ForeignKey(
        BuildingAuthorityButton,
        models.DO_NOTHING,
        db_column="BUILDING_AUTHORITY_BUTTON_ID",
        related_name="+",
    )
    instance = models.ForeignKey(
        "instance.Instance", models.CASCADE, db_column="INSTANCE_ID", related_name="+"
    )
    is_clicked = models.PositiveSmallIntegerField(db_column="IS_CLICKED", default=0)
    is_disabled = models.PositiveSmallIntegerField(db_column="IS_DISABLED", default=0)

    class Meta:
        managed = True
        db_table = "BUILDING_AUTHORITY_BUTTONSTATE"


class BuildingAuthorityComment(models.Model):
    building_authority_comment_id = models.AutoField(
        db_column="BUILDING_AUTHORITY_COMMENT_ID", primary_key=True
    )
    building_authority_section = models.ForeignKey(
        "BuildingAuthoritySection",
        models.DO_NOTHING,
        db_column="BUILDING_AUTHORITY_SECTION_ID",
        related_name="+",
    )
    text = models.CharField(db_column="TEXT", max_length=4000, blank=True, null=True)
    group = models.FloatField(db_column="GROUP")
    instance = models.ForeignKey(
        "instance.Instance", models.DO_NOTHING, db_column="INSTANCE_ID"
    )

    class Meta:
        managed = True
        db_table = "BUILDING_AUTHORITY_COMMENT"
        unique_together = (("building_authority_section", "group", "instance"),)


class BuildingAuthorityDoc(models.Model):
    building_authority_doc_id = models.AutoField(
        db_column="BUILDING_AUTHORITY_DOC_ID", primary_key=True
    )
    building_authority_button = models.ForeignKey(
        BuildingAuthorityButton,
        models.CASCADE,
        db_column="BUILDING_AUTHORITY_BUTTON_ID",
        related_name="+",
    )
    template_class = models.ForeignKey(
        "DocgenTemplateClass",
        models.CASCADE,
        db_column="TEMPLATE_CLASS_ID",
        related_name="+",
    )
    template = models.ForeignKey(
        "DocgenTemplate", models.CASCADE, db_column="TEMPLATE_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "BUILDING_AUTHORITY_DOC"


class BuildingAuthorityEmail(models.Model):
    building_authority_email_id = models.AutoField(
        db_column="BUILDING_AUTHORITY_EMAIL_ID", primary_key=True
    )
    building_authority_button = models.ForeignKey(
        BuildingAuthorityButton,
        models.CASCADE,
        db_column="BUILDING_AUTHORITY_BUTTON_ID",
        related_name="+",
    )
    email_text = models.CharField(
        db_column="EMAIL_TEXT", max_length=4000, blank=True, null=True
    )
    receiver_query = models.CharField(
        db_column="RECEIVER_QUERY", max_length=4000, blank=True, null=True
    )
    email_subject = models.CharField(
        db_column="EMAIL_SUBJECT", max_length=400, blank=True, null=True
    )
    from_email = models.CharField(
        db_column="FROM_EMAIL", max_length=400, blank=True, null=True
    )
    from_name = models.CharField(
        db_column="FROM_NAME", max_length=400, blank=True, null=True
    )
    attachment_section = models.ForeignKey(
        "document.AttachmentSection",
        models.DO_NOTHING,
        db_column="ATTACHMENT_SECTION_ID",
        blank=True,
        null=True,
        related_name="+",
    )
    workflow_item = models.ForeignKey(
        "WorkflowItem",
        models.DO_NOTHING,
        db_column="WORKFLOW_ITEM_ID",
        blank=True,
        null=True,
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "BUILDING_AUTHORITY_EMAIL"


class BuildingAuthorityItemDis(models.Model):
    ba_item_dis_id = models.AutoField(db_column="BA_ITEM_DIS_ID", primary_key=True)
    workflow_item = models.ForeignKey(
        "WorkflowItem",
        models.DO_NOTHING,
        db_column="WORKFLOW_ITEM_ID",
        related_name="+",
    )
    instance = models.ForeignKey(
        "instance.Instance",
        models.DO_NOTHING,
        db_column="INSTANCE_ID",
        related_name="+",
    )
    group = models.FloatField(db_column="GROUP")

    class Meta:
        managed = True
        db_table = "BUILDING_AUTHORITY_ITEM_DIS"


class BuildingAuthoritySection(models.Model):
    building_authority_section_id = models.AutoField(
        db_column="BUILDING_AUTHORITY_SECTION_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=128)

    class Meta:
        managed = True
        db_table = "BUILDING_AUTHORITY_SECTION"


class BuildingAuthoritySectionDis(models.Model):
    ba_section_dis_id = models.AutoField(
        db_column="BA_SECTION_DIS_ID", primary_key=True
    )
    instance = models.ForeignKey(
        "instance.Instance",
        models.DO_NOTHING,
        db_column="INSTANCE_ID",
        related_name="+",
    )
    ba_section = models.ForeignKey(
        BuildingAuthoritySection,
        models.DO_NOTHING,
        db_column="BA_SECTION_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "BUILDING_AUTHORITY_SECTION_DIS"


class Button(MultilingualModel, models.Model):
    button_id = models.AutoField(db_column="BUTTON_ID", primary_key=True)
    instance_resource = models.ForeignKey(
        "InstanceResource",
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        related_name="buttons",
    )
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )
    # Field renamed because it was a Python reserved word.
    class_field = models.CharField(
        db_column="CLASS", max_length=250, blank=True, null=True
    )
    hidden = models.PositiveSmallIntegerField(db_column="HIDDEN")
    sort = models.IntegerField(db_column="SORT")

    class Meta:
        managed = True
        db_table = "BUTTON"


class ButtonT(models.Model):
    button = models.ForeignKey(
        Button, models.CASCADE, db_column="BUTTON_ID", related_name="trans"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "BUTTON_T"


class Chapter(MultilingualModel, models.Model):
    chapter_id = models.AutoField(db_column="CHAPTER_ID", primary_key=True)
    name = models.CharField(db_column="NAME", max_length=500, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )
    javascript = models.CharField(
        db_column="JAVASCRIPT", max_length=4000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "CHAPTER"


class ChapterPage(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    chapter = models.ForeignKey(
        Chapter, models.CASCADE, db_column="CHAPTER_ID", related_name="+"
    )
    page = models.ForeignKey(
        "Page", models.CASCADE, db_column="PAGE_ID", related_name="+"
    )
    sort = models.IntegerField(db_column="SORT")

    class Meta:
        managed = True
        db_table = "CHAPTER_PAGE"
        unique_together = (("chapter", "page"),)


class ChapterPageGroupAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    chapter = models.ForeignKey(
        ChapterPage, models.CASCADE, db_column="CHAPTER_ID", related_name="+"
    )
    page = models.ForeignKey(
        ChapterPage, models.CASCADE, db_column="PAGE_ID", related_name="+"
    )
    group = models.ForeignKey(
        "user.Group", models.CASCADE, db_column="GROUP_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "CHAPTER_PAGE_GROUP_ACL"
        unique_together = (("chapter", "page", "group", "instance_state"),)


class ChapterPageRoleAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    chapter = models.ForeignKey(
        ChapterPage, models.CASCADE, db_column="CHAPTER_ID", related_name="+"
    )
    page = models.ForeignKey(
        ChapterPage, models.CASCADE, db_column="PAGE_ID", related_name="+"
    )
    role = models.ForeignKey(
        "user.Role", models.CASCADE, db_column="ROLE_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "CHAPTER_PAGE_ROLE_ACL"
        unique_together = (("chapter", "page", "role", "instance_state"),)


class ChapterPageServiceAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    chapter = models.ForeignKey(
        ChapterPage, models.CASCADE, db_column="CHAPTER_ID", related_name="+"
    )
    page = models.ForeignKey(
        ChapterPage, models.CASCADE, db_column="PAGE_ID", related_name="+"
    )
    service = models.ForeignKey(
        "user.Service", models.CASCADE, db_column="SERVICE_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "CHAPTER_PAGE_SERVICE_ACL"
        unique_together = (("chapter", "page", "service", "instance_state"),)


class ChapterPageUserAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    chapter = models.ForeignKey(
        ChapterPage, models.CASCADE, db_column="CHAPTER_ID", related_name="+"
    )
    page = models.ForeignKey(
        ChapterPage, models.CASCADE, db_column="PAGE_ID", related_name="+"
    )
    user = models.ForeignKey(
        "user.User", models.CASCADE, db_column="USER_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "CHAPTER_PAGE_USER_ACL"
        unique_together = (("chapter", "page", "user", "instance_state"),)


class ChapterT(models.Model):
    chapter = models.ForeignKey(
        Chapter, models.CASCADE, db_column="CHAPTER_ID", related_name="trans"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=500, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "CHAPTER_T"


class Circulation(models.Model):
    circulation_id = models.AutoField(db_column="CIRCULATION_ID", primary_key=True)
    # While this "should" be a foreign key, we decouple to be able
    # to separate config from data models
    # references IrEditcirculation
    instance_resource_id = models.IntegerField(
        db_column="INSTANCE_RESOURCE_ID", db_index=True
    )
    instance = models.ForeignKey(
        "instance.Instance",
        models.CASCADE,
        db_column="INSTANCE_ID",
        related_name="circulations",
    )
    service = models.ForeignKey(
        "user.Service",
        models.DO_NOTHING,
        db_column="SERVICE_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    name = models.CharField(db_column="NAME", max_length=50)

    class Meta:
        managed = True
        db_table = "CIRCULATION"


class CirculationAnswer(MultilingualModel, models.Model):
    circulation_answer_id = models.AutoField(
        db_column="CIRCULATION_ANSWER_ID", primary_key=True
    )
    circulation_type = models.ForeignKey(
        "CirculationType",
        models.CASCADE,
        db_column="CIRCULATION_TYPE_ID",
        related_name="+",
    )
    circulation_answer_type = models.ForeignKey(
        "CirculationAnswerType",
        models.CASCADE,
        db_column="CIRCULATION_ANSWER_TYPE_ID",
        related_name="+",
    )
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)
    sort = models.IntegerField(db_column="SORT")

    class Meta:
        managed = True
        db_table = "CIRCULATION_ANSWER"


class CirculationAnswerT(models.Model):
    circulation_answer = models.ForeignKey(
        CirculationAnswer,
        models.CASCADE,
        db_column="CIRCULATION_ANSWER_ID",
        related_name="trans",
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "CIRCULATION_ANSWER_T"


class CirculationAnswerType(MultilingualModel, models.Model):
    circulation_answer_type_id = models.AutoField(
        db_column="CIRCULATION_ANSWER_TYPE_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "CIRCULATION_ANSWER_TYPE"


class CirculationAnswerTypeT(models.Model):
    circulation_answer_type = models.ForeignKey(
        CirculationAnswerType,
        models.CASCADE,
        db_column="CIRCULATION_ANSWER_TYPE_ID",
        related_name="trans",
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "CIRCULATION_ANSWER_TYPE_T"


class CirculationLog(models.Model):
    circulation_log_id = models.AutoField(
        db_column="CIRCULATION_LOG_ID", primary_key=True
    )
    id = models.IntegerField(db_column="ID")
    user_id = models.IntegerField(db_column="USER_ID")
    action = models.CharField(db_column="ACTION", max_length=500)
    data = models.TextField(db_column="DATA", blank=True, null=True)
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")

    class Meta:
        managed = True
        db_table = "CIRCULATION_LOG"


class CirculationReason(MultilingualModel, models.Model):
    circulation_reason_id = models.AutoField(
        db_column="CIRCULATION_REASON_ID", primary_key=True
    )
    circulation_type = models.ForeignKey(
        "CirculationType",
        models.CASCADE,
        db_column="CIRCULATION_TYPE_ID",
        related_name="+",
    )
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)
    sort = models.IntegerField(db_column="SORT")

    class Meta:
        managed = True
        db_table = "CIRCULATION_REASON"


class CirculationReasonT(models.Model):
    circulation_reason = models.ForeignKey(
        CirculationReason,
        models.CASCADE,
        db_column="CIRCULATION_REASON_ID",
        related_name="trans",
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "CIRCULATION_REASON_T"


class CirculationState(MultilingualModel, models.Model):
    circulation_state_id = models.AutoField(
        db_column="CIRCULATION_STATE_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=100, blank=True, null=True)
    sort = models.IntegerField(db_column="SORT")

    class Meta:
        managed = True
        db_table = "CIRCULATION_STATE"


class CirculationStateT(models.Model):
    circulation_state_id = models.ForeignKey(
        CirculationState,
        models.CASCADE,
        db_column="CIRCULATION_STATE_ID",
        related_name="trans",
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "CIRCULATION_STATE_T"


class CirculationType(MultilingualModel, models.Model):
    circulation_type_id = models.AutoField(
        db_column="CIRCULATION_TYPE_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)
    # While this "should" be a foreign key, we decouple to be able
    # to separate config from data models
    # references Page
    page_id = models.IntegerField(db_column="PAGE_ID", db_index=True, null=True)
    parent_specific_activations = models.PositiveSmallIntegerField(
        db_column="PARENT_SPECIFIC_ACTIVATIONS"
    )

    class Meta:
        managed = True
        db_table = "CIRCULATION_TYPE"


class CommissionAssignment(models.Model):
    commission_assignment_id = models.AutoField(
        db_column="COMMISSION_ASSIGNMENT_ID", primary_key=True
    )
    group = models.ForeignKey(
        "user.Group", models.DO_NOTHING, db_column="GROUP_ID", related_name="+"
    )
    instance = models.ForeignKey(
        "instance.Instance",
        models.DO_NOTHING,
        db_column="INSTANCE_ID",
        related_name="+",
    )
    creator_group = models.ForeignKey(
        "user.Group",
        models.DO_NOTHING,
        db_column="CREATOR_GROUP_ID",
        related_name="+",
        null=True,
    )
    creator_user = models.FloatField(db_column="CREATOR_USER_ID")
    date = models.DateTimeField(db_column="DATE")

    class Meta:
        managed = True
        db_table = "COMMISSION_ASSIGNMENT"
        unique_together = (("group", "instance"),)


class DocgenActivationAction(models.Model):
    docgen_activation_action_id = models.AutoField(
        db_column="DOCGEN_ACTIVATION_ACTION_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=255)

    class Meta:
        managed = True
        db_table = "DOCGEN_ACTIVATION_ACTION"


class DocgenActivationDocket(models.Model):
    docgen_activation_docket_id = models.AutoField(
        db_column="DOCGEN_ACTIVATION_DOCKET_ID", primary_key=True
    )
    instance = models.ForeignKey(
        "instance.Instance", models.CASCADE, db_column="INSTANCE_ID", related_name="+"
    )
    activation = models.ForeignKey(
        Activation,
        models.CASCADE,
        db_column="ACTIVATION_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    text = models.TextField(db_column="TEXT")

    class Meta:
        managed = True
        db_table = "DOCGEN_ACTIVATION_DOCKET"


class DocgenActivationactionAction(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    docgen_activation_action = models.ForeignKey(
        DocgenActivationAction,
        models.CASCADE,
        db_column="DOCGEN_ACTIVATION_ACTION_ID",
        related_name="+",
    )
    action = models.ForeignKey(
        Action, models.CASCADE, db_column="ACTION_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "DOCGEN_ACTIVATIONACTION_ACTION"
        unique_together = (("docgen_activation_action", "action"),)


class DocgenDocxAction(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    docgen_template = models.ForeignKey(
        "DocgenTemplate",
        models.CASCADE,
        db_column="DOCGEN_TEMPLATE_ID",
        related_name="+",
    )
    docgen_template_class = models.ForeignKey(
        "DocgenTemplateClass",
        models.CASCADE,
        db_column="DOCGEN_TEMPLATE_CLASS_ID",
        related_name="+",
    )
    action = models.ForeignKey(
        Action, models.CASCADE, db_column="ACTION_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "DOCGEN_DOCX_ACTION"
        unique_together = (("docgen_template", "docgen_template_class", "action"),)


class TemplateGenerateAction(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    template = models.ForeignKey(
        "document.Template", models.CASCADE, db_column="TEMPLATE_ID", related_name="+"
    )
    action = models.ForeignKey(
        Action, models.CASCADE, db_column="ACTION_ID", related_name="+"
    )
    as_pdf = models.PositiveSmallIntegerField(db_column="AS_PDF", default=0)

    class Meta:
        managed = True
        db_table = "TEMPLATE_GENERATE_ACTION"
        unique_together = (("as_pdf", "template", "action"),)


class CirculationTypeT(models.Model):
    circulation_type = models.ForeignKey(
        CirculationType,
        models.CASCADE,
        db_column="CIRCULATION_TYPE_ID",
        related_name="trans",
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "CIRCULATION_TYPE_T"


class DocgenPdfAction(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    docgen_template = models.ForeignKey(
        "DocgenTemplate",
        models.CASCADE,
        db_column="DOCGEN_TEMPLATE_ID",
        related_name="+",
    )
    docgen_template_class = models.ForeignKey(
        "DocgenTemplateClass",
        models.CASCADE,
        db_column="DOCGEN_TEMPLATE_CLASS_ID",
        related_name="+",
    )
    action = models.ForeignKey(
        Action, models.CASCADE, db_column="ACTION_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "DOCGEN_PDF_ACTION"
        unique_together = (("docgen_template", "docgen_template_class", "action"),)


class DocgenTemplate(models.Model):
    docgen_template_id = models.AutoField(
        db_column="DOCGEN_TEMPLATE_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=255)
    path = models.CharField(db_column="PATH", max_length=255)
    type = models.FloatField(db_column="TYPE")

    class Meta:
        managed = True
        db_table = "DOCGEN_TEMPLATE"


class DocgenTemplateClass(models.Model):
    docgen_template_class_id = models.AutoField(
        db_column="DOCGEN_TEMPLATE_CLASS_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=255)
    path = models.CharField(db_column="PATH", max_length=255)
    type = models.FloatField(db_column="TYPE")

    class Meta:
        managed = True
        db_table = "DOCGEN_TEMPLATE_CLASS"


class FormGroup(MultilingualModel, models.Model):
    form_group_id = models.AutoField(db_column="FORM_GROUP_ID", primary_key=True)
    name = models.CharField(db_column="NAME", max_length=500, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "FORM_GROUP"


class FormGroupForm(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    form_group = models.ForeignKey(
        FormGroup, models.CASCADE, db_column="FORM_GROUP_ID", related_name="forms"
    )
    form = models.ForeignKey(
        "instance.Form", models.CASCADE, db_column="FORM_ID", related_name="form_group"
    )

    class Meta:
        managed = True
        db_table = "FORM_GROUP_FORM"
        unique_together = (("form_group", "form"),)


class FormGroupT(models.Model):
    form_group = models.ForeignKey(
        FormGroup, models.CASCADE, db_column="FORM_GROUP_ID", related_name="trans"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=500, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "FORM_GROUP_T"


class GroupPermission(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    group = models.ForeignKey(
        "user.Group", models.DO_NOTHING, db_column="GROUP_ID", related_name="+"
    )
    permission_id = models.CharField(db_column="PERMISSION_ID", max_length=100)

    class Meta:
        managed = True
        db_table = "GROUP_PERMISSION"
        unique_together = (("group", "permission_id"),)


class InstanceDemo(models.Model):
    instance_demo = models.OneToOneField(
        "instance.Instance",
        models.DO_NOTHING,
        db_column="INSTANCE_DEMO_ID",
        primary_key=True,
        related_name="+",
    )
    value = models.CharField(db_column="VALUE", max_length=1000, blank=True, null=True)
    automatic_date = models.DateTimeField(
        db_column="AUTOMATIC_DATE", blank=True, null=True
    )
    form_date = models.DateTimeField(db_column="FORM_DATE", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "INSTANCE_DEMO"


class InstanceDemoLog(models.Model):
    instance_demo_log_id = models.AutoField(
        db_column="INSTANCE_DEMO_LOG_ID", primary_key=True
    )
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")
    user_id = models.IntegerField(db_column="USER_ID")
    action = models.CharField(db_column="ACTION", max_length=500)
    data = models.TextField(db_column="DATA")
    id = models.IntegerField(db_column="ID")

    class Meta:
        managed = True
        db_table = "INSTANCE_DEMO_LOG"


class InstanceFormPdf(models.Model):
    instance_form_pdf_id = models.AutoField(
        db_column="INSTANCE_FORM_PDF_ID", primary_key=True
    )
    instance = models.ForeignKey(
        "instance.Instance",
        models.DO_NOTHING,
        db_column="INSTANCE_ID",
        related_name="+",
    )
    action = models.ForeignKey(
        Action, models.DO_NOTHING, db_column="ACTION_ID", related_name="+"
    )
    user = models.ForeignKey(
        "user.User", models.DO_NOTHING, db_column="USER_ID", related_name="+"
    )
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")
    name = models.CharField(db_column="NAME", max_length=50)
    filename = models.CharField(db_column="FILENAME", max_length=50)

    class Meta:
        managed = True
        db_table = "INSTANCE_FORM_PDF"


class InstanceFormwizard(models.Model):
    instance = models.OneToOneField(
        "instance.Instance",
        models.DO_NOTHING,
        db_column="INSTANCE_ID",
        primary_key=True,
        related_name="+",
    )
    pages = models.CharField(db_column="PAGES", max_length=500)

    class Meta:
        managed = True
        db_table = "INSTANCE_FORMWIZARD"


class InstanceFormwizardLog(models.Model):
    instance_formwizard_log_id = models.AutoField(
        db_column="INSTANCE_FORMWIZARD_LOG_ID", primary_key=True
    )
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")
    user_id = models.IntegerField(db_column="USER_ID")
    action = models.CharField(db_column="ACTION", max_length=500)
    data = models.TextField(db_column="DATA")
    id = models.IntegerField(db_column="ID")

    class Meta:
        managed = True
        db_table = "INSTANCE_FORMWIZARD_LOG"


class InstanceGuest(models.Model):
    instance = models.OneToOneField(
        "instance.Instance",
        models.DO_NOTHING,
        db_column="INSTANCE_ID",
        primary_key=True,
        related_name="+",
    )
    session_id = models.CharField(db_column="SESSION_ID", max_length=128)
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")

    class Meta:
        managed = True
        db_table = "INSTANCE_GUEST"


class InstanceLocation(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    location = models.ForeignKey(
        "user.Location", models.DO_NOTHING, db_column="LOCATION_ID", related_name="+"
    )
    instance = models.ForeignKey(
        "instance.Instance", models.CASCADE, db_column="INSTANCE_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "INSTANCE_LOCATION"
        unique_together = (("location", "instance"),)


class InstanceLocationLog(models.Model):
    instance_location_log_id = models.AutoField(
        db_column="INSTANCE_LOCATION_LOG_ID", primary_key=True
    )
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")
    user_id = models.IntegerField(db_column="USER_ID")
    action = models.CharField(db_column="ACTION", max_length=500)
    data = models.TextField(db_column="DATA", blank=True, null=True)
    id1 = models.IntegerField(db_column="ID1")
    field1 = models.CharField(db_column="FIELD1", max_length=30)
    id2 = models.IntegerField(db_column="ID2")
    field2 = models.CharField(db_column="FIELD2", max_length=30)

    class Meta:
        managed = True
        db_table = "INSTANCE_LOCATION_LOG"


class InstanceLog(models.Model):
    instance_log_id = models.AutoField(db_column="INSTANCE_LOG_ID", primary_key=True)
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")
    user_id = models.IntegerField(db_column="USER_ID")
    action = models.CharField(db_column="ACTION", max_length=500)
    data = models.TextField(db_column="DATA", blank=True, null=True)
    id = models.IntegerField(db_column="ID")

    class Meta:
        managed = True
        db_table = "INSTANCE_LOG"


class InstancePortal(models.Model):
    # TODO Why isn't this a foreign key?
    instance_id = models.AutoField(db_column="INSTANCE_ID", primary_key=True)
    portal_identifier = models.CharField(db_column="PORTAL_IDENTIFIER", max_length=256)
    # Once all rows have been migrated this model can be deleted.
    migrated = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = "INSTANCE_PORTAL"


class InstanceResource(MultilingualModel, models.Model):
    instance_resource_id = models.AutoField(
        db_column="INSTANCE_RESOURCE_ID", primary_key=True
    )
    available_instance_resource = models.ForeignKey(
        AvailableInstanceResource,
        models.CASCADE,
        db_column="AVAILABLE_INSTANCE_RESOURCE_ID",
        related_name="+",
    )
    resource = models.ForeignKey(
        "Resource", models.CASCADE, db_column="RESOURCE_ID", related_name="+"
    )
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )
    template = models.CharField(
        db_column="TEMPLATE", max_length=500, blank=True, null=True
    )
    # Field renamed because it was a Python reserved word.
    class_field = models.CharField(
        db_column="CLASS", max_length=250, blank=True, null=True
    )
    hidden = models.PositiveSmallIntegerField(db_column="HIDDEN")
    sort = models.IntegerField(db_column="SORT")
    form_group = models.ForeignKey(
        FormGroup, models.CASCADE, db_column="FORM_GROUP_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "INSTANCE_RESOURCE"
        ordering = ["resource__sort", "sort"]


class InstanceResourceAction(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    available_instance_resource = models.ForeignKey(
        AvailableInstanceResource,
        models.CASCADE,
        db_column="AVAILABLE_INSTANCE_RESOURCE_ID",
        related_name="+",
    )
    available_action = models.ForeignKey(
        AvailableAction,
        models.CASCADE,
        db_column="AVAILABLE_ACTION_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "INSTANCE_RESOURCE_ACTION"
        unique_together = (("available_instance_resource", "available_action"),)


class InstanceResourceT(models.Model):
    instance_resource = models.ForeignKey(
        InstanceResource,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        related_name="trans",
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "INSTANCE_RESOURCE_T"


class IrAllformpages(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    page_form_group = models.ForeignKey(
        "PageFormGroup",
        models.CASCADE,
        db_column="PAGE_FORM_GROUP_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    pdf_class = models.CharField(
        db_column="PDF_CLASS", max_length=500, blank=True, null=True
    )
    show_all_page_form_mode = models.PositiveSmallIntegerField(
        db_column="SHOW_ALL_PAGE_FORM_MODE"
    )

    class Meta:
        managed = True
        db_table = "IR_ALLFORMPAGES"


class IrCirculation(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    circulation_type = models.ForeignKey(
        CirculationType,
        models.CASCADE,
        db_column="CIRCULATION_TYPE_ID",
        related_name="+",
    )
    service = models.ForeignKey(
        "user.Service",
        models.CASCADE,
        db_column="SERVICE_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    draft_circulation_answer = models.ForeignKey(
        CirculationAnswer,
        models.CASCADE,
        db_column="DRAFT_CIRCULATION_ANSWER_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    show_notice = models.PositiveSmallIntegerField(db_column="SHOW_NOTICE")
    show_history = models.PositiveSmallIntegerField(db_column="SHOW_HISTORY")
    show_all_children = models.PositiveSmallIntegerField(db_column="SHOW_ALL_CHILDREN")
    read_notice_template = models.CharField(
        db_column="READ_NOTICE_TEMPLATE", max_length=500, blank=True, null=True
    )
    pdf_class = models.CharField(
        db_column="PDF_CLASS", max_length=500, blank=True, null=True
    )
    service_to_be_interpreted = models.CharField(
        db_column="SERVICE_TO_BE_INTERPRETED", max_length=50, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "IR_CIRCULATION"


class IrEditcirculation(MultilingualModel, models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    circulation_type = models.ForeignKey(
        CirculationType,
        models.CASCADE,
        db_column="CIRCULATION_TYPE_ID",
        related_name="+",
    )
    draft_circulation_answer = models.ForeignKey(
        CirculationAnswer,
        models.CASCADE,
        db_column="DRAFT_CIRCULATION_ANSWER_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    show_notice = models.PositiveSmallIntegerField(db_column="SHOW_NOTICE")
    add_template = models.CharField(
        db_column="ADD_TEMPLATE", max_length=500, blank=True, null=True
    )
    add_activation_template = models.CharField(
        db_column="ADD_ACTIVATION_TEMPLATE", max_length=500, blank=True, null=True
    )
    read_notice_template = models.CharField(
        db_column="READ_NOTICE_TEMPLATE", max_length=500, blank=True, null=True
    )
    pdf_class = models.CharField(
        db_column="PDF_CLASS", max_length=500, blank=True, null=True
    )
    default_circulation_name = models.CharField(
        db_column="DEFAULT_CIRCULATION_NAME", max_length=500, blank=True, null=True
    )
    single_circulation = models.PositiveSmallIntegerField(
        db_column="SINGLE_CIRCULATION"
    )
    inherit_notices = models.PositiveSmallIntegerField(db_column="INHERIT_NOTICES")
    display_first_circulation = models.PositiveSmallIntegerField(
        db_column="DISPLAY_FIRST_CIRCULATION"
    )
    circulation_email_action_id = models.ForeignKey(
        Action,
        models.CASCADE,
        db_column="CIRCULATION_EMAIL_ACTION_ID",
        related_name="+",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.get_trans_attr("default_circulation_name")

    class Meta:
        managed = True
        db_table = "IR_EDITCIRCULATION"


class IrEditcirculationSg(models.Model):
    ir_editcirculation_sg_id = models.AutoField(
        db_column="IR_EDITCIRCULATION_SG_ID", primary_key=True
    )
    instance_resource = models.ForeignKey(
        IrEditcirculation,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        related_name="+",
    )
    service_group = models.ForeignKey(
        "user.ServiceGroup",
        models.CASCADE,
        db_column="SERVICE_GROUP_ID",
        related_name="+",
    )
    localized = models.PositiveSmallIntegerField(db_column="LOCALIZED")

    class Meta:
        managed = True
        db_table = "IR_EDITCIRCULATION_SG"


class IrEditcirculationT(models.Model):
    instance_resource = models.ForeignKey(
        IrEditcirculation,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        related_name="trans",
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    default_circulation_name = models.CharField(
        db_column="DEFAULT_CIRCULATION_NAME", max_length=500, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "IR_EDITCIRCULATION_T"


class IrEditformpage(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    page = models.ForeignKey(
        "Page", models.CASCADE, db_column="PAGE_ID", related_name="+"
    )
    pdf_class = models.CharField(
        db_column="PDF_CLASS", max_length=500, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "IR_EDITFORMPAGE"


class IrEditformpages(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    page_form_group = models.ForeignKey(
        "PageFormGroup",
        models.CASCADE,
        db_column="PAGE_FORM_GROUP_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    pdf_class = models.CharField(
        db_column="PDF_CLASS", max_length=500, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "IR_EDITFORMPAGES"


class IrEditletter(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    pdf_class = models.CharField(
        db_column="PDF_CLASS", max_length=500, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "IR_EDITLETTER"


class IrEditletterAnswer(MultilingualModel, models.Model):
    ir_editletter_answer_id = models.AutoField(
        db_column="IR_EDITLETTER_ANSWER_ID", primary_key=True
    )
    instance_resource = models.ForeignKey(
        IrEditletter, models.CASCADE, db_column="INSTANCE_RESOURCE_ID", related_name="+"
    )
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "IR_EDITLETTER_ANSWER"


class IrEditletterAnswerT(models.Model):
    ir_editletter_answer = models.ForeignKey(
        IrEditletterAnswer,
        models.CASCADE,
        db_column="IR_EDITLETTER_ANSWER_ID",
        related_name="trans",
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "IR_EDITLETTER_ANSWER_T"


class IrEditnotice(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    circulation_type = models.ForeignKey(
        CirculationType,
        models.CASCADE,
        db_column="CIRCULATION_TYPE_ID",
        related_name="+",
    )
    editable_after_deadline = models.PositiveSmallIntegerField(
        db_column="EDITABLE_AFTER_DEADLINE"
    )
    pdf_class = models.CharField(
        db_column="PDF_CLASS", max_length=500, blank=True, null=True
    )
    edit_notice_template = models.CharField(
        db_column="EDIT_NOTICE_TEMPLATE", max_length=500, blank=True, null=True
    )
    hide_answered_notices = models.PositiveSmallIntegerField(
        db_column="HIDE_ANSWERED_NOTICES"
    )
    is_always_editable = models.PositiveSmallIntegerField(
        db_column="IS_ALWAYS_EDITABLE"
    )

    class Meta:
        managed = True
        db_table = "IR_EDITNOTICE"


class IrFormerror(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    ir_editformpages = models.ForeignKey(
        IrEditformpages,
        models.CASCADE,
        db_column="IR_EDITFORMPAGES_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "IR_FORMERROR"


class IrFormpage(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    page = models.ForeignKey(
        "Page", models.CASCADE, db_column="PAGE_ID", related_name="+"
    )
    pdf_class = models.CharField(
        db_column="PDF_CLASS", max_length=500, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "IR_FORMPAGE"


class IrFormpages(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    page_form_group = models.ForeignKey(
        "PageFormGroup",
        models.CASCADE,
        db_column="PAGE_FORM_GROUP_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    pdf_class = models.CharField(
        db_column="PDF_CLASS", max_length=500, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "IR_FORMPAGES"


class IrFormwizard(MultilingualModel, models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    page_form_group = models.ForeignKey(
        "PageFormGroup",
        models.CASCADE,
        db_column="PAGE_FORM_GROUP_ID",
        related_name="+",
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )
    show_captcha = models.PositiveSmallIntegerField(db_column="SHOW_CAPTCHA")
    summary = models.CharField(
        db_column="SUMMARY", max_length=4000, blank=True, null=True
    )
    php_class = models.CharField(
        db_column="PHP_CLASS", max_length=500, blank=True, null=True
    )
    goto_second_page = models.PositiveSmallIntegerField(db_column="GOTO_SECOND_PAGE")
    hide_summary_page = models.PositiveSmallIntegerField(db_column="HIDE_SUMMARY_PAGE")
    hide_summary_questions = models.PositiveSmallIntegerField(
        db_column="HIDE_SUMMARY_QUESTIONS"
    )

    def __str__(self):
        return self.get_trans_attr("summary")

    class Meta:
        managed = True
        db_table = "IR_FORMWIZARD"


class IrFormwizardT(models.Model):
    instance_resource = models.ForeignKey(
        IrFormwizard,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        related_name="trans",
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    summary = models.CharField(
        db_column="SUMMARY", max_length=4000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "IR_FORMWIZARD_T"


class IrGroupAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    instance_resource = models.ForeignKey(
        InstanceResource,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        related_name="+",
    )
    group = models.ForeignKey(
        "user.Group", models.CASCADE, db_column="GROUP_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "IR_GROUP_ACL"
        unique_together = (("instance_resource", "group", "instance_state"),)


class IrLetter(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    ir_editletter_id = models.IntegerField(
        db_column="IR_EDITLETTER_ID", blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "IR_LETTER"


class IrNewform(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )
    page_form_group = models.ForeignKey(
        "PageFormGroup",
        models.CASCADE,
        db_column="PAGE_FORM_GROUP_ID",
        related_name="+",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "IR_NEWFORM"


class IrPage(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    pdf_class = models.CharField(
        db_column="PDF_CLASS", max_length=500, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "IR_PAGE"


class IrRoleAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    instance_resource = models.ForeignKey(
        InstanceResource,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        related_name="role_acls",
    )
    role = models.ForeignKey(
        "user.Role", models.CASCADE, db_column="ROLE_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "IR_ROLE_ACL"
        unique_together = (("instance_resource", "role", "instance_state"),)


class IrServiceAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    instance_resource = models.ForeignKey(
        InstanceResource,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        related_name="+",
    )
    service = models.ForeignKey(
        "user.Service", models.CASCADE, db_column="SERVICE_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "IR_SERVICE_ACL"
        unique_together = (("instance_resource", "service", "instance_state"),)


class IrUserAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    instance_resource = models.ForeignKey(
        InstanceResource,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        related_name="+",
    )
    user = models.ForeignKey(
        "user.User", models.CASCADE, db_column="USER_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "IR_USER_ACL"
        unique_together = (("instance_resource", "user", "instance_state"),)


class Letter(models.Model):
    instance = models.ForeignKey(
        "instance.Instance",
        models.DO_NOTHING,
        db_column="INSTANCE_ID",
        related_name="+",
    )
    instance_resource = models.ForeignKey(
        IrEditletter,
        models.DO_NOTHING,
        db_column="INSTANCE_RESOURCE_ID",
        related_name="+",
    )
    user = models.ForeignKey(
        "user.User", models.DO_NOTHING, db_column="USER_ID", related_name="+"
    )
    ir_editletter_answer = models.ForeignKey(
        IrEditletterAnswer,
        models.DO_NOTHING,
        db_column="IR_EDITLETTER_ANSWER_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    date = models.DateTimeField(db_column="DATE")
    name = models.CharField(db_column="NAME", max_length=50)
    content = models.TextField(db_column="CONTENT")
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")

    class Meta:
        managed = True
        db_table = "LETTER"
        unique_together = (("instance", "instance_resource"),)


class LetterImage(models.Model):
    letter_image_id = models.AutoField(db_column="LETTER_IMAGE_ID", primary_key=True)
    instance = models.ForeignKey(
        "instance.Instance",
        models.DO_NOTHING,
        db_column="INSTANCE_ID",
        related_name="+",
    )
    instance_resource = models.ForeignKey(
        InstanceResource,
        models.DO_NOTHING,
        db_column="INSTANCE_RESOURCE_ID",
        related_name="+",
    )
    user = models.ForeignKey(
        "user.User", models.DO_NOTHING, db_column="USER_ID", related_name="+"
    )
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")
    name = models.CharField(db_column="NAME", max_length=50)
    filename = models.CharField(db_column="FILENAME", max_length=50)

    class Meta:
        managed = True
        db_table = "LETTER_IMAGE"


class LoginAttempt(models.Model):
    login_attempt_id = models.AutoField(db_column="LOGIN_ATTEMPT_ID", primary_key=True)
    ip = models.CharField(db_column="IP", max_length=45)
    attempt_date = models.DateTimeField(db_column="ATTEMPT_DATE")
    username = models.CharField(
        db_column="USERNAME", max_length=250, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "LOGIN_ATTEMPT"


class Mapping(models.Model):
    mapping_id = models.AutoField(db_column="MAPPING_ID", primary_key=True)
    table_name = models.CharField(db_column="TABLE_NAME", max_length=30)
    column_name = models.CharField(db_column="COLUMN_NAME", max_length=30)

    class Meta:
        managed = True
        db_table = "MAPPING"


class Notice(models.Model):
    notice_type = models.ForeignKey(
        "NoticeType", models.DO_NOTHING, db_column="NOTICE_TYPE_ID", related_name="+"
    )
    activation = models.ForeignKey(
        Activation, models.CASCADE, db_column="ACTIVATION_ID", related_name="notices"
    )
    content = models.TextField(db_column="CONTENT", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "NOTICE"
        unique_together = (("notice_type", "activation"),)


class NoticeImage(models.Model):
    notice_image_id = models.AutoField(db_column="NOTICE_IMAGE_ID", primary_key=True)
    instance = models.ForeignKey(
        "instance.Instance",
        models.DO_NOTHING,
        db_column="INSTANCE_ID",
        related_name="+",
    )
    instance_resource = models.ForeignKey(
        IrEditnotice,
        models.DO_NOTHING,
        db_column="INSTANCE_RESOURCE_ID",
        related_name="+",
    )
    user = models.ForeignKey(
        "user.User", models.DO_NOTHING, db_column="USER_ID", related_name="+"
    )
    activation = models.ForeignKey(
        Activation, models.DO_NOTHING, db_column="ACTIVATION_ID", related_name="+"
    )
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")
    name = models.CharField(db_column="NAME", max_length=50)
    filename = models.CharField(db_column="FILENAME", max_length=50)

    class Meta:
        managed = True
        db_table = "NOTICE_IMAGE"


class NoticeLog(models.Model):
    notice_log_id = models.AutoField(db_column="NOTICE_LOG_ID", primary_key=True)
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")
    user_id = models.IntegerField(db_column="USER_ID")
    action = models.CharField(db_column="ACTION", max_length=500)
    data = models.TextField(db_column="DATA", blank=True, null=True)
    id1 = models.IntegerField(db_column="ID1")
    field1 = models.CharField(db_column="FIELD1", max_length=30)
    id2 = models.IntegerField(db_column="ID2")
    field2 = models.CharField(db_column="FIELD2", max_length=30)

    class Meta:
        managed = True
        db_table = "NOTICE_LOG"


class NoticeType(MultilingualModel, models.Model):
    notice_type_id = models.AutoField(db_column="NOTICE_TYPE_ID", primary_key=True)
    circulation_type = models.ForeignKey(
        CirculationType,
        models.CASCADE,
        db_column="CIRCULATION_TYPE_ID",
        related_name="+",
    )
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "NOTICE_TYPE"


class NoticeTypeT(models.Model):
    notice_type = models.ForeignKey(
        NoticeType, models.CASCADE, db_column="NOTICE_TYPE_ID", related_name="trans"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "NOTICE_TYPE_T"


class Page(MultilingualModel, models.Model):
    page_id = models.AutoField(db_column="PAGE_ID", primary_key=True)
    name = models.CharField(db_column="NAME", max_length=500, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )
    javascript = models.CharField(
        db_column="JAVASCRIPT", max_length=4000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "PAGE"


class PageT(models.Model):
    page = models.ForeignKey(
        Page, models.CASCADE, db_column="PAGE_ID", related_name="trans"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=500, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "PAGE_T"


class PageAnswerActivation(models.Model):
    page_answer_activation_id = models.AutoField(
        db_column="PAGE_ANSWER_ACTIVATION_ID", primary_key=True
    )
    form = models.ForeignKey(
        "instance.Form", models.CASCADE, db_column="FORM_ID", related_name="+"
    )
    chapter = models.ForeignKey(
        "Chapter", models.CASCADE, db_column="CHAPTER_ID", related_name="+"
    )
    question = models.ForeignKey(
        "Question", models.CASCADE, db_column="QUESTION_ID", related_name="+"
    )
    page = models.ForeignKey(
        "Page", models.CASCADE, db_column="PAGE_ID", related_name="+"
    )
    answer = models.CharField(db_column="ANSWER", max_length=4000)

    class Meta:
        managed = True
        db_table = "PAGE_ANSWER_ACTIVATION"


class PageForm(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    page = models.ForeignKey(
        Page, models.CASCADE, db_column="PAGE_ID", related_name="+"
    )
    form = models.ForeignKey(
        "instance.Form", models.CASCADE, db_column="FORM_ID", related_name="+"
    )
    page_form_mode = models.ForeignKey(
        "PageFormMode", models.CASCADE, db_column="PAGE_FORM_MODE_ID", related_name="+"
    )
    page_form_group = models.ForeignKey(
        "PageFormGroup",
        models.CASCADE,
        db_column="PAGE_FORM_GROUP_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    sort = models.IntegerField(db_column="SORT")

    class Meta:
        managed = True
        db_table = "PAGE_FORM"
        unique_together = (("page", "form"),)


class PageFormGroup(MultilingualModel, models.Model):
    page_form_group_id = models.AutoField(
        db_column="PAGE_FORM_GROUP_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "PAGE_FORM_GROUP"


class PageFormGroupAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    page = models.ForeignKey(
        PageForm, models.CASCADE, db_column="PAGE_ID", related_name="+"
    )
    form = models.ForeignKey(
        PageForm, models.CASCADE, db_column="FORM_ID", related_name="+"
    )
    group = models.ForeignKey(
        "user.Group", models.CASCADE, db_column="GROUP_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "PAGE_FORM_GROUP_ACL"
        unique_together = (("page", "form", "group", "instance_state"),)


class PageFormGroupT(models.Model):
    page_form_group = models.ForeignKey(
        PageFormGroup,
        models.CASCADE,
        db_column="PAGE_FORM_GROUP_ID",
        related_name="trans",
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "PAGE_FORM_GROUP_T"


class PageFormMode(models.Model):
    page_form_mode_id = models.AutoField(
        db_column="PAGE_FORM_MODE_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=50)

    class Meta:
        managed = True
        db_table = "PAGE_FORM_MODE"


class PageFormRoleAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    page = models.ForeignKey(
        PageForm, models.CASCADE, db_column="PAGE_ID", related_name="+"
    )
    form = models.ForeignKey(
        PageForm, models.CASCADE, db_column="FORM_ID", related_name="+"
    )
    role = models.ForeignKey(
        "user.Role", models.CASCADE, db_column="ROLE_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "PAGE_FORM_ROLE_ACL"
        unique_together = (("page", "form", "role", "instance_state"),)


class PageFormServiceAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    page = models.ForeignKey(
        PageForm, models.CASCADE, db_column="PAGE_ID", related_name="+"
    )
    form = models.ForeignKey(
        PageForm, models.CASCADE, db_column="FORM_ID", related_name="+"
    )
    service = models.ForeignKey(
        "user.Service", models.CASCADE, db_column="SERVICE_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "PAGE_FORM_SERVICE_ACL"
        unique_together = (("page", "form", "service", "instance_state"),)


class PageFormUserAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    page = models.ForeignKey(
        PageForm, models.CASCADE, db_column="PAGE_ID", related_name="+"
    )
    form = models.ForeignKey(
        PageForm, models.CASCADE, db_column="FORM_ID", related_name="+"
    )
    user = models.ForeignKey(
        "user.User", models.CASCADE, db_column="USER_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "PAGE_FORM_USER_ACL"
        unique_together = (("page", "form", "user", "instance_state"),)


class PortalSession(models.Model):
    portal_session_id = models.CharField(
        db_column="PORTAL_SESSION_ID", primary_key=True, max_length=256
    )
    portal_identifier = models.CharField(db_column="PORTAL_IDENTIFIER", max_length=256)
    last_active = models.DateTimeField(db_column="LAST_ACTIVE")

    class Meta:
        managed = True
        db_table = "PORTAL_SESSION"


class ProposalActivation(models.Model):
    proposal_activation_id = models.AutoField(
        db_column="PROPOSAL_ACTIVATION_ID", primary_key=True
    )
    instance = models.ForeignKey(
        "instance.Instance",
        models.CASCADE,
        db_column="INSTANCE_ID",
        related_name="+",
    )
    circulation_type = models.ForeignKey(
        CirculationType,
        models.DO_NOTHING,
        db_column="CIRCULATION_TYPE_ID",
        related_name="+",
    )
    service = models.ForeignKey(
        "user.Service", models.DO_NOTHING, db_column="SERVICE_ID", related_name="+"
    )
    circulation_state = models.ForeignKey(
        CirculationState,
        models.DO_NOTHING,
        db_column="CIRCULATION_STATE_ID",
        related_name="+",
    )
    deadline_date = models.DateTimeField(db_column="DEADLINE_DATE")
    reason = models.CharField(db_column="REASON", max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "PROPOSAL_ACTIVATION"


class PublicationType(models.Model):
    name = models.TextField(db_column="NAME")

    class Meta:
        managed = True
        db_table = "PUBLICATION_TYPE"


class PublicationEntry(models.Model):
    publication_entry_id = models.AutoField(
        db_column="PUBLICATION_ENTRY_ID", primary_key=True
    )
    instance = models.ForeignKey(
        "instance.Instance",
        models.CASCADE,
        db_column="INSTANCE_ID",
        related_name="publication_entries",
    )
    note = models.FloatField(db_column="NOTE", blank=True, null=True)
    publication_date = models.DateTimeField(db_column="PUBLICATION_DATE")
    publication_end_date = models.DateTimeField()
    is_published = models.PositiveSmallIntegerField(db_column="IS_PUBLISHED")
    text = models.TextField(db_column="TEXT", blank=True, null=True)
    type = models.ForeignKey(
        PublicationType,
        models.DO_NOTHING,
        db_column="PUBLICATION_TYPE_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    publication_views = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = "PUBLICATION_ENTRY"


class PublicationSetting(models.Model):
    publication_setting_id = models.AutoField(
        db_column="PUBLICATION_SETTING_ID", primary_key=True
    )
    key = models.CharField(db_column="KEY", max_length=64)
    value = models.CharField(db_column="VALUE", max_length=4000, blank=True, null=True)
    type = models.ForeignKey(
        PublicationType,
        models.DO_NOTHING,
        db_column="PUBLICATION_TYPE_ID",
        related_name="+",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "PUBLICATION_SETTING"


# This table is only used in kt. bern
class Publication(models.Model):
    instance = models.AutoField(
        "instance.Instance", db_column="INSTANCE_ID", primary_key=True
    )
    start = models.DateField(db_column="START_DATE")
    end = models.DateField(db_column="END_DATE")
    text = models.TextField(db_column="TEXT", null=True, blank=True)
    publication_anzeiger_1 = models.DateField(
        db_column="PUBLICATION_DATE_1_ANZEIGER", null=True, blank=True
    )
    publication_anzeiger_2 = models.DateField(
        db_column="PUBLICATION_DATE_2_ANZEIGER", null=True, blank=True
    )
    publication_amtsblatt = models.DateField(
        db_column="PUBLICATION_DATE_AMTSBLATT", null=True, blank=True
    )
    anzeiger = models.CharField(
        db_column="ANZEIGER", max_length=255, null=True, blank=True
    )

    class Meta:
        managed = True
        db_table = "PUBLICATION"


class Question(MultilingualModel, models.Model):
    question_id = models.AutoField(db_column="QUESTION_ID", primary_key=True)
    question_type = models.ForeignKey(
        "QuestionType", models.CASCADE, db_column="QUESTION_TYPE_ID", related_name="+"
    )
    mapping = models.ForeignKey(
        Mapping,
        models.CASCADE,
        db_column="MAPPING_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    answer_query = models.ForeignKey(
        AnswerQuery,
        models.CASCADE,
        db_column="ANSWER_QUERY_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    name = models.CharField(db_column="NAME", max_length=500, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )
    javascript = models.CharField(
        db_column="JAVASCRIPT", max_length=4000, blank=True, null=True
    )
    regex = models.CharField(db_column="REGEX", max_length=1000, blank=True, null=True)
    default_answer = models.CharField(
        db_column="DEFAULT_ANSWER", max_length=4000, blank=True, null=True
    )
    # Field renamed because it was a Python reserved word.
    class_field = models.CharField(
        db_column="CLASS", max_length=25, blank=True, null=True
    )
    validation = models.CharField(
        db_column="VALIDATION", max_length=50, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "QUESTION"


class QuestionChapter(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    question = models.ForeignKey(
        Question, models.CASCADE, db_column="QUESTION_ID", related_name="+"
    )
    chapter = models.ForeignKey(
        Chapter, models.CASCADE, db_column="CHAPTER_ID", related_name="+"
    )
    required = models.PositiveSmallIntegerField(db_column="REQUIRED")
    item = models.IntegerField(db_column="ITEM")
    sort = models.IntegerField(db_column="SORT")

    class Meta:
        managed = True
        db_table = "QUESTION_CHAPTER"
        unique_together = (("question", "chapter"),)


class QuestionChapterGroupAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    question = models.ForeignKey(
        Question, models.CASCADE, db_column="QUESTION_ID", related_name="+"
    )
    chapter = models.ForeignKey(
        Chapter, models.CASCADE, db_column="CHAPTER_ID", related_name="+"
    )
    group = models.ForeignKey(
        "user.Group", models.CASCADE, db_column="GROUP_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "QUESTION_CHAPTER_GROUP_ACL"
        unique_together = (("question", "chapter", "group", "instance_state"),)


class QuestionChapterRoleAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    question = models.ForeignKey(
        Question, models.CASCADE, db_column="QUESTION_ID", related_name="+"
    )
    chapter = models.ForeignKey(
        Chapter, models.CASCADE, db_column="CHAPTER_ID", related_name="+"
    )
    role = models.ForeignKey(
        "user.Role", models.CASCADE, db_column="ROLE_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "QUESTION_CHAPTER_ROLE_ACL"
        unique_together = (("question", "chapter", "role", "instance_state"),)


class QuestionChapterServiceAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    question = models.ForeignKey(
        Question, models.CASCADE, db_column="QUESTION_ID", related_name="+"
    )
    chapter = models.ForeignKey(
        Chapter, models.CASCADE, db_column="CHAPTER_ID", related_name="+"
    )
    service = models.ForeignKey(
        "user.Service", models.CASCADE, db_column="SERVICE_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "QUESTION_CHAPTER_SERVICE_ACL"
        unique_together = (("question", "chapter", "service", "instance_state"),)


class QuestionChapterUserAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    question = models.ForeignKey(
        Question, models.CASCADE, db_column="QUESTION_ID", related_name="+"
    )
    chapter = models.ForeignKey(
        Chapter, models.CASCADE, db_column="CHAPTER_ID", related_name="+"
    )
    user = models.ForeignKey(
        "user.User", models.CASCADE, db_column="USER_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "QUESTION_CHAPTER_USER_ACL"
        unique_together = (("question", "chapter", "user", "instance_state"),)


class QuestionT(models.Model):
    question = models.ForeignKey(
        Question, models.CASCADE, db_column="QUESTION_ID", related_name="trans"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=500, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )
    default_answer = models.CharField(
        db_column="DEFAULT_ANSWER", max_length=4000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "QUESTION_T"


class QuestionType(models.Model):
    question_type_id = models.AutoField(db_column="QUESTION_TYPE_ID", primary_key=True)
    name = models.CharField(db_column="NAME", max_length=20)
    sort = models.IntegerField(db_column="SORT", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "QUESTION_TYPE"


class RApiListInstanceState(models.Model):
    resource = models.ForeignKey(
        "Resource", models.CASCADE, db_column="RESOURCE_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "R_API_LIST_INSTANCE_STATE"
        unique_together = (("resource", "instance_state"),)


class RApiListCirculationState(models.Model):
    resource = models.ForeignKey(
        "Resource", models.CASCADE, db_column="RESOURCE_ID", related_name="+"
    )
    circulation_state = models.ForeignKey(
        "CirculationState",
        models.CASCADE,
        db_column="CIRCULATION_STATE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "R_API_LIST_CIRCULATION_STATE"
        unique_together = (("resource", "circulation_state"),)


class RApiListCirculationType(models.Model):
    resource = models.ForeignKey(
        "Resource", models.CASCADE, db_column="RESOURCE_ID", related_name="+"
    )
    circulation_type = models.ForeignKey(
        "CirculationType",
        models.CASCADE,
        db_column="CIRCULATION_TYPE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "R_API_LIST_CIRCULATION_TYPE"
        unique_together = (("resource", "circulation_type"),)


class RFormlist(models.Model):
    resource = models.OneToOneField(
        "Resource",
        models.CASCADE,
        db_column="RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    form = models.ForeignKey(
        "instance.Form", models.CASCADE, db_column="FORM_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "R_FORMLIST"


class RGroupAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    resource = models.ForeignKey(
        "Resource", models.CASCADE, db_column="RESOURCE_ID", related_name="+"
    )
    group = models.ForeignKey(
        "user.Group", models.CASCADE, db_column="GROUP_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "R_GROUP_ACL"
        unique_together = (("resource", "group"),)


class RList(models.Model):
    resource = models.OneToOneField(
        "Resource",
        models.CASCADE,
        db_column="RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    query = models.CharField(db_column="QUERY", max_length=4000)

    class Meta:
        managed = True
        db_table = "R_LIST"


class RListColumn(MultilingualModel, models.Model):
    r_list_column_id = models.AutoField(db_column="R_LIST_COLUMN_ID", primary_key=True)
    resource = models.ForeignKey(
        RList, models.CASCADE, db_column="RESOURCE_ID", related_name="+"
    )
    column_name = models.CharField(db_column="COLUMN_NAME", max_length=30)
    alias = models.CharField(db_column="ALIAS", max_length=50, blank=True, null=True)
    sort = models.IntegerField(db_column="SORT")

    def __str__(self):
        return self.get_trans_attr("alias")

    class Meta:
        managed = True
        db_table = "R_LIST_COLUMN"


class RListColumnT(models.Model):
    r_list_column = models.ForeignKey(
        RListColumn, models.CASCADE, db_column="R_LIST_COLUMN_ID", related_name="trans"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    alias = models.CharField(db_column="ALIAS", max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "R_LIST_COLUMN_T"


class RPage(models.Model):
    resource = models.OneToOneField(
        "Resource",
        models.CASCADE,
        db_column="RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    pdf_class = models.CharField(
        db_column="PDF_CLASS", max_length=500, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "R_PAGE"


class RRoleAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    resource = models.ForeignKey(
        "Resource", models.CASCADE, db_column="RESOURCE_ID", related_name="role_acls"
    )
    role = models.ForeignKey(
        "user.Role", models.CASCADE, db_column="ROLE_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "R_ROLE_ACL"
        unique_together = (("resource", "role"),)


class RSearch(models.Model):
    resource = models.OneToOneField(
        "Resource",
        models.CASCADE,
        db_column="RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    result_template = models.CharField(
        db_column="RESULT_TEMPLATE", max_length=500, blank=True, null=True
    )
    query = models.TextField(db_column="QUERY")
    pdf_class = models.CharField(
        db_column="PDF_CLASS", max_length=500, blank=True, null=True
    )
    preserve_result = models.PositiveSmallIntegerField(
        db_column="PRESERVE_RESULT", default=0
    )

    class Meta:
        managed = True
        db_table = "R_SEARCH"


class RSearchColumn(MultilingualModel, models.Model):
    r_search_column_id = models.AutoField(
        db_column="R_SEARCH_COLUMN_ID", primary_key=True
    )
    resource = models.ForeignKey(
        RSearch, models.CASCADE, db_column="RESOURCE_ID", related_name="+"
    )
    column_name = models.CharField(db_column="COLUMN_NAME", max_length=30)
    alias = models.CharField(db_column="ALIAS", max_length=30, blank=True, null=True)
    sort = models.IntegerField(db_column="SORT")

    def __str__(self):
        return self.get_trans_attr("alias")

    class Meta:
        managed = True
        db_table = "R_SEARCH_COLUMN"


class RSearchColumnT(models.Model):
    r_search_column = models.ForeignKey(
        RSearchColumn,
        models.CASCADE,
        db_column="R_SEARCH_COLUMN_ID",
        related_name="trans",
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    alias = models.CharField(db_column="ALIAS", max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "R_SEARCH_COLUMN_T"


class RSearchFilter(MultilingualModel, models.Model):
    r_search_filter_id = models.AutoField(
        db_column="R_SEARCH_FILTER_ID", primary_key=True
    )
    resource = models.ForeignKey(
        RSearch, models.CASCADE, db_column="RESOURCE_ID", related_name="+"
    )
    question = models.ForeignKey(
        Question,
        models.CASCADE,
        db_column="QUESTION_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    field_name = models.CharField(db_column="FIELD_NAME", max_length=50)
    class_field = models.CharField(
        db_column="CLASS", max_length=200, blank=True, null=True
    )  # Field renamed because it was a Python reserved word.
    label = models.CharField(db_column="LABEL", max_length=1000, blank=True, null=True)
    query = models.CharField(db_column="QUERY", max_length=4000)
    wildcard = models.PositiveSmallIntegerField(db_column="WILDCARD")
    # Field renamed because it was a Python reserved word.
    class_field = models.CharField(
        db_column="CLASS", max_length=25, blank=True, null=True
    )

    def __str__(self):
        return self.get_trans_attr("label")

    class Meta:
        managed = True
        db_table = "R_SEARCH_FILTER"


class RSearchFilterT(models.Model):
    r_search_filter = models.ForeignKey(
        RSearchFilter,
        models.CASCADE,
        db_column="R_SEARCH_FILTER_ID",
        related_name="trans",
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    label = models.CharField(db_column="LABEL", max_length=1000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "R_SEARCH_FILTER_T"


class RServiceAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    resource = models.ForeignKey(
        "Resource", models.CASCADE, db_column="RESOURCE_ID", related_name="+"
    )
    service = models.ForeignKey(
        "user.Service", models.CASCADE, db_column="SERVICE_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "R_SERVICE_ACL"
        unique_together = (("resource", "service"),)


class RSimpleList(models.Model):
    resource_id = models.AutoField(db_column="RESOURCE_ID", primary_key=True)
    instance_states = models.CharField(db_column="INSTANCE_STATES", max_length=400)

    class Meta:
        managed = True
        db_table = "R_SIMPLE_LIST"


class RCalumaList(models.Model):
    resource_id = models.AutoField(db_column="RESOURCE_ID", primary_key=True)
    instance_states = models.CharField(db_column="INSTANCE_STATES", max_length=400)

    class Meta:
        managed = True
        db_table = "R_CALUMA_LIST"


class REmberList(models.Model):
    resource_id = models.AutoField(db_column="RESOURCE_ID", primary_key=True)
    instance_states = models.CharField(db_column="INSTANCE_STATES", max_length=400)

    class Meta:
        managed = True
        db_table = "R_EMBER_LIST"


class RUserAcl(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    resource = models.ForeignKey(
        "Resource", models.CASCADE, db_column="RESOURCE_ID", related_name="+"
    )
    user = models.ForeignKey(
        "user.User", models.CASCADE, db_column="USER_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "R_USER_ACL"
        unique_together = (("resource", "user"),)


class Resource(MultilingualModel, models.Model):
    resource_id = models.AutoField(db_column="RESOURCE_ID", primary_key=True)
    available_resource = models.ForeignKey(
        AvailableResource,
        models.CASCADE,
        db_column="AVAILABLE_RESOURCE_ID",
        related_name="+",
    )
    name = models.CharField(db_column="NAME", max_length=100, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )
    template = models.CharField(
        db_column="TEMPLATE", max_length=500, blank=True, null=True
    )
    # Field renamed because it was a Python reserved word.
    class_field = models.CharField(
        db_column="CLASS", max_length=25, blank=True, null=True
    )
    hidden = models.PositiveSmallIntegerField(db_column="HIDDEN")
    sort = models.IntegerField(db_column="SORT")

    class Meta:
        managed = True
        db_table = "RESOURCE"
        ordering = ["sort"]


class ResourceT(models.Model):
    resource = models.ForeignKey(
        Resource, models.CASCADE, db_column="RESOURCE_ID", related_name="trans"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=100, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "RESOURCE_T"


class Sanction(models.Model):
    sanction_id = models.AutoField(db_column="SANCTION_ID", primary_key=True)
    instance = models.ForeignKey(
        "instance.Instance",
        models.CASCADE,
        db_column="INSTANCE_ID",
        related_name="sanctions",
    )
    service = models.ForeignKey(
        "user.Service", models.DO_NOTHING, db_column="SERVICE_ID", related_name="+"
    )
    user = models.ForeignKey(
        "user.User", models.DO_NOTHING, db_column="USER_ID", related_name="+"
    )
    text = models.CharField(db_column="TEXT", max_length=4000)
    start_date = models.DateTimeField(db_column="START_DATE")
    deadline_date = models.DateTimeField(
        db_column="DEADLINE_DATE", blank=True, null=True
    )
    end_date = models.DateTimeField(db_column="END_DATE", blank=True, null=True)
    control_instance = models.ForeignKey(
        "user.Service",
        models.DO_NOTHING,
        db_column="CONTROL_INSTANCE_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    notice = models.CharField(db_column="NOTICE", max_length=500, blank=True, null=True)
    is_finished = models.PositiveSmallIntegerField(db_column="IS_FINISHED")
    finished_by_user = models.ForeignKey(
        "user.User",
        models.DO_NOTHING,
        db_column="FINISHED_BY_USER_ID",
        related_name="+",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "SANCTION"


class ServiceAnswerActivation(models.Model):
    service_answer_activation_id = models.AutoField(
        db_column="SERVICE_ANSWER_ACTIVATION_ID", primary_key=True
    )
    form = models.ForeignKey(
        "instance.Form", models.DO_NOTHING, db_column="FORM_ID", related_name="+"
    )
    chapter = models.ForeignKey(
        Chapter, models.DO_NOTHING, db_column="CHAPTER_ID", related_name="+"
    )
    question = models.ForeignKey(
        Question, models.DO_NOTHING, db_column="QUESTION_ID", related_name="+"
    )
    service = models.ForeignKey(
        "user.Service", models.DO_NOTHING, db_column="SERVICE_ID", related_name="+"
    )
    answer = models.CharField(db_column="ANSWER", max_length=4000)

    class Meta:
        managed = True
        db_table = "SERVICE_ANSWER_ACTIVATION"


class InstanceService(models.Model):
    instance = models.ForeignKey(
        "instance.Instance",
        models.CASCADE,
        db_column="INSTANCE_ID",
        related_name="instance_services",
    )
    service = models.ForeignKey(
        "user.Service",
        models.DO_NOTHING,
        db_column="SERVICE_ID",
        related_name="instance_services",
    )
    active = models.PositiveSmallIntegerField(db_column="ACTIVE", default=0)
    activation_date = models.DateTimeField(
        db_column="ACTIVATION_DATE", blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "INSTANCE_SERVICE"


class InstanceParent(models.Model):
    instance = models.AutoField(
        "instance.Instance", db_column="INSTANCE_ID", primary_key=True
    )
    parent = models.ForeignKey(
        "instance.Instance",
        models.DO_NOTHING,
        db_column="PARENT_INSTANCE_ID",
        related_name="+",
    )
    user = models.ForeignKey(
        "user.User", models.DO_NOTHING, db_column="USER_ID", related_name="+"
    )
    service = models.ForeignKey(
        "user.Service",
        models.DO_NOTHING,
        db_column="SERVICE_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    created = models.DateTimeField(db_column="CREATED")

    class Meta:
        managed = True
        db_table = "INSTANCE_PARENT"


class BillingV2Entry(models.Model):
    TAX_MODE_CHOICES = (
        ("inclusive", "Incl 7.7%"),
        ("exclusive", "Excl 7.7%"),
        ("exempt", "Tax exempt"),
    )

    CALCULATION_CHOICES = (
        ("flat", "Flat rate"),
        ("percentage", "Percentage"),
        ("hourly", "Hourly"),
    )

    MUNICIPAL = "municipal"
    CANTONAL = "cantonal"
    ORGANIZATION_CHOICES = ((MUNICIPAL, "Municipal"), (CANTONAL, "Cantonal"))

    DECIMAL_FORMAT = {"max_digits": 10, "decimal_places": 2, "null": True}

    # Structural: Which instance is the item billed to?
    instance = models.ForeignKey(
        "instance.Instance",
        models.CASCADE,
        db_column="INSTANCE_ID",
        related_name="+",
    )

    # Organisation: Who charged the item?
    group = models.ForeignKey("user.Group", models.DO_NOTHING, related_name="+")
    user = models.ForeignKey("user.User", models.DO_NOTHING, related_name="+")

    # Billing text
    text = models.TextField()
    date_added = models.DateField()

    # Tax mode = calculation model for tax
    tax_mode = models.CharField(choices=TAX_MODE_CHOICES, max_length=20)

    # Calculation mode
    calculation = models.CharField(choices=CALCULATION_CHOICES, max_length=20)

    # Tax rate (percentage)
    tax_rate = models.DecimalField(**DECIMAL_FORMAT)

    # Calculation mode: hourly rate
    hours = models.DecimalField(**DECIMAL_FORMAT)
    hourly_rate = models.DecimalField(**DECIMAL_FORMAT)

    # Calculation mode: percentage of total cost
    percentage = models.DecimalField(**DECIMAL_FORMAT)
    total_cost = models.DecimalField(**DECIMAL_FORMAT)

    # Final rate (may be entered directly in "flat" mode, otherwise it's
    # calculated. We store it for easier handling in the output however.
    final_rate = models.DecimalField(**DECIMAL_FORMAT)

    # Organization: either municipal or cantonal but can be NULL
    # Used to distinguish which oranization collects part of the bill
    organization = models.CharField(
        choices=ORGANIZATION_CHOICES, max_length=20, null=True
    )

    class Meta:
        managed = True
        db_table = "BILLING_V2_ENTRY"


class DocxDecision(models.Model):
    instance = models.OneToOneField(
        "instance.Instance",
        on_delete=models.CASCADE,
        db_column="INSTANCE_ID",
        primary_key=True,
        related_name="decision",
    )
    decision = models.CharField(db_column="DECISION", max_length=30)
    decision_type = models.CharField(
        db_column="DECISION_TYPE", max_length=90, blank=True, null=True
    )
    decision_date = models.DateField(db_column="DECISION_DATE")

    class Meta:
        managed = True
        db_table = "DOCX_DECISION"


class Municipality(models.Model):
    bfs_nr = models.IntegerField(db_column="BFS_NR", primary_key=True)
    name = models.CharField(db_column="NAME", max_length=100)
    district_nr = models.PositiveSmallIntegerField(db_column="DISTRICT_NR")

    class Meta:
        managed = True
        db_table = "MUNICIPALITY"


class WorkflowAction(models.Model):
    action = models.OneToOneField(
        Action,
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )
    workflow_item = models.ForeignKey(
        "WorkflowItem", models.CASCADE, db_column="WORKFLOW_ITEM_ID", related_name="+"
    )
    multi_value = models.PositiveSmallIntegerField(db_column="MULTI_VALUE")

    class Meta:
        managed = True
        db_table = "WORKFLOW_ACTION"


class WorkflowEntry(models.Model):
    workflow_entry_id = models.AutoField(
        db_column="WORKFLOW_ENTRY_ID", primary_key=True
    )
    workflow_date = models.DateTimeField(db_column="WORKFLOW_DATE")
    instance = models.ForeignKey(
        "instance.Instance", models.CASCADE, db_column="INSTANCE_ID"
    )
    workflow_item = models.ForeignKey(
        "WorkflowItem",
        models.DO_NOTHING,
        db_column="WORKFLOW_ITEM_ID",
        related_name="+",
    )
    group = models.IntegerField(db_column="GROUP")

    class Meta:
        managed = True
        db_table = "WORKFLOW_ENTRY"


class WorkflowItem(models.Model):
    workflow_item_id = models.AutoField(db_column="WORKFLOW_ITEM_ID", primary_key=True)
    position = models.IntegerField(db_column="POSITION")
    name = models.CharField(db_column="NAME", max_length=255)
    automatical = models.PositiveSmallIntegerField(db_column="AUTOMATICAL")
    different_color = models.PositiveSmallIntegerField(db_column="DIFFERENT_COLOR")
    is_workflow = models.PositiveSmallIntegerField(db_column="IS_WORKFLOW")
    is_building_authority = models.PositiveSmallIntegerField(
        db_column="IS_BUILDING_AUTHORITY"
    )
    workflow_section = models.ForeignKey(
        "WorkflowSection",
        models.CASCADE,
        db_column="WORKFLOW_SECTION_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    caluma_task = models.ForeignKey(
        "caluma_workflow.Task",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    caluma_question = models.ForeignKey(
        "caluma_form.Question",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "WORKFLOW_ITEM"


class WorkflowRole(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    workflow_item = models.ForeignKey(
        WorkflowItem, models.CASCADE, db_column="WORKFLOW_ITEM_ID", related_name="+"
    )
    role = models.ForeignKey(
        "user.Role", models.CASCADE, db_column="ROLE_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "WORKFLOW_ROLE"
        unique_together = (("role", "workflow_item"),)


class WorkflowSection(models.Model):
    workflow_section_id = models.AutoField(
        db_column="WORKFLOW_SECTION_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=60)
    sort = models.IntegerField(db_column="SORT", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "WORKFLOW_SECTION"


class AttachmentExtension(models.Model):
    attachment_extension_id = models.AutoField(
        db_column="ATTACHMENT_EXTENSION_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=10)

    class Meta:
        managed = True
        db_table = "ATTACHMENT_EXTENSION"


class AttachmentExtensionRole(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    attachment_extension = models.ForeignKey(
        AttachmentExtension,
        models.CASCADE,
        db_column="ATTACHMENT_EXTENSION_ID",
        related_name="+",
    )
    role = models.ForeignKey(
        "user.Role", models.CASCADE, db_column="ROLE_ID", related_name="+"
    )
    mode = models.CharField(db_column="MODE", max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "ATTACHMENT_EXTENSION_ROLE"
        unique_together = (("attachment_extension", "role"),)


class AttachmentExtensionService(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    attachment_extension = models.ForeignKey(
        AttachmentExtension,
        models.CASCADE,
        db_column="ATTACHMENT_EXTENSION_ID",
        related_name="+",
    )
    service = models.ForeignKey(
        "user.Service", models.CASCADE, db_column="SERVICE_ID", related_name="+"
    )
    mode = models.CharField(db_column="MODE", max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "ATTACHMENT_EXTENSION_SERVICE"
        unique_together = (("attachment_extension", "service"),)


class Archive(models.Model):
    archive_id = models.AutoField(db_column="ARCHIVE_ID", primary_key=True)
    identifier = models.TextField(db_column="IDENTIFIER", unique=True)
    path = models.TextField(db_column="PATH", unique=True)
    first_download = models.DateTimeField(
        db_column="FIRST_DOWNLOAD", null=True, blank=True
    )
    created = models.DateTimeField(db_column="CREATED")
    instance = models.ForeignKey(
        "instance.Instance",
        models.DO_NOTHING,
        db_column="INSTANCE_ID",
        related_name="+",
    )
    attachment_section = models.ForeignKey(
        "document.AttachmentSection",
        models.DO_NOTHING,
        db_column="ATTACHMENT_SECTION_ID",
        related_name="+",
    )
    workflow_item = models.ForeignKey(
        "WorkflowItem",
        models.DO_NOTHING,
        db_column="WORKFLOW_ITEM_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "ARCHIVE"


class HistoryActionConfig(models.Model):
    HISTORY_TYPE_NOTIFICATION = "notification"
    HISTORY_TYPE_STATUS = "status-change"
    HISTORY_TYPES = (HISTORY_TYPE_NOTIFICATION, HISTORY_TYPE_STATUS)
    HISTORY_TYPES_TUPLE = ((t, t) for t in HISTORY_TYPES)

    action = models.OneToOneField(
        "Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )
    title = models.TextField(db_column="TITLE", blank=True, null=True)
    body = models.TextField(db_column="BODY", blank=True, null=True)
    history_type = models.CharField(
        db_column="HISTORY_TYPE", max_length=20, choices=HISTORY_TYPES_TUPLE
    )

    def __str__(self):
        return self.get_trans_attr("title")

    class Meta:
        managed = True
        db_table = "HISTORY_ACTION_CONFIG"


class HistoryActionConfigT(models.Model):
    action = models.ForeignKey(
        HistoryActionConfig, models.CASCADE, db_column="ACTION_ID", related_name="trans"
    )

    title = models.TextField(db_column="TITLE")
    body = models.TextField(db_column="BODY", blank=True, null=True)
    language = models.CharField(db_column="LANGUAGE", max_length=2)

    class Meta:
        managed = True
        db_table = "HISTORY_ACTION_CONFIG_T"


class ActionWorkitem(models.Model):
    PROCESS_TYPE_COMPLETE = "complete"
    PROCESS_TYPE_SKIP = "skip"
    PROCESS_TYPE_CANCEL = "cancel"

    PROCESS_TYPES = tuple(
        (t, t) for t in (PROCESS_TYPE_COMPLETE, PROCESS_TYPE_SKIP, PROCESS_TYPE_CANCEL)
    )

    action = models.OneToOneField(
        "Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )
    tasks = ArrayField(
        models.CharField(max_length=255), db_column="TASKS", default=list
    )
    process_type = models.CharField(
        db_column="PROCESS_TYPE", max_length=10, choices=PROCESS_TYPES
    )
    process_all = models.BooleanField(db_column="PROCESS_ALL", default=False)
    is_activation = models.BooleanField(db_column="IS_ACTIVATION", default=False)
    fail_on_empty = models.BooleanField(db_column="FAIL_ON_EMPTY", default=False)

    class Meta:
        managed = True
        db_table = "ACTION_WORKITEM"


class ActionCase(models.Model):
    PROCESS_TYPE_CANCEL = "cancel"
    PROCESS_TYPE_SUSPEND = "suspend"
    PROCESS_TYPE_RESUME = "resume"

    PROCESS_TYPES = tuple(
        (t, t) for t in (PROCESS_TYPE_CANCEL, PROCESS_TYPE_SUSPEND, PROCESS_TYPE_RESUME)
    )

    action = models.OneToOneField(
        "Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )
    process_type = models.CharField(
        db_column="PROCESS_TYPE", max_length=10, choices=PROCESS_TYPES
    )

    class Meta:
        managed = True
        db_table = "ACTION_CASE"


class IrTaskform(models.Model):
    instance_resource = models.OneToOneField(
        InstanceResource,
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    task = models.ForeignKey(
        "caluma_workflow.Task",
        on_delete=models.CASCADE,
        db_column="TASK",
    )

    class Meta:
        managed = True
        db_table = "IR_TASKFORM"
