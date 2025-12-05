from django.db.models import F
from pydantic import ConfigDict, Field

from camac.settings.ebau_schema import EBauConfig, ModuleApplicationConfig


class PersonConfig(EBauConfig):
    """Configuration of needed slugs to represent a person in Caluma."""

    table_question: str = Field(
        description="Question slug of the table question",
        default="personalien-gesuchstellerin",
    )
    is_juristic: str = Field(
        description="Question slug to determine whether the person is juristic or not",
        default="juristische-person-gesuchstellerin",
    )
    is_juristic_yes: str = Field(
        description="Answer value to determine that the person is indeed juristic",
        default="juristische-person-gesuchstellerin-ja",
    )
    juristic_name: str = Field(
        description="Question slug for the persons juristic name",
        default="name-juristische-person-gesuchstellerin",
    )
    first_name: str = Field(
        description="Question slug for the persons first name",
        default="vorname-gesuchstellerin",
    )
    last_name: str = Field(
        description="Question slug for the persons last name",
        default="name-gesuchstellerin",
    )


class AnnotationsConfig(EBauConfig):
    """Configuration for the annotations of the work item list row model."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    special_id: F = Field(
        description="Annotation for the special ID",
        default=F("case__family__meta__dossier-number"),
    )
    municipality: str | None = Field(
        description="Question slug for the municipality", default="gemeinde"
    )
    description: str | list[str] = Field(
        description="Question slug for the description",
        default="beschreibung-bauvorhaben",
    )
    applicants: PersonConfig | None = PersonConfig()


class WorkItemListConfig(ModuleApplicationConfig):
    """Configuration of the work item list module."""

    annotations: AnnotationsConfig = AnnotationsConfig()

    available_tasks_include_count: bool = Field(
        description="If enabled, the options in the task filter will compute a count of work items for that task",
        default=False,
    )
    available_tasks_include_templates: bool = Field(
        description="If enabled, work item templates will appear in the options for the task filter",
        default=False,
    )
    available_tasks_default: list[str] = Field(
        description="Task slugs that always appear in the options for the task filter",
        default_factory=list,
    )
    available_tasks_for_role: dict[str, list[str]] = Field(
        description="Task slugs that only appear in the options for the task filter if a certain role is given",
        default_factory=dict,
    )
    available_tasks_for_service_group: dict[str, list[str]] = Field(
        description="Task slugs that only appear in the options for the task filter if a certain service group is given",
        default_factory=dict,
    )
