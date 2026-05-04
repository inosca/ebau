defmodule Caluma.Workflow.Extensions.Case do
  @moduledoc """
  Ash extension for resources that are (or relate to) a Caluma case.

  Provides a `caluma_case` DSL section with nested `caluma_document` and
  `meta` subsections for declaring calculations and relationships that
  read from the case's document answers and meta JSON.

  The `caluma_document` subsection reuses the same entity types as
  `Caluma.Form.Extensions.Document` — `answer`, `mapped_answer`,
  `mapped_list_answer`, and `table`.

  ## Usage

  When the resource IS a Caluma case (or has a direct `document` relationship):

      use Ash.Resource,
        extensions: [Caluma.Workflow.Extensions.Case]

      caluma_case do
        caluma_document do
          answer :proposal, :string, question_id: "umschreibung-bauprojekt"
        end

        meta do
          attribute :dossier_number, :string, key: "dossier-number"
        end
      end

  When the resource relates to a case through a relationship:

      caluma_case do
        through :case  # relationship name pointing to the Caluma case

        caluma_document do
          answer :proposal, :string, question_id: "umschreibung-bauprojekt"
        end
      end

  ## The `through` option

  When omitted, the extension assumes the resource itself is (or acts as)
  a Caluma case — answers resolve via `document.answers` and meta via `meta`.

  When specified, it names the relationship that points to the Caluma case.
  Answers then resolve through `<rel>.document.answers` and meta through
  `<rel>.meta`.

  ## The `question_id` and `key` options

  These accept the same forms as `Caluma.Form.Extensions.Document` — a
  plain string, a list of strings, or a `{resolver_module, opts}` tuple.
  See `Caluma.Form.QuestionIdResolver`.

  ## The `mapping` option

  For `mapped_answer` and `mapped_list_answer`, the `mapping` option
  accepts either a flat `%{string => value}` map or a `{resolver_module, opts}`
  tuple for dynamic resolution at query time.
  """

  # -- Case-specific entity --

  defmodule MetaAttribute do
    @moduledoc false
    defstruct [:name, :type, :key, __spark_metadata__: nil]
  end

  # -- Meta entity definition --

  @meta_attribute %Spark.Dsl.Entity{
    name: :attribute,
    describe: "Declares a calculation that reads from the case's meta JSON.",
    target: MetaAttribute,
    schema: [
      name: [type: :atom, required: true, doc: "The calculation name."],
      type: [type: :atom, required: true, doc: "The Ash type for this calculation."],
      key: [
        type: {:or, [:string, :mod_arg]},
        required: true,
        doc:
          "A meta key string or a {resolver_module, opts} tuple. See `Caluma.Form.QuestionIdResolver`."
      ]
    ],
    args: [:name, :type]
  }

  # -- Section definitions --
  # Reuse entity definitions from Document extension

  @caluma_document %Spark.Dsl.Section{
    name: :caluma_document,
    describe: "Declares answers and tables from the case's document.",
    entities: [
      Caluma.Form.Extensions.Document.answer_entity(),
      Caluma.Form.Extensions.Document.mapped_answer_entity(),
      Caluma.Form.Extensions.Document.mapped_list_answer_entity(),
      Caluma.Form.Extensions.Document.table_entity()
    ]
  }

  @meta %Spark.Dsl.Section{
    name: :meta,
    describe: "Declares attributes from the case's meta JSON.",
    entities: [@meta_attribute]
  }

  @caluma_case %Spark.Dsl.Section{
    name: :caluma_case,
    describe: "Declares Caluma case data accessible through a relationship.",
    schema: [
      through: [
        type: :atom,
        doc:
          "The relationship name that points to the Caluma case. When omitted, the resource itself is treated as the case."
      ]
    ],
    sections: [@caluma_document, @meta]
  }

  use Spark.Dsl.Extension,
    sections: [@caluma_case],
    transformers: [Caluma.Workflow.Extensions.Case.Transformer]
end

defmodule Caluma.Workflow.Extensions.Case.Transformer do
  @moduledoc false

  use Spark.Dsl.Transformer

  require Ash.Expr

  alias Caluma.Form.Extensions.Document
  alias Caluma.Workflow.Extensions.Case
  alias Document.AnswerTransformer

  def transform(dsl_state) do
    through = Spark.Dsl.Transformer.get_option(dsl_state, [:caluma_case], :through)

    dsl_state =
      dsl_state
      |> add_document_entities(through)
      |> add_meta_attributes(through)

    {:ok, dsl_state}
  end

  # When `through` is nil, the resource IS the case, so the parent's document FK
  # is `document_id` directly. Otherwise, traverse `<through>.document_id`.
  defp parent_doc_id_ref(nil), do: %Ash.Query.Ref{attribute: :document_id}

  defp parent_doc_id_ref(through),
    do: %Ash.Query.Ref{relationship_path: [through], attribute: :document_id}

  defp answer_relationship_name(name), do: :"_#{name}_answer"

  defp add_answer_relationship(dsl, rel_name, question_id, through) do
    source = Spark.Dsl.Transformer.get_persisted(dsl, :module)
    slugs = AnswerTransformer.all_question_slugs(question_id)

    {:ok, rel} =
      Ash.Resource.Builder.build_relationship(:has_one, rel_name, Caluma.Form.Answer,
        no_attributes?: true
      )

    rel_with_filter = %{
      rel
      | source: source,
        filter: Caluma.Form.AnswerFilters.answer_filter(parent_doc_id_ref(through), slugs)
    }

    Spark.Dsl.Transformer.add_entity(dsl, [:relationships], rel_with_filter)
  end

  defp add_calc(dsl, name, type, mod, opts) do
    {:ok, calc} = Ash.Resource.Builder.build_calculation(name, type, {mod, opts})
    Spark.Dsl.Transformer.add_entity(dsl, [:calculations], calc)
  end

  # -- Entity builders --

  defp add_document_entities(dsl_state, through) do
    source = Spark.Dsl.Transformer.get_persisted(dsl_state, :module)

    dsl_state
    |> Spark.Dsl.Transformer.get_entities([:caluma_case, :caluma_document])
    |> Enum.reduce(dsl_state, fn
      %Document.Answer{} = answer, dsl ->
        rel_name = answer_relationship_name(answer.name)

        dsl
        |> add_answer_relationship(rel_name, answer.question_id, through)
        |> add_calc(answer.name, answer.type, Caluma.Form.Calculations.DocumentAnswer,
          relationship: rel_name
        )

      %Document.MappedAnswer{} = mapped, dsl ->
        rel_name = answer_relationship_name(mapped.name)

        dsl
        |> add_answer_relationship(rel_name, mapped.question_id, through)
        |> add_calc(mapped.name, mapped.type, Caluma.Form.Calculations.MappedDocumentAnswer,
          relationship: rel_name,
          mapping: mapped.mapping
        )

      %Document.MappedListAnswer{} = mapped, dsl ->
        rel_name = answer_relationship_name(mapped.name)

        dsl
        |> add_answer_relationship(rel_name, mapped.question_id, through)
        |> add_calc(
          mapped.name,
          {:array, mapped.type},
          Caluma.Form.Calculations.MappedListDocumentAnswer,
          relationship: rel_name,
          mapping: mapped.mapping
        )

      %Document.Table{} = table, dsl ->
        question_ids = AnswerTransformer.all_question_slugs(table.question_id)

        {:ok, rel} =
          Ash.Resource.Builder.build_relationship(:has_many, table.name, table.resource,
            no_attributes?: true,
            sort: [min_answer_document_sort: :asc]
          )

        rel_with_filter = %{
          rel
          | source: source,
            filter:
              Caluma.Form.AnswerFilters.table_filter(parent_doc_id_ref(through), question_ids)
        }

        Spark.Dsl.Transformer.add_entity(dsl, [:relationships], rel_with_filter)

      _, dsl ->
        dsl
    end)
  end

  defp add_meta_attributes(dsl_state, through) do
    dsl_state
    |> Spark.Dsl.Transformer.get_entities([:caluma_case, :meta])
    |> Enum.filter(&is_struct(&1, Case.MetaAttribute))
    |> Enum.reduce(dsl_state, fn meta, dsl ->
      {:ok, calc} =
        Ash.Resource.Builder.build_calculation(
          meta.name,
          meta.type,
          {Caluma.Workflow.Calculations.CaseMeta, key: meta.key, through: through}
        )

      Spark.Dsl.Transformer.add_entity(dsl, [:calculations], calc)
    end)
  end
end
