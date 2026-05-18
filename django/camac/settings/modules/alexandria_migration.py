from pydantic import Field

from camac.settings.ebau_schema import ModuleApplicationConfig, ModuleConfig


class AlexandriaMigrationConfig(ModuleApplicationConfig):
    fallback_category: str = Field(
        description="Alexandria category to migrate to if attachment is in no sections",
        default="intern",
    )
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
    context_mark_mapping: dict[str, str] = Field(
        description=(
            "Mapping between legacy context property flags and alexandria"
            "marks. If the property is true in the context property, the"
            "document will be marked with the corresponding mark."
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
            # "Entscheiddokumente" (ID 8): There are 352 documents that are
            # still in this invisible attachment section. They will be migrated
            # into the internal category.
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
        context_mark_mapping={
            "isDecision": "decision",
            "isPublished": "publication",
            "isReplaced": "void",
            "for_geometer": "geometer",
        },
    ),
    kt_schwyz=AlexandriaMigrationConfig(
        enabled=True,
        category_mapping={
            1: "dokumente-des-gesuchstellers",
            2: "interne-ablage-nur-gruppenintern-sichtbar",
            4: "auflagedokumente",
            5: "einsprachen",
            6: "bauentscheid-und-merkblatter",
            7: "interne-ablage-nur-gruppenintern-sichtbar-1",
            8: "schriftenverkehr",
            9: "dokumente-fur-gesuchsteller",
            10: "rechtsmittel",
            11: "baukontrolle-und-bauabnahme",
            12: "dokumente-dateien-und-anhange",
        },
        category_suffix_mapping={
            "dokument-grundstucksangaben": "-grundstucksangaben",
            "dokument-gutachten-nachweise-begrundungen": "-gutachten-nachweise-begrundungen",
            "dokument-projektplane-projektbeschrieb": "-projektplane-projektbeschrieb",
            "dokument-weitere-gesuchsunterlagen": "-weitere-gesuchsunterlagen",
        },
        # TODO Validate these
        context_mark_mapping={
            "isDecision": "decision",
            "isPublished": "publication",
            # SZ Prod currently only has "isReplaced"
            "isReplaced": "void",
        },
    ),
)
