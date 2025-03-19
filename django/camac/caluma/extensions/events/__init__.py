# Import all modules in this folder so the event receivers are registered
# automatically without having to define each file as caluma event receiver
# module

from . import (  # noqa: F401
    additional_demand,
    audit,
    caluma_workflow_notifications,
    cantonal_exam,
    check_gwr_relevancy,
    complete_check,
    construction_acceptance,
    construction_monitoring,
    decision,
    direct_inquiry,
    distribution,
    ebau_number,
    general,
    rejection,
    sb,
    simple_workflow,
)
