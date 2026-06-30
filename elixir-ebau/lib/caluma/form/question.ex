defmodule Caluma.Form.Question do
  @moduledoc """
  Caluma question resource.

  Questions are globally identified by slug and can be linked into many forms via
  `Caluma.Form.FormQuestion`. This resource exposes a normal create action and an
  explicit compatibility assertion action used by the form-tree builder.
  """
  use Ash.Resource,
    domain: Caluma.Form,
    data_layer: AshPostgres.DataLayer,
    authorizers: Ash.Policy.Authorizer

  alias Caluma.Form.Form
  alias Caluma.Form.Validations.ExistingQuestionMatchesSpec

  postgres do
    table "caluma_form_question"
    repo Ebau.Repo
    migrate? false

    references do
      reference :sub_form, on_delete: :delete
    end
  end

  policies do
    policy action_type([:create, :update, :destroy]) do
      forbid_if always()
    end

    policy action_type(:read) do
      authorize_if never()
    end
  end

  actions do
    defaults [:read]

    create :create_question do
      description """
      Creates a question.

      `is_hidden` is stored as a JEXL expression string, not as a boolean flag.
      """

      accept [:slug, :label, :type, :is_hidden, :configuration, :meta]

      argument :row_form, :map do
        description "Row form relationship input for a `:table` question."
      end

      argument :sub_form, :map do
        description "Sub form relationship input for a `:form` question."
      end

      validate present(:row_form) do
        where attribute_equals(:type, :table)
      end

      validate absent(:row_form) do
        where [negate(attribute_equals(:type, :table))]
        message "row_form can only be set on :table questions"
      end

      validate present(:sub_form) do
        where attribute_equals(:type, :form)
      end

      validate absent(:sub_form) do
        where [negate(attribute_equals(:type, :form))]
        message "sub_form can only be set on :form questions"
      end

      change manage_relationship(:row_form, type: :append)
      change manage_relationship(:sub_form, type: :append)
    end

    action :assert_question_compatible do
      description """
      Asserts that an existing question is compatible with a form-tree occurrence.

      Pure assertion — does not mutate the question. Each provided argument is
      compared against the corresponding question attribute; omitted (or `nil`)
      arguments are skipped.
      """

      argument :question, :struct do
        description "Existing persisted question to check."
        allow_nil? false
        constraints instance_of: __MODULE__
      end

      argument :type, :atom do
        description "Resolved question type that the existing question must match."
        allow_nil? false
      end

      argument :label, Caluma.Form.Types.LocalizedField do
        description "Expected label for the existing question, if provided."
      end

      argument :is_hidden, :string do
        description "Expected `is_hidden` JEXL expression for the existing question, if provided."
      end

      argument :configuration, :map do
        description "Expected configuration for the existing question, if provided."
      end

      argument :meta, :map do
        description "Expected metadata for the existing question, if provided."
      end

      argument :row_form_id, :string do
        description "Expected row form slug for an existing `:table` question."
      end

      argument :sub_form_id, :string do
        description "Expected sub form slug for an existing `:form` question."
      end

      validate {ExistingQuestionMatchesSpec, field: :type}
      validate {ExistingQuestionMatchesSpec, field: :label}
      validate {ExistingQuestionMatchesSpec, field: :is_hidden}
      validate {ExistingQuestionMatchesSpec, field: :configuration}
      validate {ExistingQuestionMatchesSpec, field: :meta}
      validate {ExistingQuestionMatchesSpec, field: :row_form_id}
      validate {ExistingQuestionMatchesSpec, field: :sub_form_id}

      run fn _input, _context -> :ok end
    end
  end

  attributes do
    attribute :slug, :string do
      writable? true
      primary_key? true
      allow_nil? false
      always_select? true
      generated? false
    end

    attribute :type, :atom,
      allow_nil?: false,
      constraints: [
        one_of: [
          :text,
          :textarea,
          :static,
          :integer,
          :float,
          :date,
          :choice,
          :multiple_choice,
          :form,
          :table,
          :dynamic_choice,
          :dynamic_multiple_choice,
          :action_button,
          :calculated_float
        ]
      ]

    attribute :label, Caluma.Form.Types.LocalizedField do
      allow_nil? false
    end

    attribute :is_hidden, :string do
      allow_nil? false
      default "false"
      description "JEXL expression that controls whether the question is hidden."
    end

    attribute :configuration, :map,
      constraints: [
        fields: [
          min_length: [type: :integer, constraints: [min: 0]],
          max_length: [type: :integer, constraints: [min: 0]],
          min_value: [type: :integer],
          max_value: [type: :integer]
        ]
      ],
      default: %{}

    attribute :meta, :map
  end

  relationships do
    many_to_many :forms, Form do
      through Caluma.Form.FormQuestion
      source_attribute_on_join_resource :question_id
      source_attribute :slug
      destination_attribute_on_join_resource :form_id
      destination_attribute :slug
    end

    belongs_to :row_form, Form, destination_attribute: :slug, attribute_type: :string
    belongs_to :sub_form, Form, destination_attribute: :slug, attribute_type: :string

    has_many :answers, Caluma.Form.Answer,
      destination_attribute: :question_id,
      source_attribute: :slug
  end

  identities do
    identity :slug, :slug
  end
end
