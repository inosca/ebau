defmodule Ebau.MasterData.Dwelling do
  @moduledoc """
  Residential unit (Wohnung) extracted from a Caluma table question.

  Contains details like floor number, location on floor, number of rooms,
  kitchen facilities, and area. Each row corresponds to one row document
  under the row dwelling table question.

  Used for GWR (federal building register) reporting.
  """

  use Ash.Resource,
    otp_app: :ebau,
    domain: Ebau.MasterData,
    data_layer: AshPostgres.DataLayer,
    extensions: [Caluma.Form.Extensions.Document, Ebau.Caluma.Extensions.DocumentBacked]

  caluma_document do
    field :floor_number, :string, question_ids: %{default: "stockwerknummer"}
    field :location_on_floor, :string, question_ids: %{default: "lage"}
    field :number_of_rooms, :string, question_ids: %{default: "anzahl-zimmer"}
    field :kitchen_facilities, :string, question_ids: %{default: "kocheinrichtung"}
    field :area, :string, question_ids: %{default: "flaeche"}

    # TODO: Fields requiring value_parser (not yet supported):
    # - name_of_building (dazugehoeriges-gebaeude-auswahl, dynamic_option)
    # - floor_type (stockwerktyp, value_mapping to integer codes)
    # - has_kitchen_facilities (kocheinrichtung, value_mapping to boolean)
    # - multiple_floors (maisonette, value_mapping to boolean)
    # - usage_limitation (zwg, value_mapping to integer codes)
  end
end
