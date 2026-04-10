defmodule Ebau.MasterData.PlotDataRow do
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
