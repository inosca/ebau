defmodule Caluma.Form.AnswerDocument do
  @moduledoc """
  Ash resource for the Caluma answer–document join table (`caluma_form_answerdocument`).

  Links table-question answers to their row documents. Partial clone: only the
  fields needed by the eBau Elixir app are mapped.
  See https://github.com/projectcaluma/caluma for the full upstream model.
  """

  use Ash.Resource,
    otp_app: :ebau,
    domain: Caluma.Form,
    data_layer: AshPostgres.DataLayer,
    authorizers: Ash.Policy.Authorizer

  alias Caluma.Form.Answer
  alias Caluma.Form.Document

  postgres do
    table "caluma_form_answerdocument"
    repo Ebau.Repo
    migrate? false
  end

  policies do
    policy action_type([:create, :update, :destroy]) do
      forbid_if always()
    end

    policy action_type(:read) do
      authorize_if {Ebau.Policies.Checks.HasActiveInstanceACL, via: [:document, :family, :case]}
    end
  end

  actions do
    defaults [:read, :destroy, create: :*, update: :*]
  end

  attributes do
    uuid_primary_key :id

    attribute :sort, :integer do
      default 0
    end
  end

  relationships do
    belongs_to :answer, Answer do
      allow_nil? false
    end

    belongs_to :document, Document do
      allow_nil? false
    end
  end
end
