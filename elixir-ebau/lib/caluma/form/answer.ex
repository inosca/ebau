defmodule Caluma.Form.Answer do
  @moduledoc """
  Ash resource for a Caluma form answer (`caluma_form_answer`).

  Partial clone: only the fields needed by the eBau Elixir app are mapped.
  See https://github.com/projectcaluma/caluma for the full upstream model.
  """

  use Ash.Resource,
    otp_app: :ebau,
    domain: Caluma.Form,
    data_layer: AshPostgres.DataLayer,
    authorizers: Ash.Policy.Authorizer

  postgres do
    repo Ebau.Repo
    table "caluma_form_answer"
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

    attribute :value, Caluma.Form.Types.AnswerValue do
      public? true
    end
  end

  calculations do
    # The `value` column is jsonb. Casting jsonb directly to text yields the
    # JSON-encoded form (a string `"foo"` becomes the literal `"foo"` with
    # quotes). Use the `#>> '{}'` operator to extract the root jsonb scalar
    # as plain text. Typed variants then cast to the desired primitive.
    calculate :value_string, :string, expr(fragment("(? #>> '{}')", value))
    calculate :value_integer, :integer, expr(fragment("(? #>> '{}')::integer", value))
    calculate :value_float, :float, expr(fragment("(? #>> '{}')::double precision", value))
    calculate :value_boolean, :boolean, expr(fragment("(? #>> '{}')::boolean", value))
  end

  aggregates do
    max :max_sort, :answer_documents, :sort
  end

  relationships do
    belongs_to :document, Caluma.Form.Document do
      public? true
      allow_nil? false
    end

    belongs_to :question, Caluma.Form.Question do
      public? true
      allow_nil? false
      attribute_type :string
      destination_attribute :slug
    end

    has_many :answer_documents, Caluma.Form.AnswerDocument

    many_to_many :documents, Caluma.Form.Document do
      through Caluma.Form.AnswerDocument
    end
  end

  identities do
    identity :document_question, [:document_id, :question_id]
  end
end
