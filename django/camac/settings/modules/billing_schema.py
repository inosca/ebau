from pydantic import Field

from camac.settings.ebau_schema import EBauConfig, ModuleApplicationConfig


class InvoiceConfig(EBauConfig):
    enabled: bool = Field(description="Is the invoice feature enabled?")
    template: str | None = Field(
        description="Template to use for invoice generation.", default=None
    )
    document_category: str | int = Field(
        description=("Document category to save the generated invoice to.")
    )
    convert_to_pdf: bool = Field(
        description="Convert the generated invoice to PDF instead of keeping the DOCX.",
        default=True,
    )
    file_name: str | None = Field(
        description=(
            "File name of the generated invoice without extension. Supports the "
            "placeholders `{identifier}` (dossier number) and `{datetime}`. "
            "Defaults to the name of the used template."
        ),
        default=None,
    )


class BillingDjangoAdminConfig(EBauConfig):
    hidden_fields: list[str] = Field(
        description="Billing entry fields that should be hidden in the django admin",
        default_factory=list,
    )
    hidden_calculation_modes: list[str] = Field(
        description="Billing entry calculation modes that should be hidden in the django admin",
        default_factory=list,
    )


class ProductNumberConfig(EBauConfig):
    number: int = Field(description="Product number")
    name: str = Field(
        description="Name of the product number. Use gettext if it needs to be translated."
    )
    only_for_services: list[str] = Field(
        description="List of service slugs which this product number is visible for.",
        default=[],
    )
    only_for_service_groups: list[str] = Field(
        description=(
            "List of service_group slugs which this product number is visible for."
            "For example if you want to only allow product numbers for cantonal services."
        ),
        default=[],
    )
    not_for_services: list[str] = Field(
        description="List of service slugs which this product number is NOT visible for.",
        default=[],
    )
    only_subsequent_charge: bool = Field(
        description="Should this product number be only available if an invoice exists already.",
        default=False,
    )
    only_forms: list[str] = Field(
        description="Unversioned form slugs for which this product number should be used.",
        default=[],
    )
    archived: bool = Field(
        description="This product number cannot be selected because it has been archived.",
        default=False,
    )


class WilkenConfig(EBauConfig):
    encoding: str = Field(description="How should the exported files be encoded.")
    newline_character: str
    replace_character_map: dict[str, str]
    clerk: str = Field(
        description="Wilken user name which should be used for the billing."
    )
    user_id: str = Field(
        description="Wilken id name which should be used for the billing."
    )
    invoice_file_name: str = Field(
        description="File name which should be used. Available placeholders are: identifier, datetime."
    )
    payment_purpose: str
    customer_numbers: dict[str, str] = Field(
        description="Mapping of municipality name to customer number."
    )
    keycloak_client: str = Field(
        description="Name of the keycloak client used for the api."
    )


class RapagConfig(EBauConfig):
    """Credentials for the SAP billing API in Kt. AG ("RAPAG")."""

    enabled: bool = Field(description="Enable RAPAG integration", default=False)
    client_id: str | None = Field(description="OAuth2 client ID", default=None)
    client_secret: str | None = Field(description="OAuth2 client secret", default=None)
    token_url: str | None = Field(description="OAuth2 token URL", default=None)
    base_url: str | None = Field(description="Base URL for RAPAG API", default=None)


class BillingConfig(ModuleApplicationConfig):
    product_numbers: list[ProductNumberConfig] = Field(
        description=(
            "Configure product numbers which can be selected in the billing module "
            "when creating new billing entries. This also requires the `productNumber` flag "
            "to be set to true in `ember-ebau-core/addon/config/features/[canton].js`."
        ),
        default=[],
    )
    wilken: WilkenConfig | None = Field(
        description="Configuration for the wilken export feature (currently for SZ)",
        default=None,
    )
    rapag: RapagConfig = Field(
        description="Configuration for RAPAG interface (only for kt_ag)",
        default=RapagConfig(),
    )
    cantonal_service_group_slugs: list[str] = Field(
        description="Which ServiceGroup's are cantonal. List of slugs.", default=[]
    )
    admin: BillingDjangoAdminConfig = BillingDjangoAdminConfig()
    invoice: InvoiceConfig | None = Field(
        description="Configuration for creating invoices",
        default=None,
    )
