defmodule Ebau.MasterData.EnergyDevice do
  @moduledoc """
  HVAC/energy system (Gebaeudetechnik) extracted from a Caluma table question.

  Contains the device type. Each row corresponds to one row document under
  the `gebaeudetechnik` table question.

  Used for GWR (federal building register) reporting.
  """

  use Ash.Resource,
    otp_app: :ebau,
    domain: Ebau.MasterData,
    data_layer: AshPostgres.DataLayer,
    extensions: [Caluma.Form.Extensions.Document, Ebau.Caluma.Extensions.DocumentBacked]

  postgres do
    table "caluma_form_document"
    repo Ebau.Repo
    migrate? false
  end

  caluma_document do
    field :type, :string, question_ids: %{default: "anlagetyp"}

    # TODO: Fields requiring value_parser (not yet supported):
    # - name_of_building (dazugehoeriges-gebaeude-auswahl, dynamic_option)
    # - information_source (static default 869)
    # - is_heating, is_warm_water, is_heating_and_warm_water (anlagetyp, value_mapping to boolean)
    # - is_main_heating (heizsystem-art, value_mapping to boolean)
    # - energy_source (hauptheizungsanlage, value_mapping to integer codes)
  end
end
