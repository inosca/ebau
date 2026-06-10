defmodule Caluma.Form.FormQuestion do
  @moduledoc """
  Join resource between a Caluma form and a Caluma question.

  This resource stores the question order inside a form and follows upstream
  Caluma's natural key behavior for the primary key.
  """
  use Ash.Resource,
    domain: Caluma.Form,
    data_layer: AshPostgres.DataLayer,
    authorizers: Ash.Policy.Authorizer

  alias Caluma.Form.Changes.SetFormQuestionNaturalKey
  alias Caluma.Form.Validations.ExistingFormQuestionMatchesSpec

  postgres do
    table "caluma_form_formquestion"
    repo Ebau.Repo
    migrate? false

    references do
      reference :form, on_delete: :delete
      reference :question, on_delete: :delete
    end
  end

  policies do
    policy action_type([:create, :update, :destroy]) do
      forbid_if always()
    end

    policy action_type(:read) do
      authorize_if always()
    end
  end

  actions do
    defaults [:destroy]

    read :read do
      primary? true
      prepare build(sort: [sort: :desc])
    end

    create :create_form_question do
      description """
      Creates the join row between a form and a question.

      The natural primary key is derived as `\#{form_id}.\#{question_id}` to match
      upstream Caluma's `FormQuestion` behavior.
      """

      accept [:form_id, :question_id, :sort]
      change SetFormQuestionNaturalKey
    end

    action :assert_form_question_compatible do
      description """
      Asserts that an existing form-question join is compatible with a form-tree occurrence.

      Pure assertion — does not mutate the join row.
      """

      argument :form_question, :struct do
        description "Existing persisted form-question join to check."
        allow_nil? false
        constraints instance_of: __MODULE__
      end

      argument :sort, :integer do
        allow_nil? false
      end

      validate {ExistingFormQuestionMatchesSpec, field: :sort}

      run fn _input, _context -> :ok end
    end
  end

  attributes do
    attribute :id, :string do
      allow_nil? false
      writable? true
      primary_key? true
    end

    attribute :sort, :integer do
      allow_nil? false
      default 0
      constraints min: 0
    end
  end

  relationships do
    belongs_to :form, Caluma.Form.Form do
      allow_nil? false
      destination_attribute :slug
      attribute_type :string
    end

    belongs_to :question, Caluma.Form.Question do
      allow_nil? false
      destination_attribute :slug
      attribute_type :string
    end
  end

  identities do
    identity :form_question, [:form_id, :question_id]
  end
end
