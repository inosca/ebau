defmodule Caluma.Form.Extensions.Document do
  @moduledoc """
  Ash extension for resources backed by the `caluma_form_document` table.

  ## What it does

  Adding this extension to an Ash resource does two things:

  1. **Adds base document infrastructure** — a UUID primary key, relationships
     to `answers`, `answer_documents`, and `family`, an aggregate, and a
     default `:read` action (skipped if one already exists).

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
  slug is determined at query time. It accepts three forms:

  ### Plain string

  Used as-is. Generates a `WHERE question_id = 'slug'` filter.

      answer :name, :string, question_id: "nachname"

  ### List of strings

  Matches any of the given slugs. Useful when a question was renamed and
  both old and new slugs may exist in the database. Generates a
  `WHERE question_id IN ('slug1', 'slug2')` filter.

      answer :name, :string, question_id: ["nachname", "nachname-v2"]

  ### Resolver tuple `{module, opts}`

  For dynamic resolution at query time. The module must implement
  `Caluma.Form.QuestionIdResolver`. At query time, `module.resolve(opts, context)`
  is called where `context` is the Ash calculation context (containing the
  actor, tenant, and any custom context set via `Ash.Context`).

  The resolver must return either a single string or a list of strings.

      answer :name, :string,
        question_id: {MyApp.TenantResolver, %{default: "nachname", tenant_a: "full-name"}}

  See `Caluma.Form.QuestionIdResolver` for how to implement a resolver.

  ## The `mapping` option

  For `mapped_answer` and `mapped_list_answer`, the `mapping` option
  accepts either a flat `%{string => value}` map or a `{resolver_module, opts}`
  tuple for dynamic resolution at query time.

  ## How it works under the hood

  At compile time, two Spark transformers run in order:

  1. `Transformer` — adds the base infrastructure (primary key, relationships,
     aggregates, read action).
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
  @question_id_doc "A question ID string, a list of question ID strings, or a {resolver_module, opts} tuple. See `Caluma.Form.QuestionIdResolver`."

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
    ]
end

defmodule Caluma.Form.Extensions.Document.Transformer do
  @moduledoc false

  use Spark.Dsl.Transformer

  def before?(Caluma.Form.Extensions.Document.AnswerTransformer), do: true
  def before?(_), do: false

  def transform(dsl_state) do
    {:ok, dsl_state} = maybe_add_action(dsl_state)
    {:ok, dsl_state} = add_attribute(dsl_state)
    {:ok, dsl_state} = add_aggregates(dsl_state)
    {:ok, dsl_state} = add_relationships(dsl_state)

    {:ok, dsl_state}
  end

  defp maybe_add_action(dsl_state) do
    existing_actions = Spark.Dsl.Transformer.get_entities(dsl_state, [:actions])
    has_read? = Enum.any?(existing_actions, &(&1.name == :read && &1.type == :read))

    if has_read? do
      {:ok, dsl_state}
    else
      {:ok, action} =
        Spark.Dsl.Transformer.build_entity(Ash.Resource.Dsl, [:actions], :read,
          name: :read,
          primary?: true
        )

      {:ok, Spark.Dsl.Transformer.add_entity(dsl_state, [:actions], action)}
    end
  end

  defp add_attribute(dsl_state) do
    {:ok, attr} =
      Spark.Dsl.Transformer.build_entity(Ash.Resource.Dsl, [:attributes], :uuid_primary_key,
        name: :id
      )

    {:ok, Spark.Dsl.Transformer.add_entity(dsl_state, [:attributes], attr)}
  end

  defp add_aggregates(dsl_state) do
    {:ok, agg} =
      Ash.Resource.Builder.build_aggregate(
        :sort,
        :min,
        :answer_documents,
        field: :sort
      )

    {:ok, Spark.Dsl.Transformer.add_entity(dsl_state, [:aggregates], agg)}
  end

  defp add_relationships(dsl_state) do
    {:ok, answers} =
      Ash.Resource.Builder.build_relationship(:has_many, :answers, Caluma.Form.Answer,
        destination_attribute: :document_id
      )

    {:ok, answer_documents} =
      Ash.Resource.Builder.build_relationship(
        :has_many,
        :answer_documents,
        Caluma.Form.AnswerDocument,
        destination_attribute: :document_id
      )

    {:ok, family} =
      Ash.Resource.Builder.build_relationship(:belongs_to, :family, Caluma.Form.Document, [])

    dsl_state =
      dsl_state
      |> Spark.Dsl.Transformer.add_entity([:relationships], answers)
      |> Spark.Dsl.Transformer.add_entity([:relationships], answer_documents)
      |> Spark.Dsl.Transformer.add_entity([:relationships], family)

    {:ok, dsl_state}
  end
end

defmodule Caluma.Form.Extensions.Document.AnswerTransformer do
  @moduledoc false

  use Spark.Dsl.Transformer

  require Ash.Expr

  alias Caluma.Form.Extensions.Document

  def transform(dsl_state) do
    source = Spark.Dsl.Transformer.get_persisted(dsl_state, :module)
    entities = Spark.Dsl.Transformer.get_entities(dsl_state, [:caluma_document])

    dsl_state =
      entities
      |> Enum.reduce(dsl_state, fn
        %Document.Answer{} = answer, dsl ->
          add_answer_calc(dsl, answer)

        %Document.MappedAnswer{} = mapped, dsl ->
          add_mapped_answer_calc(dsl, mapped)

        %Document.MappedListAnswer{} = mapped, dsl ->
          add_mapped_list_answer_calc(dsl, mapped)

        %Document.Table{} = table, dsl ->
          add_table_relationship(dsl, table, source)

        _, dsl ->
          dsl
      end)

    {:ok, dsl_state}
  end

  defp add_answer_calc(dsl, answer) do
    rel_name = answer_relationship_name(answer.name)

    dsl
    |> add_answer_relationship(rel_name, answer.question_id)
    |> add_calc(answer.name, answer.type, Caluma.Form.Calculations.DocumentAnswer,
      relationship: rel_name
    )
  end

  defp add_mapped_answer_calc(dsl, mapped) do
    rel_name = answer_relationship_name(mapped.name)

    dsl
    |> add_answer_relationship(rel_name, mapped.question_id)
    |> add_calc(mapped.name, mapped.type, Caluma.Form.Calculations.MappedDocumentAnswer,
      relationship: rel_name,
      mapping: mapped.mapping
    )
  end

  defp add_mapped_list_answer_calc(dsl, mapped) do
    rel_name = answer_relationship_name(mapped.name)

    dsl
    |> add_answer_relationship(rel_name, mapped.question_id)
    |> add_calc(
      mapped.name,
      {:array, mapped.type},
      Caluma.Form.Calculations.MappedListDocumentAnswer,
      relationship: rel_name,
      mapping: mapped.mapping
    )
  end

  def add_calc(dsl, name, type, mod, opts) do
    {:ok, calc} = Ash.Resource.Builder.build_calculation(name, type, {mod, opts})
    Spark.Dsl.Transformer.add_entity(dsl, [:calculations], calc)
  end

  # The resource IS the document, so the parent's primary key is `id`.
  @parent_doc_id_ref %Ash.Query.Ref{attribute: :id}

  def answer_relationship_name(name), do: :"_#{name}_answer"

  @doc false
  def add_answer_relationship(dsl, rel_name, question_id, parent_doc_id_ref) do
    source = Spark.Dsl.Transformer.get_persisted(dsl, :module)
    slugs = all_question_slugs(question_id)

    {:ok, rel} =
      Ash.Resource.Builder.build_relationship(:has_one, rel_name, Caluma.Form.Answer,
        no_attributes?: true
      )

    rel_with_filter = %{
      rel
      | source: source,
        filter: Caluma.Form.AnswerFilters.answer_filter(parent_doc_id_ref, slugs)
    }

    Spark.Dsl.Transformer.add_entity(dsl, [:relationships], rel_with_filter)
  end

  defp add_answer_relationship(dsl, rel_name, question_id) do
    add_answer_relationship(dsl, rel_name, question_id, @parent_doc_id_ref)
  end

  @doc false
  def add_table_relationship(dsl, table, source, parent_doc_id_ref) do
    question_ids = all_question_slugs(table.question_id)

    {:ok, rel} =
      Ash.Resource.Builder.build_relationship(:has_many, table.name, table.resource,
        no_attributes?: true,
        sort: [sort: :desc]
      )

    rel_with_filter = %{
      rel
      | source: source,
        filter: Caluma.Form.AnswerFilters.table_filter(parent_doc_id_ref, question_ids)
    }

    Spark.Dsl.Transformer.add_entity(dsl, [:relationships], rel_with_filter)
  end

  defp add_table_relationship(dsl, table, source) do
    add_table_relationship(dsl, table, source, @parent_doc_id_ref)
  end

  @doc false
  def all_question_slugs(id) when is_binary(id), do: [id]
  def all_question_slugs(ids) when is_list(ids), do: Enum.uniq(ids)
  def all_question_slugs({mod, opts}), do: {mod, opts}
end
