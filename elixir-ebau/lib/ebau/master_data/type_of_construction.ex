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
    authorizers: Ash.Policy.Authorizer,
    extensions: [Caluma.Form.Extensions.Document]

  postgres do
    table "caluma_form_document"
    repo Ebau.Repo
    migrate? false
  end

  policies do
    policy action_type(:read) do
      authorize_if accessing_from(Ebau.Instances.Instance, :type_of_construction)
    end
  end

  caluma_document do
    answer :art_der_hochbaute, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "typ-des-bauwerks"}}
  end
end
