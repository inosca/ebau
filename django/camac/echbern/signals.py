import django.dispatch

instance_submitted = django.dispatch.Signal(providing_args=["instance", "group_pk"])
