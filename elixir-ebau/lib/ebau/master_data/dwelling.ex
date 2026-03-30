defmodule Ebau.MasterData.Dwelling do
  use Ash.Resource,
    otp_app: :ebau,
    domain: Ebau.MasterData,
    data_layer: AshPostgres.DataLayer,
    extensions: [Caluma.Form.Extensions.Document]

  alias Ebau.Caluma.Calculations.DocumentAnswer

  calculations do
    calculate :floor_number, Caluma.Form.Types.AnswerValue,
              {DocumentAnswer, question_ids: %{default: "stockwerknummer"}}

    calculate :location_on_floor, Caluma.Form.Types.AnswerValue,
              {DocumentAnswer, question_ids: %{default: "lage"}}

    calculate :number_of_rooms, Caluma.Form.Types.AnswerValue,
              {DocumentAnswer, question_ids: %{default: "anzahl-zimmer"}}

    calculate :kitchen_facilities, Caluma.Form.Types.AnswerValue,
              {DocumentAnswer, question_ids: %{default: "kocheinrichtung"}}

    calculate :area, Caluma.Form.Types.AnswerValue,
              {DocumentAnswer, question_ids: %{default: "flaeche"}}

    # TODO: Fields requiring value_parser (not yet supported):
    # - name_of_building (dazugehoeriges-gebaeude-auswahl, dynamic_option)
    # - floor_type (stockwerktyp, value_mapping to integer codes)
    # - has_kitchen_facilities (kocheinrichtung, value_mapping to boolean)
    # - multiple_floors (maisonette, value_mapping to boolean)
    # - usage_limitation (zwg, value_mapping to integer codes)
  end
end
