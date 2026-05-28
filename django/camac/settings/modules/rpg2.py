from camac.settings.ebau_schema import ModuleConfig
from camac.settings.modules.rpg2_schema import RPG2Config

RPG2 = ModuleConfig[RPG2Config](
    default=RPG2Config(),
)
