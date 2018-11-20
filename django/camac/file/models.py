from django.db import models


class AFilecheckcontent(models.Model):
    action = models.OneToOneField(
        "core.Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )
    page_form_group = models.ForeignKey(
        "core.PageFormGroup",
        models.CASCADE,
        db_column="PAGE_FORM_GROUP_ID",
        related_name="+",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "A_FILECHECKCONTENT"


class AFilesavepdf(models.Model):
    action = models.OneToOneField(
        "core.Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )
    file_content_category = models.ForeignKey(
        "FileContentCategory",
        models.CASCADE,
        db_column="FILE_CONTENT_CATEGORY_ID",
        related_name="+",
    )
    file_content = models.ForeignKey(
        "FileContent", models.CASCADE, db_column="FILE_CONTENT_ID", related_name="+"
    )
    page_form_group = models.ForeignKey(
        "core.PageFormGroup",
        models.CASCADE,
        db_column="PAGE_FORM_GROUP_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    file_name = models.CharField(
        db_column="FILE_NAME", max_length=50, blank=True, null=True
    )
    show_all_page_form_mode = models.PositiveSmallIntegerField(
        db_column="SHOW_ALL_PAGE_FORM_MODE"
    )
    template = models.CharField(db_column="TEMPLATE", max_length=500)
    pdf_class = models.CharField(db_column="PDF_CLASS", max_length=500)
    separate_pages = models.PositiveSmallIntegerField(db_column="SEPARATE_PAGES")
    new_version = models.NullBooleanField(db_column="NEW_VERSION")

    class Meta:
        managed = True
        db_table = "A_FILESAVEPDF"


class AFilesavepdfContentpage(models.Model):
    a_filesavepdf_contentpage_id = models.AutoField(
        db_column="A_FILESAVEPDF_CONTENTPAGE_ID", primary_key=True
    )
    action = models.ForeignKey(
        AFilesavepdf, models.CASCADE, db_column="ACTION_ID", related_name="+"
    )
    file_content = models.ForeignKey(
        "FileContent", models.CASCADE, db_column="FILE_CONTENT_ID", related_name="+"
    )
    page = models.ForeignKey(
        "core.Page", models.CASCADE, db_column="PAGE_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "A_FILESAVEPDF_CONTENTPAGE"


class AFilesavepdfT(models.Model):
    action = models.ForeignKey(
        AFilesavepdf, models.CASCADE, db_column="ACTION_ID", related_name="+"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    file_name = models.CharField(
        db_column="FILE_NAME", max_length=50, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "A_FILESAVEPDF_T"
        unique_together = (("action", "language"),)


class AFilesdownload(models.Model):
    action = models.OneToOneField(
        "core.Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "A_FILESDOWNLOAD"


class AFilesdownloadContent(models.Model):
    a_filesdownload_content_id = models.AutoField(
        db_column="A_FILESDOWNLOAD_CONTENT_ID", primary_key=True
    )
    file_content = models.ForeignKey(
        "FileContent", models.CASCADE, db_column="FILE_CONTENT_ID", related_name="+"
    )
    action = models.ForeignKey(
        AFilesdownload, models.CASCADE, db_column="ACTION_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "A_FILESDOWNLOAD_CONTENT"


class AFiletransition(models.Model):
    action_id = models.AutoField(db_column="ACTION_ID", primary_key=True)
    current_state = models.ForeignKey(
        "FileComplementState",
        models.CASCADE,
        db_column="CURRENT_STATE_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    next_state = models.ForeignKey(
        "FileComplementState",
        models.CASCADE,
        db_column="NEXT_STATE_ID",
        related_name="+",
    )
    a_filetransition_date = models.ForeignKey(
        "AFiletransitionDate",
        models.CASCADE,
        db_column="A_FILETRANSITION_DATE_ID",
        related_name="+",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "A_FILETRANSITION"


class AFiletransitionDate(models.Model):
    a_filetransition_date_id = models.AutoField(
        db_column="A_FILETRANSITION_DATE_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=30)

    class Meta:
        managed = True
        db_table = "A_FILETRANSITION_DATE"


class File(models.Model):
    file_id = models.AutoField(db_column="FILE_ID", primary_key=True)
    instance = models.ForeignKey(
        "instance.Instance",
        models.DO_NOTHING,
        db_column="INSTANCE_ID",
        related_name="+",
    )
    user = models.ForeignKey(
        "user.User", models.DO_NOTHING, db_column="USER_ID", related_name="+"
    )
    group = models.ForeignKey(
        "user.Group", models.DO_NOTHING, db_column="GROUP_ID", related_name="+"
    )
    instance_state = models.ForeignKey(
        "instance.InstanceState",
        models.DO_NOTHING,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )
    file_format = models.ForeignKey(
        "FileFormat",
        models.DO_NOTHING,
        db_column="FILE_FORMAT_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    file_mime_type = models.IntegerField(
        db_column="FILE_MIME_TYPE_ID", blank=True, null=True, db_index=True
    )

    file_complement_req = models.ForeignKey(
        "FileComplementReq",
        models.DO_NOTHING,
        db_column="FILE_COMPLEMENT_REQ_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    name = models.CharField(db_column="NAME", max_length=250)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    file_date = models.DateTimeField(db_column="FILE_DATE", blank=True, null=True)
    size = models.IntegerField(db_column="SIZE", blank=True, null=True)
    is_physical_document = models.PositiveSmallIntegerField(
        db_column="IS_PHYSICAL_DOCUMENT"
    )
    filename = models.CharField(
        db_column="FILENAME", max_length=50, blank=True, null=True
    )
    last_version_file = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        db_column="LAST_VERSION_FILE_ID",
        related_name="+",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = "FILE"


class FileComplementReq(models.Model):
    file_complement_req_id = models.AutoField(
        db_column="FILE_COMPLEMENT_REQ_ID", primary_key=True
    )
    file_complement_state = models.ForeignKey(
        "FileComplementState",
        models.DO_NOTHING,
        db_column="FILE_COMPLEMENT_STATE_ID",
        related_name="+",
    )
    instance = models.ForeignKey(
        "instance.Instance",
        models.DO_NOTHING,
        db_column="INSTANCE_ID",
        related_name="+",
    )
    user = models.ForeignKey(
        "user.User", models.DO_NOTHING, db_column="USER_ID", related_name="+"
    )
    group = models.ForeignKey(
        "user.Group", models.DO_NOTHING, db_column="GROUP_ID", related_name="+"
    )
    complement_date = models.DateTimeField(db_column="COMPLEMENT_DATE")
    confirm_date = models.DateTimeField(db_column="CONFIRM_DATE", blank=True, null=True)
    expire_date = models.DateTimeField(db_column="EXPIRE_DATE", blank=True, null=True)
    response_date = models.DateTimeField(
        db_column="RESPONSE_DATE", blank=True, null=True
    )
    content = models.TextField(db_column="CONTENT")
    answer_note = models.TextField(db_column="ANSWER_NOTE", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "FILE_COMPLEMENT_REQ"


class FileComplementReqLog(models.Model):
    file_complement_req_log_id = models.AutoField(
        db_column="FILE_COMPLEMENT_REQ_LOG_ID", primary_key=True
    )
    id = models.IntegerField(db_column="ID")
    user_id = models.IntegerField(db_column="USER_ID")
    action = models.CharField(db_column="ACTION", max_length=500)
    data = models.TextField(db_column="DATA")
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")

    class Meta:
        managed = True
        db_table = "FILE_COMPLEMENT_REQ_LOG"


class FileComplementState(models.Model):
    file_complement_state_id = models.AutoField(
        db_column="FILE_COMPLEMENT_STATE_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "FILE_COMPLEMENT_STATE"


class FileComplementStateT(models.Model):
    file_complement_state = models.ForeignKey(
        FileComplementState,
        models.CASCADE,
        db_column="FILE_COMPLEMENT_STATE_ID",
        related_name="+",
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "FILE_COMPLEMENT_STATE_T"
        unique_together = (("file_complement_state", "language"),)


class FileContent(models.Model):
    file_content_id = models.AutoField(db_column="FILE_CONTENT_ID", primary_key=True)
    file_content_category = models.ForeignKey(
        "FileContentCategory",
        models.DO_NOTHING,
        db_column="FILE_CONTENT_CATEGORY_ID",
        related_name="+",
    )
    name = models.CharField(db_column="NAME", max_length=200, blank=True, null=True)
    url = models.CharField(db_column="URL", max_length=500, blank=True, null=True)
    sort = models.IntegerField(db_column="SORT")
    is_enabled = models.PositiveSmallIntegerField(db_column="IS_ENABLED")
    tooltip = models.CharField(
        db_column="TOOLTIP", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "FILE_CONTENT"


class FileContentCategory(models.Model):
    file_content_category_id = models.AutoField(
        db_column="FILE_CONTENT_CATEGORY_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=200, blank=True, null=True)
    sort = models.IntegerField(db_column="SORT")
    is_enabled = models.PositiveSmallIntegerField(db_column="IS_ENABLED")

    class Meta:
        managed = True
        db_table = "FILE_CONTENT_CATEGORY"


class FileContentCategoryT(models.Model):
    file_content_category = models.ForeignKey(
        FileContentCategory,
        models.CASCADE,
        db_column="FILE_CONTENT_CATEGORY_ID",
        related_name="+",
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=200, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "FILE_CONTENT_CATEGORY_T"
        unique_together = (("file_content_category", "language"),)


class FileContentFile(models.Model):
    file_content = models.ForeignKey(
        FileContent, models.DO_NOTHING, db_column="FILE_CONTENT_ID", related_name="+"
    )
    file = models.ForeignKey(
        File, models.DO_NOTHING, db_column="FILE_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "FILE_CONTENT_FILE"
        unique_together = (("file_content", "file"),)


class FileContentFileLog(models.Model):
    file_content_file_log_id = models.AutoField(
        db_column="FILE_CONTENT_FILE_LOG_ID", primary_key=True
    )
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")
    user_id = models.IntegerField(db_column="USER_ID")
    action = models.CharField(db_column="ACTION", max_length=500)
    data = models.TextField(db_column="DATA")
    id1 = models.IntegerField(db_column="ID1")
    field1 = models.CharField(db_column="FIELD1", max_length=30)
    id2 = models.IntegerField(db_column="ID2")
    field2 = models.CharField(db_column="FIELD2", max_length=30)

    class Meta:
        managed = True
        db_table = "FILE_CONTENT_FILE_LOG"


class FileContentForm(models.Model):
    file_content = models.ForeignKey(
        FileContent, models.CASCADE, db_column="FILE_CONTENT_ID", related_name="+"
    )
    form = models.ForeignKey(
        "instance.Form", models.CASCADE, db_column="FORM_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "FILE_CONTENT_FORM"
        unique_together = (("file_content", "form"),)


class FileContentMimeType(models.Model):
    file_content = models.ForeignKey(
        FileContent, models.CASCADE, db_column="FILE_CONTENT_ID", related_name="+"
    )
    file_mime_type = models.ForeignKey(
        "FileMimeType", models.CASCADE, db_column="FILE_MIME_TYPE_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "FILE_CONTENT_MIME_TYPE"
        unique_together = (("file_content", "file_mime_type"),)


class FileContentRequest(models.Model):
    file_content = models.ForeignKey(
        FileContent, models.DO_NOTHING, db_column="FILE_CONTENT_ID", related_name="+"
    )
    file_complement_req = models.ForeignKey(
        FileComplementReq,
        models.DO_NOTHING,
        db_column="FILE_COMPLEMENT_REQ_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "FILE_CONTENT_REQUEST"
        unique_together = (("file_content", "file_complement_req"),)


class FileContentRequestLog(models.Model):
    file_content_request_log_id = models.AutoField(
        db_column="FILE_CONTENT_REQUEST_LOG_ID", primary_key=True
    )
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")
    user_id = models.IntegerField(db_column="USER_ID")
    action = models.CharField(db_column="ACTION", max_length=500)
    data = models.TextField(db_column="DATA")
    id1 = models.IntegerField(db_column="ID1")
    field1 = models.CharField(db_column="FIELD1", max_length=30)
    id2 = models.IntegerField(db_column="ID2")
    field2 = models.CharField(db_column="FIELD2", max_length=30)

    class Meta:
        managed = True
        db_table = "FILE_CONTENT_REQUEST_LOG"


class FileContentRequired(models.Model):
    file_content_required_id = models.AutoField(
        db_column="FILE_CONTENT_REQUIRED_ID", primary_key=True
    )
    form = models.ForeignKey(
        "instance.Form", models.CASCADE, db_column="FORM_ID", related_name="+"
    )
    chapter = models.ForeignKey(
        "core.Chapter",
        models.CASCADE,
        db_column="CHAPTER_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    question = models.ForeignKey(
        "core.Question",
        models.CASCADE,
        db_column="QUESTION_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    file_content = models.ForeignKey(
        FileContent, models.CASCADE, db_column="FILE_CONTENT_ID", related_name="+"
    )
    answer = models.CharField(
        db_column="ANSWER", max_length=4000, blank=True, null=True
    )
    always_required = models.PositiveSmallIntegerField(db_column="ALWAYS_REQUIRED")

    class Meta:
        managed = True
        db_table = "FILE_CONTENT_REQUIRED"


class FileContentT(models.Model):
    file_content = models.ForeignKey(
        FileContent, models.CASCADE, db_column="FILE_CONTENT_ID", related_name="+"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=200, blank=True, null=True)
    url = models.CharField(db_column="URL", max_length=500, blank=True, null=True)
    tooltip = models.CharField(
        db_column="TOOLTIP", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "FILE_CONTENT_T"
        unique_together = (("file_content", "language"),)


class FileFormat(models.Model):
    file_format_id = models.AutoField(db_column="FILE_FORMAT_ID", primary_key=True)
    name = models.CharField(db_column="NAME", max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "FILE_FORMAT"


class FileFormatT(models.Model):
    file_format = models.ForeignKey(
        FileFormat, models.CASCADE, db_column="FILE_FORMAT_ID", related_name="+"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "FILE_FORMAT_T"
        unique_together = (("file_format", "language"),)


class FileLog(models.Model):
    file_log_id = models.AutoField(db_column="FILE_LOG_ID", primary_key=True)
    id = models.IntegerField(db_column="ID")
    user_id = models.IntegerField(db_column="USER_ID")
    action = models.CharField(db_column="ACTION", max_length=500)
    data = models.TextField(db_column="DATA")
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")

    class Meta:
        managed = True
        db_table = "FILE_LOG"


class FileMimeType(models.Model):
    file_mime_type_id = models.AutoField(
        db_column="FILE_MIME_TYPE_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=100)
    extension = models.CharField(db_column="EXTENSION", max_length=10)

    class Meta:
        managed = True
        db_table = "FILE_MIME_TYPE"


class FileValidTypeFile(models.Model):
    file_validation_type = models.ForeignKey(
        "FileValidationType",
        models.DO_NOTHING,
        db_column="FILE_VALIDATION_TYPE_ID",
        related_name="+",
    )
    file = models.ForeignKey(
        File, models.DO_NOTHING, db_column="FILE_ID", related_name="+"
    )
    validation_date = models.DateTimeField(db_column="VALIDATION_DATE")

    class Meta:
        managed = True
        db_table = "FILE_VALID_TYPE_FILE"
        unique_together = (("file_validation_type", "file"),)


class FileValidTypeFileLog(models.Model):
    file_valid_type_file_log_id = models.AutoField(
        db_column="FILE_VALID_TYPE_FILE_LOG_ID", primary_key=True
    )
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")
    user_id = models.IntegerField(db_column="USER_ID")
    action = models.CharField(db_column="ACTION", max_length=500)
    data = models.TextField(db_column="DATA")
    id1 = models.IntegerField(db_column="ID1")
    field1 = models.CharField(db_column="FIELD1", max_length=30)
    id2 = models.IntegerField(db_column="ID2")
    field2 = models.CharField(db_column="FIELD2", max_length=30)

    class Meta:
        managed = True
        db_table = "FILE_VALID_TYPE_FILE_LOG"


class FileValidationType(models.Model):
    file_validation_type_id = models.AutoField(
        db_column="FILE_VALIDATION_TYPE_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=100, blank=True, null=True)
    sort = models.IntegerField(db_column="SORT")

    class Meta:
        managed = True
        db_table = "FILE_VALIDATION_TYPE"


class FileValidationTypeT(models.Model):
    file_validation_type = models.ForeignKey(
        FileValidationType,
        models.CASCADE,
        db_column="FILE_VALIDATION_TYPE_ID",
        related_name="+",
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "FILE_VALIDATION_TYPE_T"
        unique_together = (("file_validation_type", "language"),)


class IrFileAccessType(models.Model):
    ir_file_access_type_id = models.AutoField(
        db_column="IR_FILE_ACCESS_TYPE_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=50)

    class Meta:
        managed = True
        db_table = "IR_FILE_ACCESS_TYPE"


class IrFilecomplementanswer(models.Model):
    instance_resource = models.OneToOneField(
        "core.InstanceResource",
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    ir_file_access_type = models.ForeignKey(
        IrFileAccessType,
        models.CASCADE,
        db_column="IR_FILE_ACCESS_TYPE_ID",
        related_name="+",
    )
    enable_unlink = models.PositiveSmallIntegerField(db_column="ENABLE_UNLINK")
    enable_physical_document = models.PositiveSmallIntegerField(
        db_column="ENABLE_PHYSICAL_DOCUMENT"
    )
    enable_format = models.PositiveSmallIntegerField(db_column="ENABLE_FORMAT")
    accessible_after_expiration = models.PositiveSmallIntegerField(
        db_column="ACCESSIBLE_AFTER_EXPIRATION"
    )

    class Meta:
        managed = True
        db_table = "IR_FILECOMPLEMENTANSWER"


class IrFilecomplementreqCc(models.Model):
    ir_filecomplementreq_cc_id = models.AutoField(
        db_column="IR_FILECOMPLEMENTREQ_CC_ID", primary_key=True
    )
    instance_resource = models.ForeignKey(
        "IrFilecomplementrequest",
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        related_name="+",
    )
    file_content_category = models.ForeignKey(
        FileContentCategory,
        models.CASCADE,
        db_column="FILE_CONTENT_CATEGORY_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "IR_FILECOMPLEMENTREQ_CC"


class IrFilecomplementrequest(models.Model):
    instance_resource = models.OneToOneField(
        "core.InstanceResource",
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    ir_file_access_type = models.ForeignKey(
        IrFileAccessType,
        models.CASCADE,
        db_column="IR_FILE_ACCESS_TYPE_ID",
        related_name="+",
    )
    enable_expiring_date = models.PositiveSmallIntegerField(
        db_column="ENABLE_EXPIRING_DATE"
    )
    pdf_class = models.CharField(
        db_column="PDF_CLASS", max_length=500, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "IR_FILECOMPLEMENTREQUEST"


class IrFilelist(models.Model):
    instance_resource_id = models.AutoField(
        db_column="INSTANCE_RESOURCE_ID", primary_key=True
    )
    ir_file_access_type = models.ForeignKey(
        IrFileAccessType,
        models.CASCADE,
        db_column="IR_FILE_ACCESS_TYPE_ID",
        related_name="+",
    )
    file_validation_type = models.ForeignKey(
        FileValidationType,
        models.CASCADE,
        db_column="FILE_VALIDATION_TYPE_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    access_foreign_id = models.CharField(
        db_column="ACCESS_FOREIGN_ID", max_length=100, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "IR_FILELIST"


class IrFileupload(models.Model):
    instance_resource = models.OneToOneField(
        "core.InstanceResource",
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    page_form_group = models.ForeignKey(
        "core.PageFormGroup",
        models.CASCADE,
        db_column="PAGE_FORM_GROUP_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    ir_file_access_type = models.ForeignKey(
        IrFileAccessType,
        models.CASCADE,
        db_column="IR_FILE_ACCESS_TYPE_ID",
        related_name="+",
    )
    enable_unlink = models.PositiveSmallIntegerField(db_column="ENABLE_UNLINK")
    enable_physical_document = models.PositiveSmallIntegerField(
        db_column="ENABLE_PHYSICAL_DOCUMENT"
    )
    enable_format = models.PositiveSmallIntegerField(db_column="ENABLE_FORMAT")
    enable_unlink_different_state = models.PositiveSmallIntegerField(
        db_column="ENABLE_UNLINK_DIFFERENT_STATE"
    )

    class Meta:
        managed = True
        db_table = "IR_FILEUPLOAD"


class IrFileuploadCc(models.Model):
    ir_fileupload_cc_id = models.AutoField(
        db_column="IR_FILEUPLOAD_CC_ID", primary_key=True
    )
    instance_resource = models.ForeignKey(
        IrFileupload, models.CASCADE, db_column="INSTANCE_RESOURCE_ID", related_name="+"
    )
    file_content_category = models.ForeignKey(
        FileContentCategory,
        models.CASCADE,
        db_column="FILE_CONTENT_CATEGORY_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "IR_FILEUPLOAD_CC"


class IrFilevalidation(models.Model):
    instance_resource = models.OneToOneField(
        "core.InstanceResource",
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    ir_file_access_type = models.ForeignKey(
        IrFileAccessType,
        models.CASCADE,
        db_column="IR_FILE_ACCESS_TYPE_ID",
        related_name="+",
    )
    read_file_validation_type = models.ForeignKey(
        FileValidationType,
        models.CASCADE,
        db_column="READ_FILE_VALIDATION_TYPE_ID",
        related_name="+",
    )
    write_file_validation_type = models.ForeignKey(
        FileValidationType,
        models.CASCADE,
        db_column="WRITE_FILE_VALIDATION_TYPE_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "IR_FILEVALIDATION"
