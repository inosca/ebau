from pydantic import Field

from camac.settings.ebau_schema import EBauConfig, ModuleApplicationConfig, ModuleConfig


class AllowListedCopyFormConfig(EBauConfig):
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
    simple_questions: list[str] = Field(
        description="List of 'simple', i.e. non-table question slugs that should be copied.",
        default_factory=list,
    )
    table_questions: list[str] = Field(
        description="List of table question slugs that should be copied.",
        default_factory=list,
    )


class InstanceCopyConfig(ModuleApplicationConfig):
    enabled: bool = True
    extend_validity: AllowListedCopyFormConfig | None = Field(
        description="Configuration for the 'extend_validity' (Verlängerung Geltungsdauer) copy type.",
        default=None,
    )
    demolition_payment: AllowListedCopyFormConfig | None = Field(
        description="Configuration for the 'demolition_payment' (Antrag auf Auszahlung Abbruchprämie) copy type.",
        default=None,
    )

    def special_copy_types(self):
        """Return all 'special' copy types (not 'full')."""

        target_fields = ["extend_validity", "demolition_payment"]
        return [field for field in target_fields if getattr(self, field) is not None]


INSTANCE_COPY = ModuleConfig[InstanceCopyConfig](
    default=InstanceCopyConfig(),
    kt_bern=InstanceCopyConfig(
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
        )
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
                "parzelle",
            ],
        )
    ),
    kt_uri=InstanceCopyConfig(),
    kt_gr=InstanceCopyConfig(),
    kt_so=InstanceCopyConfig(),
    kt_sg=InstanceCopyConfig(),
)
