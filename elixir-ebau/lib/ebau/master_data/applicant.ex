defmodule Ebau.MasterData.Applicant do
  use Ash.Resource,
    otp_app: :ebau,
    domain: Ebau.MasterData,
    data_layer: AshPostgres.DataLayer,
    extensions: [Caluma.Form.Extensions.Document, Ebau.Caluma.Extensions.DocumentBacked]

  caluma_document do
    field :title, :string, question_ids: %{default: "titel"}
    field :last_name, :string, question_ids: %{default: "nachname"}
    field :first_name, :string, question_ids: %{default: "vorname"}
    field :street, :string, question_ids: %{default: "strasse"}
    field :street_number, :string, question_ids: %{default: "strasse-nummer"}
    field :zip, :string, question_ids: %{default: "plz"}
    field :town, :string, question_ids: %{default: "ort"}
    field :country, :string, question_ids: %{default: "land"}
    field :email, :string, question_ids: %{default: "e-mail"}
    field :tel, :string, question_ids: %{default: "telefon"}
    field :po_box, :string, question_ids: %{default: "postfach"}
    field :juristic_name, :string, question_ids: %{default: "juristische-person-name"}
    field :representative_juristic_name, :string, question_ids: %{default: "vertretung-juristische-person-name"}
    field :representative_title, :string, question_ids: %{default: "vertretung-titel"}
    field :representative_last_name, :string, question_ids: %{default: "vertretung-nachname"}
    field :representative_first_name, :string, question_ids: %{default: "vertretung-vorname"}
    field :representative_street, :string, question_ids: %{default: "vertretung-strasse"}
    field :representative_street_number, :string, question_ids: %{default: "vertretung-nummer"}
    field :representative_zip, :string, question_ids: %{default: "vertretung-plz"}
    field :representative_town, :string, question_ids: %{default: "vertretung-ort"}
    field :representative_country, :string, question_ids: %{default: "vertretung-land"}
    field :representative_email, :string, question_ids: %{default: "vertretung-e-mail"}
    field :representative_tel, :string, question_ids: %{default: "vertretung-telefon"}
    field :representative_po_box, :string, question_ids: %{default: "vertretung-postfach"}

    # TODO: Fields requiring value_parser (not yet supported):
    # - salutation (anrede, option parser)
    # - country_code (land, value_mapping to country codes)
    # - is_juristic_person (juristische-person, value_mapping to boolean)
    # - has_representative (vertretung, value_mapping to boolean)
    # - representative_is_juristic_person (vertretung-juristische-person, value_mapping)
    # - representative_salutation (vertretung-anrede, option parser)
    # - representative_country_code (land, value_mapping)
  end
end
