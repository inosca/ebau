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
    policy action_type([:create, :destroy]) do
      forbid_if always()
    end

    policy action_type([:read, :update]) do
      authorize_if {Ebau.Policies.Checks.HasActiveInstanceACL,
                    via: [:document, :family, :case, :instance]}
    end
  end

  actions do
    defaults [:read, :destroy, create: :*, update: :*]

    read :by_answer do
      argument :answer_id, :uuid, allow_nil?: false
      filter expr(answer_id == ^arg(:answer_id))
    end

    create :prepend do
      description "Links a row document at sort 0, shifting the answer's existing rows up."

      change before_action(fn changeset, context ->
               Caluma.Form.AnswerDocument
               |> Ash.Query.for_read(
                 :by_answer,
                 %{answer_id: Ash.Changeset.get_attribute(changeset, :answer_id)},
                 scope: context
               )
               |> Ash.bulk_update!(:shift_sort_up, %{}, scope: context)

               changeset
             end)
    end

    update :shift_sort_up do
      change atomic_update(:sort, expr(sort + 1))
    end
  end

  attributes do
    uuid_primary_key :id

    attribute :sort, :integer do
      allow_nil? false
      default 0
      constraints min: 0
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

  identities do
    identity :answer_document, [:answer_id, :document_id]
  end
end
