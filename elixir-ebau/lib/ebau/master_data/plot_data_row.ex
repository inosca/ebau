defmodule Ebau.MasterData.PlotDataRow do
  use Ash.Resource,
    otp_app: :ebau,
    domain: Ebau.MasterData,
    data_layer: AshPostgres.DataLayer,
    extensions: [Caluma.Form.Extensions.Document]

  alias Ebau.Caluma.Calculations.DocumentAnswer

  calculations do
    calculate :plot_number,
              Caluma.Form.Types.AnswerValue,
              {DocumentAnswer, question_ids: %{default: "parzellennummer", gr: "parzellennummer"}}

    calculate :egrid_number,
              Caluma.Form.Types.AnswerValue,
              {DocumentAnswer, question_ids: %{default: "e-grid", gr: "e-grid"}}

    calculate :coord_east,
              Caluma.Form.Types.AnswerValue,
              {DocumentAnswer,
               question_ids: %{default: "lagekoordinaten-ost", gr: "coordinates-east"}}

    calculate :coord_north,
              Caluma.Form.Types.AnswerValue,
              {DocumentAnswer,
               question_ids: %{default: "lagekoordinaten-nord", gr: "coordinates-north"}}

    calculate :zip,
              Caluma.Form.Types.AnswerValue,
              {DocumentAnswer, question_ids: %{default: "plz", gr: "plz"}}
  end
end
