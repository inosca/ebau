# Import all modules in this folder so the event receivers are registered
# automatically without having to define each file as caluma event receiver
# module

from . import (  # noqa: F401
    additional_demand,
    address_assignment,
    audit,
    bab,
    caluma_workflow_notifications,
    check_gwr_relevancy,
    complete_check,
    construction_monitoring,
    deadlines,
    decision,
    direct_inquiry,
    distribution,
    distribution_ag_afb_specific,
    ebau_number,
    formal_exam,
    general,
    ktso_afu_custom_task_form,
    publication,
    rejection,
    sb,
    simple_workflow,
)
