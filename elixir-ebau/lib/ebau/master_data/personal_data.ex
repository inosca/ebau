defmodule Ebau.MasterData.PersonalData do
  @moduledoc """
  Shared calculations for personal data table resources (applicants, landowners, etc.).

  All SO personal data tables share the same column mapping (SO_PERSONAL_DATA_MAPPING).
  This module provides a `__using__` macro that adds the common calculations.
  """

  defmacro __using__(_opts) do
    quote do
      alias Ebau.Caluma.Calculations.DocumentAnswer

      calculations do
        calculate :title, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "titel"}}

        calculate :last_name, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "nachname"}}

        calculate :first_name, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "vorname"}}

        calculate :street, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "strasse"}}

        calculate :street_number, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "strasse-nummer"}}

        calculate :zip, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "plz"}}

        calculate :town, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "ort"}}

        calculate :country, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "land"}}

        calculate :email, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "e-mail"}}

        calculate :tel, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "telefon"}}

        calculate :po_box, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "postfach"}}

        calculate :juristic_name, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "juristische-person-name"}}

        calculate :representative_juristic_name, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "vertretung-juristische-person-name"}}

        calculate :representative_title, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "vertretung-titel"}}

        calculate :representative_last_name, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "vertretung-nachname"}}

        calculate :representative_first_name, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "vertretung-vorname"}}

        calculate :representative_street, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "vertretung-strasse"}}

        calculate :representative_street_number, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "vertretung-nummer"}}

        calculate :representative_zip, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "vertretung-plz"}}

        calculate :representative_town, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "vertretung-ort"}}

        calculate :representative_country, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "vertretung-land"}}

        calculate :representative_email, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "vertretung-e-mail"}}

        calculate :representative_tel, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "vertretung-telefon"}}

        calculate :representative_po_box, Caluma.Form.Types.AnswerValue,
                  {DocumentAnswer, question_ids: %{default: "vertretung-postfach"}}

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
  end
end
