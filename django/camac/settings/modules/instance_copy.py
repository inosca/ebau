from pydantic import Field

from camac.settings.ebau_schema import EBauConfig, ModuleApplicationConfig, ModuleConfig


class BaseCopyFormConfig(EBauConfig):
    instance_id_slug: str | None = Field(
        description="Slug of question in target form where instance id should be copied into.",
        default=None,
    )
    special_id_slug: str | None = Field(
        description="Slug of question in target form where special id (Dossiernumber / eBau number) should be copied into.",
        default=None,
    )
    form_slug: str | None = Field(
        description="If this copy type can only be used in combination with a specific target form, it can be validated by setting this field.",
        default=None,
    )
    copy_attachments: bool = Field(
        description="If set to True, attachments will be copied as well.",
        default=True,
    )


class ConditionalTableCopyConfig(EBauConfig):
    target_question: str = Field(
        description="Copy target table question slug",
    )
    condition_questions: list[str] = Field(
        description="Versioned single choice question slugs whose answer determines the source.",
    )
    sources_by_answer: dict[str, list[str]] = Field(
        description="Map full option slug value to versioned source table question slugs",
    )
    default_source_questions: list[str] = Field(
        description="Fallback versioned source table question slug when no condition question answer matches",
        default_factory=list,
    )


class AllowListedCopyFormConfig(BaseCopyFormConfig):
    simple_questions: list[str] = Field(
        description="List of 'simple', i.e. non-table question slugs that should be copied.",
        default_factory=list,
    )
    table_questions: list[str] = Field(
        description="List of table question slugs that should be copied.",
        default_factory=list,
    )
    link_source_document: bool = Field(
        description="Flag for setting the source document on the target document",
        default=False,
    )
    conditional_table_questions: list[ConditionalTableCopyConfig] = Field(
        description="Table mapping config for tables whose source depends on a condition question answer.",
        default_factory=list,
    )


class DenyListedCopyFormConfig(BaseCopyFormConfig):
    exclude_forms: list[str] = Field(
        description="List of form slugs that should not be copied.",
        default_factory=list,
    )
    exclude_questions: list[str] = Field(
        description="List of question slugs that should not be copied.",
        default_factory=list,
    )


type CopyFormConfig = AllowListedCopyFormConfig | DenyListedCopyFormConfig


class InstanceCopyConfig(ModuleApplicationConfig):
    enabled: bool = True
    full: DenyListedCopyFormConfig | None = Field(
        description="Configuration for the 'full' copy type.",
        default_factory=DenyListedCopyFormConfig,
    )
    full_without_confirmation: DenyListedCopyFormConfig | None = Field(
        description="Configuration for the 'full' copy type, but excluding confirmation answers. If not configured, `full` will be used instead",
        default=None,
    )
    extend_validity: CopyFormConfig | None = Field(
        description="Configuration for the 'extend_validity' (Verlängerung Geltungsdauer) copy type.",
        default=None,
    )
    demolition_payment: CopyFormConfig | None = Field(
        description="Configuration for the 'demolition_payment' (Antrag auf Auszahlung Abbruchprämie) copy type.",
        default=None,
    )
    ebbw_next_phase: CopyFormConfig | None = Field(
        description="Configuration for the 'ebbw_next_phase' (eBau Beitragswesen) copy type. This copy type is used to copy data from the current phase to the next phase of a project.",
        default=None,
    )

    def copy_types(self) -> list[str]:
        """Return all configured copy types."""

        target_fields = [
            "full",
            "full_without_confirmation",
            "extend_validity",
            "demolition_payment",
            "ebbw_next_phase",
        ]
        return [field for field in target_fields if getattr(self, field) is not None]

    def has_copy_config(self, copy_type: str) -> bool:
        """Check if a specific copy type is configured."""
        return copy_type in self.copy_types()

    def get_copy_config(self, copy_type: str) -> CopyFormConfig:
        """Return the configuration for a specific copy type."""
        if copy_type not in self.copy_types():  # pragma: no cover
            raise ValueError(
                f"Invalid copy type '{copy_type}'. Valid copy types are: {self.copy_types()}"
            )

        return getattr(self, copy_type)


INSTANCE_COPY = ModuleConfig[InstanceCopyConfig](
    default=InstanceCopyConfig(),
    kt_bern=InstanceCopyConfig(
        full=DenyListedCopyFormConfig(
            exclude_forms=[
                "8-freigabequittung",
            ],
        ),
        full_without_confirmation=DenyListedCopyFormConfig(
            exclude_forms=[
                "7-bestaetigung",
                "7-bestaetigung-vorabklaerung-v4",
                "8-freigabequittung",
                "bestaetigung-v5",
                "bestaetigung-v7",
            ],
        ),
        extend_validity=AllowListedCopyFormConfig(
            instance_id_slug="dossiernummer",
            form_slug="verlaengerung-geltungsdauer",
            simple_questions=[
                "weitere-personen",
                "verantwortliche-person-sb-identisch",
                "strasse-flurname",
                "nr",
                "plz-grundstueck-v3",
                "ort-grundstueck",
                "gemeinde",
                "beschreibung-bauvorhaben",
            ],
            table_questions=[
                "personalien-gesuchstellerin",
                "personalien-vertreterin-mit-vollmacht",
                "personalien-grundeigentumerin",
                "personalien-gebaudeeigentumerin",
                "personalien-projektverfasserin",
                "personalien-sb",
                "parzelle",
            ],
        ),
        demolition_payment=AllowListedCopyFormConfig(
            instance_id_slug="antrag-auf-auszahlung-dossiernummer-gesuch",
            form_slug="antrag-auf-auszahlung",
            link_source_document=True,
            simple_questions=[
                "gemeinde",
            ],
            conditional_table_questions=[
                ConditionalTableCopyConfig(
                    target_question="personalien-gesuchstellerin",
                    condition_questions=["eigentuemerschaft-identisch-v7"],
                    sources_by_answer={
                        "eigentuemerschaft-identisch-v7-ja": [
                            "personalien-gesuchstellerin"
                        ],
                        "eigentuemerschaft-identisch-v7-nein": [
                            "personalien-eigentuemerin-v7"
                        ],
                    },
                    default_source_questions=["personalien-gesuchstellerin"],
                )
            ],
        ),
    ),
    kt_ag=InstanceCopyConfig(
        demolition_payment=AllowListedCopyFormConfig(
            special_id_slug="dossier-number-reference",
            form_slug="auszahlung-abbruchpraemie",
            simple_questions=[
                "gemeinde",
            ],
            table_questions=[
                "personalien-gesuchstellerin",
                "personalien-grundeigentumerin",
                "personalien-gebaudeeigentumerin",
                "personalien-projektverfasserin",
                "personalien-rechnungsempfaenger",
                "vertreterin-mit-vollmacht",
            ],
        ),
    ),
    kt_uri=InstanceCopyConfig(),
    kt_gr=InstanceCopyConfig(
        ebbw_next_phase=DenyListedCopyFormConfig(
            exclude_questions=["einleitung-des-verfahrens"],
            exclude_forms=["dokumente-ebbw"],
            copy_attachments=False,
        )
    ),
    kt_so=InstanceCopyConfig(),
    kt_sg=InstanceCopyConfig(),
)
