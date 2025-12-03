from pydantic import Field

from camac.settings.ebau_schema import ModuleApplicationConfig, ModuleConfig


class AlexandriaMigrationConfig(ModuleApplicationConfig):
    category_mapping: dict[int, str] = Field(
        description="Mapping between legacy attachment section and alexandria categories",
        default_factory=dict,
    )
    category_suffix_mapping: dict[str, str] = Field(
        description=(
            "Mapping between legacy bucket name and suffix for alexandria"
            "subcategories. This mapping assumes that the slug of an alexandria"
            "categories starts with the slug of the parent category."
        ),
        default_factory=dict,
    )


ALEXANDRIA_MIGRATION = ModuleConfig[AlexandriaMigrationConfig](
    default=AlexandriaMigrationConfig(),
    kt_bern=AlexandriaMigrationConfig(
        enabled=True,
        category_mapping={
            1: "beilagen-zum-gesuch",
            2: "beteiligte-behoerden",
            3: "alle-beteiligten",
            4: "intern",
            5: "beilagen-sb2",
            6: "beilagen-sb1",
            7: "nachforderungen",
            # TODO: "Entscheiddokumente" (ID 8): do we really have attachments
            # in this section?
            8: "intern",
            10: "beilagen-sb1",
            11: "beilagen-sb2",
            12: "nachforderungen",
            13: "beilagen-zum-gesuch",
            14: "rechtsbegehren",
        },
        category_suffix_mapping={
            "dokument-grundstucksangaben": "-grundstuecksangaben-projektbeschrieb",
            "dokument-gutachten-nachweise-begrundungen": "-gutachten-nachweise-begruendungen-ausnahmebegehren",
            "dokument-projektplane-projektbeschrieb": "-projektplaene",
            "dokument-weitere-gesuchsunterlagen": "-weitere-gesuchsunterlagen",
            "dokument-amts-fachstellen": "-amts-und-fachstellenberichte",
            "dokument-merkblaetter": "-merkblaetter",
            "dokument-rechtsbegehren": "-rechtsbegehren",
            "dokument-stellungnahmen-verfahrensbeteiligte": "-stellungnahmen-verfahrensbeteiligte",
            "dokument-leitbehoerde": "-dokumente-der-leitbehoerde",
            "dokument-entscheid": "-entscheid",
        },
    ),
)
