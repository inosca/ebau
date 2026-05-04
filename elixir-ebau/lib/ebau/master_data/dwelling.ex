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
    authorizers: Ash.Policy.Authorizer,
    extensions: [Caluma.Form.Extensions.Document]

  postgres do
    table "caluma_form_document"
    repo Ebau.Repo
    migrate? false
  end

  policies do
    policy action_type([:create, :update, :destroy]) do
      forbid_if always()
    end

    policy action_type(:read) do
      authorize_if {Ebau.Policies.Checks.HasActiveInstanceACL, via: [:family, :case]}
    end
  end

  caluma_document do
    answer :floor_number, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "stockwerknummer"}}

    answer :location_on_floor, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "lage"}}

    answer :number_of_rooms, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "anzahl-zimmer"}}

    answer :kitchen_facilities, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "kocheinrichtung"}}

    answer :area, :string, question_id: {Ebau.Caluma.CantonResolver, %{default: "flaeche"}}

    # TODO: Fields requiring value_parser (not yet supported):
    # - name_of_building (dazugehoeriges-gebaeude-auswahl, dynamic_option)
    # - floor_type (stockwerktyp, value_mapping to integer codes)
    # - has_kitchen_facilities (kocheinrichtung, value_mapping to boolean)
    # - multiple_floors (maisonette, value_mapping to boolean)
    # - usage_limitation (zwg, value_mapping to integer codes)
  end
end
