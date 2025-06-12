from pydantic import Field

from camac.settings.ebau_schema import EBauConfig, ModuleApplicationConfig


class ProductNumberConfig(EBauConfig):
    number: int = Field(description="Product number")
    name: str = Field(
        description="Name of the product number. Use gettext if it needs to be translated."
    )
    only_for_services: list[str] | None = Field(
        description="List of service slugs which this product number is visible for.",
        default=None,
    )
    only_for_service_groups: list[str] | None = Field(
        description=(
            "List of service_group slugs which this product number is visible for."
            "For example if you want to only allow product numbers for cantonal services."
        ),
        default=None,
    )
    not_for_services: list[str] | None = Field(
        description="List of service slugs which this product number is NOT visible for.",
        default=None,
    )
    only_subsequent_charge: bool | None = Field(
        description="Should this product number be only available if an invoice exists already.",
        default=False,
    )


class WilkenConfig(EBauConfig):
    encoding: str = Field(description="How should the exported files be encoded.")
    newline_character: str
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


class BillingConfig(ModuleApplicationConfig):
    product_numbers: list[ProductNumberConfig] | None = Field(
        description=(
            "Configure product numbers which can be selected in the billing module "
            "when creating new billing entries. This also requires the `productNumber` flag "
            "to be set to true in `ember-ebau-core/addon/config/features/[canton].js`."
        ),
        default=None,
    )
    wilken: WilkenConfig | None = Field(
        description="Configuration for the wilken export feature (currently for SZ)",
        default=None,
    )
    cantonal_service_group_slugs: list[str] | None = Field(
        description="Which ServiceGroup's are cantonal. List of slugs.", default=None
    )
