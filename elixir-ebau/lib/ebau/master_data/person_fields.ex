defmodule Ebau.MasterData.PersonFields do
  @moduledoc """
  Spark DSL extension that adds shared person field declarations to the
  `caluma_document` section.

  Used by the four person-type master data resources (Applicant, Landowner,
  ProjectAuthor, InvoiceRecipient) which all share the same set of personal
  detail and representative fields.

  ## Usage

      use Ash.Resource,
        extensions: [
          Caluma.Form.Extensions.Document,
          Ebau.MasterData.PersonFields
        ]
  """

  @fields [
    {:title, :string, {Ebau.Caluma.CantonResolver, %{default: "titel"}}},
    {:last_name, :string, {Ebau.Caluma.CantonResolver, %{default: "nachname"}}},
    {:first_name, :string, {Ebau.Caluma.CantonResolver, %{default: "vorname"}}},
    {:street, :string, {Ebau.Caluma.CantonResolver, %{default: "strasse"}}},
    {:street_number, :string, {Ebau.Caluma.CantonResolver, %{default: "strasse-nummer"}}},
    {:zip, :string, {Ebau.Caluma.CantonResolver, %{default: "plz"}}},
    {:town, :string, {Ebau.Caluma.CantonResolver, %{default: "ort"}}},
    {:country, :string, {Ebau.Caluma.CantonResolver, %{default: "land"}}},
    {:email, :string, {Ebau.Caluma.CantonResolver, %{default: "e-mail"}}},
    {:tel, :string, {Ebau.Caluma.CantonResolver, %{default: "telefon"}}},
    {:po_box, :string, {Ebau.Caluma.CantonResolver, %{default: "postfach"}}},
    {:juristic_name, :string,
     {Ebau.Caluma.CantonResolver, %{default: "juristische-person-name"}}},
    {:representative_juristic_name, :string,
     {Ebau.Caluma.CantonResolver, %{default: "vertretung-juristische-person-name"}}},
    {:representative_title, :string,
     {Ebau.Caluma.CantonResolver, %{default: "vertretung-titel"}}},
    {:representative_last_name, :string,
     {Ebau.Caluma.CantonResolver, %{default: "vertretung-nachname"}}},
    {:representative_first_name, :string,
     {Ebau.Caluma.CantonResolver, %{default: "vertretung-vorname"}}},
    {:representative_street, :string,
     {Ebau.Caluma.CantonResolver, %{default: "vertretung-strasse"}}},
    {:representative_street_number, :string,
     {Ebau.Caluma.CantonResolver, %{default: "vertretung-nummer"}}},
    {:representative_zip, :string, {Ebau.Caluma.CantonResolver, %{default: "vertretung-plz"}}},
    {:representative_town, :string, {Ebau.Caluma.CantonResolver, %{default: "vertretung-ort"}}},
    {:representative_country, :string,
     {Ebau.Caluma.CantonResolver, %{default: "vertretung-land"}}},
    {:representative_email, :string,
     {Ebau.Caluma.CantonResolver, %{default: "vertretung-e-mail"}}},
    {:representative_tel, :string,
     {Ebau.Caluma.CantonResolver, %{default: "vertretung-telefon"}}},
    {:representative_po_box, :string,
     {Ebau.Caluma.CantonResolver, %{default: "vertretung-postfach"}}}
  ]

  def fields, do: @fields

  use Spark.Dsl.Extension,
    transformers: [Ebau.MasterData.PersonFields.Transformer]
end

defmodule Ebau.MasterData.PersonFields.Transformer do
  @moduledoc false

  use Spark.Dsl.Transformer

  alias Caluma.Form.Extensions.Document.Answer

  def before?(Caluma.Form.Extensions.Document.AnswerTransformer), do: true
  def before?(_), do: false

  def transform(dsl_state) do
    dsl_state =
      Ebau.MasterData.PersonFields.fields()
      |> Enum.reduce(dsl_state, fn {name, type, question_id}, dsl ->
        entity = %Answer{name: name, type: type, question_id: question_id}
        Spark.Dsl.Transformer.add_entity(dsl, [:caluma_document], entity)
      end)

    {:ok, dsl_state}
  end
end
