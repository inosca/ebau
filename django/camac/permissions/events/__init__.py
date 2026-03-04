# Import all modules in this folder so the event receivers are registered
# automatically without having to define each file as caluma event receiver
# module

from . import (  # noqa: F401
    ktso_afu_custom_task_form,
)
from .core import *  # noqa: F401 F403
