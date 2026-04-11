defmodule Caluma.Form.Form do
  @moduledoc """
  Caluma form resource.

  This resource represents persisted Caluma forms and exposes a declarative
  form-tree creation action that can build nested form/question structures.
  """
  use Ash.Resource, domain: Caluma.Form, data_layer: AshPostgres.DataLayer

  alias Caluma.Form.Changes.SyncFormTree
  alias Caluma.Form.Validations.ExistingFormMatchesSpec

  postgres do
    table "caluma_form_form"
    repo Ebau.Repo
    migrate? false
  end

  actions do
    defaults [:read]

    create :create_form do
      description "Low-level create action for persisted Caluma forms."
      accept :*
    end

    create :create_form_tree do
      description """
      Creates a form together with an ordered nested question tree.

      Nested question specs are materialized as `Question` and `FormQuestion`
      records, and the question order defines the `FormQuestion.sort` values.
      This is the main entry point for building small declarative Caluma form trees
      in tests.

      Example:

          Caluma.Form.create_form_tree!(%{
            slug: "baugesuch",
            name: "Baugesuch",
            questions: [
              %{
                slug: "parzellen",
                label: "Parzellen",
                type: :table,
                form: %{name: "Parzellen"},
                questions: [
                  %{slug: "lagekoordinaten-nord", label: "Lagekoordinaten Nord", type: :float},
                  %{slug: "lagekoordinaten-ost", label: "Lagekoordinaten Ost", type: :float}
                ]
              },
              %{
                slug: "parzellen-2",
                label: "Parzellen 2",
                type: :table,
                form: %{name: "Parzellen 2"},
                questions: [
                  %{slug: "lagekoordinaten-nord"},
                  %{slug: "lagekoordinaten-ost"}
                ]
              }
            ]
          })
      """

      accept [:slug, :name, :meta]

      argument :questions, {:array, :map} do
        description "Ordered nested question specs to attach to the form."
        allow_nil? false
        default []
      end

      change SyncFormTree
    end

    update :apply_form_tree do
      description """
      Applies a form tree to an existing form.

      The existing form itself must match the provided root attributes. Missing
      nested descendants are created, while existing descendants are checked for
      compatibility.
      """

      require_atomic? false
      accept []

      argument :form_spec, :map do
        description "Raw nested form spec from a declarative form tree."
        allow_nil? false
      end

      validate ExistingFormMatchesSpec
      change SyncFormTree
    end
  end

  attributes do
    attribute :slug, :string do
      allow_nil? false
      writable? true
      primary_key? true
      generated? false
      public? true
    end

    attribute :name, Caluma.Form.Types.LocalizedField do
      public? true
      allow_nil? false
    end

    attribute :is_published?, :boolean do
      source :is_published
      public? true
    end

    attribute :is_archived?, :boolean do
      source :is_archived
      public? true
    end

    attribute :meta, :map do
      public? true
      default %{}
    end
  end

  relationships do
    has_many :documents, Caluma.Form.Document do
      source_attribute :slug
      destination_attribute :form_id
    end

    many_to_many :questions, Caluma.Form.Question do
      through Caluma.Form.FormQuestion
      source_attribute :slug
      source_attribute_on_join_resource :form_id
      destination_attribute :slug
      destination_attribute_on_join_resource :question_id
    end

    has_many :form_questions, Caluma.Form.FormQuestion do
      source_attribute :slug
    end
  end
end
