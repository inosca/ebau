from pydantic import Field

from camac.settings.ebau_schema import ModuleApplicationConfig


class UserConfig(ModuleApplicationConfig):
    """
    Configuration of the user module.

    This module should be enabled in combination with the user profile view.
    """

    question_user_attributes_mapping: dict[str, str | list[str]] | None = Field(
        description="Mapping of question related OIDC attributes to the user model.",
        default=None,
    )
    allowed_write_attributes: list[str] | None = Field(
        description="List of attributes which should be writeable by the user in the user profile.",
        default=None,
    )
