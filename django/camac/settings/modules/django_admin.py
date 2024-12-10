DJANGO_ADMIN = {
    "default": {
        "ENABLED_MODELS": [
            "caluma_workflow.Case",
            "caluma_workflow.WorkItem",
            "permissions.AccessLevel",
            "user.Group",
            "user.Role",
            "user.Service",
            "user.ServiceGroup",
            "user.User",
        ],
        "CUSTOMER_MANAGED_MODELS": ["user.User", "user.Group", "user.Service"],
    },
    "demo": {
        "ENABLED": True,
        "ENABLED_MODELS": ["core.InstanceResource", "core.Resource"],
    },
    "kt_gr": {
        "ENABLED": True,
        "ENABLED_MODELS": [
            "alexandria_core.Category",
            "core.InstanceResource",
            "core.Resource",
            "core.ServiceContent",
            "gis.GISDataSource",
            "notification.NotificationTemplate",
        ],
        "CUSTOMER_MANAGED_MODELS": [
            "notification.NotificationTemplate",
            "core.ServiceContent",
        ],
    },
    "kt_so": {
        "ENABLED": True,
        "ENABLED_MODELS": [
            "alexandria_core.Category",
            "core.InstanceResource",
            "core.Resource",
            "gis.GISDataSource",
            "notification.NotificationTemplate",
            "django_q.Success",
            "django_q.Failure",
            "django_q.OrmQ",
        ],
        "CUSTOMER_MANAGED_MODELS": ["gis.GISDataSource"],
    },
    "kt_bern": {
        "ENABLED": True,
        "ENABLED_MODELS": [
            "gis.GISDataSource",
            "django_q.Success",
            "django_q.Failure",
            "django_q.OrmQ",
        ],
    },
    "kt_schwyz": {"ENABLED": True},
    "kt_uri": {"ENABLED": True},
    "kt_ag": {
        "ENABLED": True,
        "ENABLED_MODELS": [
            "alexandria_core.Category",
            "core.InstanceResource",
            "core.Resource",
            "gis.GISDataSource",
            "notification.NotificationTemplate",
        ],
    },
}
