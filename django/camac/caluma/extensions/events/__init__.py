# Import all modules in this folder so the event receivers are registered
# automatically without having to define each file as caluma event receiver
# module

from . import (  # noqa: F401
    additional_demand,
    address_assignment,
    audit,
    bab,
    caluma_workflow_notifications,
    cantonal_exam,
    check_gwr_relevancy,
    complete_check,
    construction_monitoring,
    deadlines,
    decision,
    direct_inquiry,
    distribution,
    ebau_number,
    formal_exam,
    general,
    gever,
    rejection,
    sb,
    simple_workflow,
)
