from camac.settings.ebau_schema import ModuleConfig
from camac.settings.modules.caluma_simple_workflow_schema import (
    CalumaSimpleWorkflowConfig,
)

from .kt_ag import AG_CALUMA_SIMPLE_WORKFLOW_SETTINGS
from .kt_bern import BE_CALUMA_SIMPLE_WORKFLOW_SETTINGS
from .kt_gr import GR_CALUMA_SIMPLE_WORKFLOW_SETTINGS
from .kt_schwyz import SZ_CALUMA_SIMPLE_WORKFLOW_SETTINGS
from .kt_sg import SG_CALUMA_SIMPLE_WORKFLOW_SETTINGS
from .kt_so import SO_CALUMA_SIMPLE_WORKFLOW_SETTINGS
from .kt_uri import UR_CALUMA_SIMPLE_WORKFLOW_SETTINGS

CALUMA_SIMPLE_WORKFLOW = ModuleConfig[CalumaSimpleWorkflowConfig](
    default=CalumaSimpleWorkflowConfig(),
    kt_schwyz=SZ_CALUMA_SIMPLE_WORKFLOW_SETTINGS,
    kt_bern=BE_CALUMA_SIMPLE_WORKFLOW_SETTINGS,
    kt_so=SO_CALUMA_SIMPLE_WORKFLOW_SETTINGS,
    kt_uri=UR_CALUMA_SIMPLE_WORKFLOW_SETTINGS,
    kt_gr=GR_CALUMA_SIMPLE_WORKFLOW_SETTINGS,
    kt_ag=AG_CALUMA_SIMPLE_WORKFLOW_SETTINGS,
    kt_sg=SG_CALUMA_SIMPLE_WORKFLOW_SETTINGS,
)
