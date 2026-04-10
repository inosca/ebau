defmodule Caluma.Form.Question do
  @moduledoc false
  use Ash.Resource, domain: Caluma.Form, data_layer: AshPostgres.DataLayer

  alias Caluma.Form.Form

  postgres do
    table "caluma_form_question"
    repo Ebau.Repo
    migrate? false

    references do
      reference :sub_form, on_delete: :delete
    end
  end

  actions do
    defaults [:read]
  end

  attributes do
    attribute :slug, :string do
      public? true
      writable? true
      primary_key? true
      allow_nil? false
      always_select? true
      generated? false
    end

    attribute :type, :atom,
      default: :text,
      allow_nil?: false,
      constraints: [
        one_of: [
          :text,
          :textarea,
          :integer,
          :float,
          :choice,
          :multiple_choice,
          :form,
          :dynamic_choice,
          :dynamic_multiple_choice,
          :action_button,
          :calculated_float
        ]
      ]

    attribute :is_hidden, :string, default: "false", allow_nil?: false

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
