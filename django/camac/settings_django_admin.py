DJANGO_ADMIN = {
    "default": {
        "ENABLED_MODELS": [
            "caluma_workflow.Case",
            "caluma_workflow.WorkItem",
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
            "gis.GISDataSource",
            "notification.NotificationTemplate",
        ],
        "CUSTOMER_MANAGED_MODELS": ["notification.NotificationTemplate"],
    },
    "kt_so": {
        "ENABLED": True,
        "ENABLED_MODELS": [
            "alexandria_core.Category",
            "core.InstanceResource",
            "core.Resource",
            "gis.GISDataSource",
            "notification.NotificationTemplate",
        ],
        "CUSTOMER_MANAGED_MODELS": ["gis.GISDataSource"],
    },
    "kt_bern": {
        "ENABLED": True,
        "ENABLED_MODELS": [
            "gis.GISDataSource",
        ],
    },
    "kt_schwyz": {"ENABLED": True},
    "kt_uri": {"ENABLED": True},
}
