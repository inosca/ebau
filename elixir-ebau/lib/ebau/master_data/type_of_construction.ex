defmodule Ebau.MasterData.TypeOfConstruction do
  @moduledoc """
  Building type classification (Gebaeude/Art der Hochbaute) extracted from
  a Caluma table question.

  Each row corresponds to one row document under the `gebaeude` table
  question. The raw answer is a choice slug like
  `typ-des-bauwerks-einfamilienhaus` that maps to a numeric BFS code.

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
    field :art_der_hochbaute, :string, question_ids: %{default: "typ-des-bauwerks"}

    # TODO: value_mapping from string to integer codes (e.g. "typ-des-bauwerks-einfamilienhaus" -> 6271)
  end
end
