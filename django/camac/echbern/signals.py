import django.dispatch

instance_submitted = django.dispatch.Signal(
    providing_args=["instance", "user_pk", "group_pk"]
)

sb1_submitted = django.dispatch.Signal(
    providing_args=["instance", "user_pk", "group_pk"]
)
sb2_submitted = django.dispatch.Signal(
    providing_args=["instance", "user_pk", "group_pk"]
)

circulation_started = django.dispatch.Signal(
    providing_args=["instance", "user_pk", "group_pk"]
)

ruling = django.dispatch.Signal(providing_args=["instance", "user_pk", "group_pk"])

finished = django.dispatch.Signal(providing_args=["instance", "user_pk", "group_pk"])

task_send = django.dispatch.Signal(providing_args=["instance", "user_pk", "group_pk"])

accompanying_report_send = django.dispatch.Signal(
    providing_args=["instance", "user_pk", "group_pk", "context", "attachments"]
)

file_subsequently = django.dispatch.Signal(
    providing_args=["instance", "user_pk", "group_pk"]
)

change_responsibility = django.dispatch.Signal(
    providing_args=["instance", "user_pk", "group_pk"]
)

assigned_ebau_number = django.dispatch.Signal(
    providing_args=["instance", "user_pk", "group_pk"]
)
