defmodule Ebau.MasterData.TypeOfConstruction do
  use Ash.Resource,
    otp_app: :ebau,
    domain: Ebau.MasterData,
    data_layer: AshPostgres.DataLayer,
    extensions: [Caluma.Form.Extensions.Document]

  alias Ebau.Caluma.Calculations.DocumentAnswer

  calculations do
    calculate :art_der_hochbaute, Caluma.Form.Types.AnswerValue,
              {DocumentAnswer, question_ids: %{default: "typ-des-bauwerks"}}

    # TODO: value_mapping from string to integer codes (e.g. "typ-des-bauwerks-einfamilienhaus" -> 6271)
  end
end
