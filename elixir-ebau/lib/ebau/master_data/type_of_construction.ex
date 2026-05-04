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
    policy action_type([:create, :update, :destroy]) do
      forbid_if always()
    end

    policy action_type(:read) do
      authorize_if {Ebau.Policies.Checks.HasActiveInstanceACL, via: [:family, :case]}
    end
  end

  caluma_document do
    answer :art_der_hochbaute, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "typ-des-bauwerks"}}

    # TODO: value_mapping from string to integer codes (e.g. "typ-des-bauwerks-einfamilienhaus" -> 6271)
  end
end
