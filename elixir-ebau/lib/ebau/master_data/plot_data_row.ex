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
    extensions: [Caluma.Form.Extensions.Document, Ebau.Caluma.Extensions.DocumentBacked]

  caluma_document do
    field :plot_number, :string, question_ids: %{default: "parzellennummer"}
    field :egrid_number, :string, question_ids: %{default: "e-grid"}

    field :coord_east, :string,
      question_ids: %{default: "lagekoordinaten-ost", gr: "coordinates-east"}

    field :coord_north, :string,
      question_ids: %{default: "lagekoordinaten-nord", gr: "coordinates-north"}

    field :zip, :string, question_ids: %{default: "plz"}
  end
end
