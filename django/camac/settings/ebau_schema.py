from typing import Generic

from pydantic import BaseModel, ConfigDict
from typing_extensions import TypeVar


class EBauConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


Module = TypeVar("Module")


class ModuleConfig(EBauConfig, Generic[Module]):
    default: Module
    demo: Module | None = None
    test: Module | None = None
    kt_schwyz: Module | None = None
    kt_bern: Module | None = None
    kt_so: Module | None = None
    kt_uri: Module | None = None
    kt_gr: Module | None = None
    kt_ag: Module | None = None


class ModuleApplicationConfig(EBauConfig):
    enabled: bool = False
