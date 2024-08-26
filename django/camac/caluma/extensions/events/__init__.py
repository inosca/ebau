# Import all modules in this folder so the event receivers are registered
# automatically without having to define each file as caluma event receiver
# module

from . import (  # noqa: F401
    additional_demand,
    audit,
    caluma_workflow_notifications,
    complete_check,
    construction_acceptance,
    construction_monitoring,
    decision,
    distribution,
    ebau_number,
    general,
    rejection,
    sb,
    simple_workflow,
)
