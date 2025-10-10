from pydantic import Field

from camac.settings.ebau_schema import EBauConfig, ModuleApplicationConfig


class UserNotificationConfig(EBauConfig):
    user_invited: str = Field(
        description="Slug of the notification that should be sent out when a user is invited."
    )


class UserConfig(ModuleApplicationConfig):
    """
    Configuration of the user module.

    This module should be enabled in combination with the user profile view.
    """

    question_user_attributes_mapping: dict[str, str | list[str]] = Field(
        description="Mapping of question related OIDC attributes to the user model.",
        default={},
    )
    allowed_write_attributes: list[str] = Field(
        description="List of attributes which should be writeable by the user in the user profile.",
        default=[],
    )
    notifications: UserNotificationConfig | None = Field(
        description="Configuration of notifications used in the user module.",
        default=UserNotificationConfig(user_invited="user-invited"),
    )
