defmodule Ebau.MasterData.TypeOfConstruction do
  use Ash.Resource,
    otp_app: :ebau,
    domain: Ebau.MasterData,
    data_layer: AshPostgres.DataLayer,
    extensions: [Caluma.Form.Extensions.Document, Ebau.Caluma.Extensions.DocumentBacked]

  caluma_document do
    field :art_der_hochbaute, :string, question_ids: %{default: "typ-des-bauwerks"}

    # TODO: value_mapping from string to integer codes (e.g. "typ-des-bauwerks-einfamilienhaus" -> 6271)
  end
end
