import django.dispatch

instance_submitted = django.dispatch.Signal()
sb1_submitted = django.dispatch.Signal()
sb2_submitted = django.dispatch.Signal()
circulation_started = django.dispatch.Signal()
circulation_ended = django.dispatch.Signal()
ruling = django.dispatch.Signal()
finished = django.dispatch.Signal()
task_send = django.dispatch.Signal()
accompanying_report_send = django.dispatch.Signal()
file_subsequently = django.dispatch.Signal()
change_responsibility = django.dispatch.Signal()
assigned_ebau_number = django.dispatch.Signal()
