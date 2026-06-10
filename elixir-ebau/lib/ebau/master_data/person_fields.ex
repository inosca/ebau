defmodule Ebau.MasterData.PersonFields do
  @moduledoc """
  Spark DSL fragment that adds shared person field declarations to the
  `caluma_document` section.

  Used by the four person-type master data resources (Applicant, Landowner,
  ProjectAuthor, InvoiceRecipient) which all share the same set of personal
  detail and representative fields.

  ## Usage

      use Ash.Resource,
        fragments: [Ebau.MasterData.PersonFields],
        extensions: [Caluma.Form.Extensions.Document]
  """

  use Spark.Dsl.Fragment,
    of: Ash.Resource,
    extensions: [Caluma.Form.Extensions.Document]

  caluma_document do
    answer :title, :string, question_id: {Ebau.Caluma.CantonResolver, %{default: "titel"}}

    answer :last_name, :string, question_id: {Ebau.Caluma.CantonResolver, %{default: "nachname"}}

    answer :first_name, :string, question_id: {Ebau.Caluma.CantonResolver, %{default: "vorname"}}

    answer :street, :string, question_id: {Ebau.Caluma.CantonResolver, %{default: "strasse"}}

    answer :street_number, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "strasse-nummer"}}

    answer :zip, :string, question_id: {Ebau.Caluma.CantonResolver, %{default: "plz"}}

    answer :town, :string, question_id: {Ebau.Caluma.CantonResolver, %{default: "ort"}}

    answer :country, :string, question_id: {Ebau.Caluma.CantonResolver, %{default: "land"}}

    answer :email, :string, question_id: {Ebau.Caluma.CantonResolver, %{default: "e-mail"}}

    answer :tel, :string, question_id: {Ebau.Caluma.CantonResolver, %{default: "telefon"}}

    answer :po_box, :string, question_id: {Ebau.Caluma.CantonResolver, %{default: "postfach"}}

    answer :juristic_name, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "juristische-person-name"}}

    answer :representative_juristic_name, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "vertretung-juristische-person-name"}}

    answer :representative_title, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "vertretung-titel"}}

    answer :representative_last_name, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "vertretung-nachname"}}

    answer :representative_first_name, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "vertretung-vorname"}}

    answer :representative_street, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "vertretung-strasse"}}

    answer :representative_street_number, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "vertretung-nummer"}}

    answer :representative_zip, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "vertretung-plz"}}

    answer :representative_town, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "vertretung-ort"}}

    answer :representative_country, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "vertretung-land"}}

    answer :representative_email, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "vertretung-e-mail"}}

    answer :representative_tel, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "vertretung-telefon"}}

    answer :representative_po_box, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "vertretung-postfach"}}
  end
end
