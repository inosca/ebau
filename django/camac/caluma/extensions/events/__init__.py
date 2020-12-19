# Import all modules in this folder so the event receivers are registered
# automatically without having to define each file as caluma event receiver
# module

# noqa: F401
from . import audit, circulation, decision, ebau_number, general, simple_workflow
