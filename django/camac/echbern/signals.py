import django.dispatch

instance_submitted = django.dispatch.Signal(providing_args=["instance", "group_pk"])

sb1_submitted = django.dispatch.Signal(providing_args=["instance", "group_pk"])
sb2_submitted = django.dispatch.Signal(providing_args=["instance", "group_pk"])

task_send = django.dispatch.Signal(providing_args=["instance", "group_pk"])

accompanying_report_send = django.dispatch.Signal(
    providing_args=["instance", "group_pk", "attachments"]
)
