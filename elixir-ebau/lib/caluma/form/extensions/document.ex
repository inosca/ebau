defmodule Caluma.Form.Extensions.Document do
  @moduledoc """
  Ash extension for resources backed by the `caluma_form_document` table.

  ## What it does

  Adding this extension to an Ash resource does two things:

  1. **Adds base document infrastructure** — a UUID primary key, relationships
     to `answers`, `answer_documents`, and `family`.

  2. **Provides the `caluma_document` DSL** — a declarative way to map Caluma
     question slugs to Ash calculations. Each `answer` you declare becomes a
     calculation that extracts the answer value for the given question ID
     from the document's answers at query time.

  ## Minimal example

  A resource with no answer declarations still gets the base infrastructure:

      defmodule MyApp.SomeDocument do
        use Ash.Resource,
          otp_app: :my_app,
          domain: MyApp.SomeDomain,
          data_layer: AshPostgres.DataLayer,
          extensions: [Caluma.Form.Extensions.Document]

        postgres do
          table "caluma_form_document"
          repo MyApp.Repo
          migrate? false
        end

        actions do
          defaults [:read]
        end
      end

  ## Declaring answers

  Use the `caluma_document` block to declare answers. Each answer maps a
  Caluma question slug to a named Ash calculation on the resource:

      caluma_document do
        answer :plot_number, :string, question_id: "parzellennummer"
        answer :area, :string, question_id: "flaeche"

        mapped_answer :is_paper, :boolean,
          question_id: "is-paper",
          mapping: %{"is-paper-yes" => true, "is-paper-no" => false}

        mapped_list_answer :tags, :string,
          question_id: "tags",
          mapping: %{"tag-a" => "A", "tag-b" => "B"}

        table :plot_data, MyApp.PlotDataRow, question_id: "parzellen"
      end

  ## The `question_id` option

  The `question_id` option on each answer controls how the Caluma question
  slug is determined when the resource is compiled (the resulting filter is
  baked into a `has_one` relationship). It accepts three forms:

  ### Plain string

  Used as-is. Generates a `WHERE question_id = 'slug'` filter.

      answer :name, :string, question_id: "nachname"

  ### List of strings

  Matches any of the given slugs. Useful when a question was renamed and
  both old and new slugs may exist in the database. Generates a
  `WHERE question_id IN ('slug1', 'slug2')` filter.

      answer :name, :string, question_id: ["nachname", "nachname-v2"]

  ### Resolver tuple `{module, opts}`

  For slugs that aren't known statically (different cantons use
  different Caluma question slugs). The module must
  implement `Caluma.Form.Behaviours.SlugResolver`. Resolution happens **at compile
  time**: the `AnswerTransformer` calls `module.resolve(opts)` while the
  resource is compiled and bakes the returned slug(s) into the relationship
  filter (no query context is available).

  Because the slug is frozen into the compiled resource, any config the
  resolver reads (e.g. the canton) must be a compile-time value (see
  `Ebau.Caluma.CantonResolver`), which reads it via `Application.compile_env/2`.

  The resolver must return either a single string or a list of strings.

      answer :name, :string,
        question_id: {Ebau.Caluma.CantonResolver, %{default: "nachname", gr: "familienname"}}

  See `Caluma.Form.Behaviours.SlugResolver` and `Ebau.Caluma.CantonResolver` for how to implement a resolver.

  ## The `mapping` option

  For `mapped_answer` and `mapped_list_answer`, the `mapping` option
  accepts either a flat `%{string => value}` map or a `{resolver_module, opts}`
  tuple for dynamic resolution at query time.

  ## How it works under the hood

  At compile time, two Spark transformers run in order:

  1. `Transformer` — adds the base infrastructure (primary key, relationships,
     aggregates).
  2. `AnswerTransformer` — reads each entity from the `caluma_document`
     section and creates the appropriate Ash calculation or relationship.

  At query time, when an answer calculation is loaded, the
  `Caluma.Form.Calculations.DocumentAnswer` calculation resolves the
  question ID (calling the resolver if one was given) and generates an Ash
  expression that filters the document's answers by question slug and
  returns the first matching value.
  """

  # -- Entity structs --

  defmodule Answer do
    @moduledoc false
    defstruct [:name, :type, :question_id, __spark_metadata__: nil]
  end

  defmodule MappedAnswer do
    @moduledoc false
    defstruct [:name, :type, :question_id, :mapping, __spark_metadata__: nil]
  end

  defmodule MappedListAnswer do
    @moduledoc false
    defstruct [:name, :type, :question_id, :mapping, __spark_metadata__: nil]
  end

  defmodule Table do
    @moduledoc false
    defstruct [:name, :resource, :question_id, __spark_metadata__: nil]
  end

  # -- Shared schema types --

  @question_id_type {:or, [:string, {:list, :string}, :mod_arg]}
  @question_id_doc "A question ID string, a list of question ID strings, or a {resolver_module, opts} tuple. See `Caluma.Form.Behaviours.SlugResolver`."

  @mapping_type {:or,
                 [
                   {:map, :string, {:or, [:string, :boolean, :integer, :float]}},
                   :mod_arg
                 ]}

  # -- Entity definitions --

  @answer %Spark.Dsl.Entity{
    name: :answer,
    describe: "Declares a calculation that reads a Caluma document answer.",
    target: Answer,
    schema: [
      name: [type: :atom, required: true, doc: "The calculation name."],
      type: [type: :atom, required: true, doc: "The Ash type returned by the calculation."],
      question_id: [type: @question_id_type, required: true, doc: @question_id_doc]
    ],
    args: [:name, :type]
  }

  @mapped_answer %Spark.Dsl.Entity{
    name: :mapped_answer,
    describe:
      "Declares a DB-level calculation that reads a scalar Caluma answer and maps its value.",
    target: MappedAnswer,
    schema: [
      name: [type: :atom, required: true, doc: "The calculation name."],
      type: [type: :atom, required: true, doc: "The Ash type returned by the calculation."],
      question_id: [type: @question_id_type, required: true, doc: @question_id_doc],
      mapping: [
        type: @mapping_type,
        required: true,
        doc:
          "Map of answer values to mapped values, or a {resolver_module, opts} tuple for dynamic resolution."
      ]
    ],
    args: [:name, :type]
  }

  @mapped_list_answer %Spark.Dsl.Entity{
    name: :mapped_list_answer,
    describe:
      "Declares an in-memory calculation that reads a list-valued Caluma answer and maps each element.",
    target: MappedListAnswer,
    schema: [
      name: [type: :atom, required: true, doc: "The calculation name."],
      type: [
        type: :atom,
        required: true,
        doc: "The Ash element type returned by the calculation."
      ],
      question_id: [type: @question_id_type, required: true, doc: @question_id_doc],
      mapping: [
        type: @mapping_type,
        required: true,
        doc:
          "Map of answer values to mapped values, or a {resolver_module, opts} tuple for dynamic resolution."
      ]
    ],
    args: [:name, :type]
  }

  @table %Spark.Dsl.Entity{
    name: :table,
    describe: "Maps Caluma table row documents to an Ash resource relationship.",
    target: Table,
    schema: [
      name: [type: :atom, required: true, doc: "The relationship name."],
      resource: [type: :atom, required: true, doc: "The target Ash resource module."],
      question_id: [type: @question_id_type, required: true, doc: @question_id_doc]
    ],
    args: [:name, :resource]
  }

  # -- Public accessors for reuse by other extensions (e.g. Case) --

  def answer_entity, do: @answer
  def mapped_answer_entity, do: @mapped_answer
  def mapped_list_answer_entity, do: @mapped_list_answer
  def table_entity, do: @table

  # -- Section definition --

  @caluma_document %Spark.Dsl.Section{
    name: :caluma_document,
    describe: "Declares answers backed by Caluma document questions.",
    entities: [@answer, @mapped_answer, @mapped_list_answer, @table]
  }

  use Spark.Dsl.Extension,
    sections: [@caluma_document],
    transformers: [
      Caluma.Form.Extensions.Document.Transformer,
      Caluma.Form.Extensions.Document.AnswerTransformer
    ],
    verifiers: [Caluma.Form.Extensions.Document.Verifier]
end
