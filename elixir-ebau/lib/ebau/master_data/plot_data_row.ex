defmodule Ebau.MasterData.PlotDataRow do
  @moduledoc """
  Plot/parcel data (Parzelle) extracted from a Caluma table question.

  Contains the plot number, EGRID number, east/north coordinates, and
  postal code. Each row corresponds to one row document under the
  `parzellen` table question.

  The coordinates are used by `Ebau.Instances.Calculations.GisLinkForInstance`
  to substitute `{x}` and `{y}` placeholders in GIS link templates.
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
    answer :plot_number, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "parzellennummer"}}

    answer :egrid_number, :string, question_id: {Ebau.Caluma.CantonResolver, %{default: "e-grid"}}

    answer :coord_east, :string,
      question_id:
        {Ebau.Caluma.CantonResolver, %{default: "lagekoordinaten-ost", gr: "coordinates-east"}}

    answer :coord_north, :string,
      question_id:
        {Ebau.Caluma.CantonResolver, %{default: "lagekoordinaten-nord", gr: "coordinates-north"}}

    answer :zip, :string, question_id: {Ebau.Caluma.CantonResolver, %{default: "plz"}}
  end
end
