defmodule Ebau.MasterData.Extensions.MasterData do
  @moduledoc """
  Spark DSL extension that provides a `master_data` block for declaring
  Instance-level master data fields.

  ## Usage

      use Ash.Resource,
        extensions: [Ebau.MasterData.Extensions.MasterData]

      master_data do
        table :plot_data, Ebau.MasterData.PlotDataRow, question_ids: %{default: "parzellen"}
        answer :proposal, :string, question_ids: %{default: "umschreibung-bauprojekt"}
        mapped_answer :is_paper, :boolean, question_ids: %{default: "is-paper"}, mapping: %{"is-paper-yes" => true, "is-paper-no" => false}
        mapped_list_answer :tags, :string, question_ids: %{default: "tags"}, mapping: %{"tag-a" => "A", "tag-b" => "B"}
        case_meta :dossier_number, :string, keys: %{default: "dossier-number"}
      end
  """

  defmodule Table do
    @moduledoc false
    defstruct [:name, :resource, :question_ids, __spark_metadata__: nil]
  end

  defmodule Answer do
    @moduledoc false
    defstruct [:name, :type, :question_ids, __spark_metadata__: nil]
  end

  defmodule MappedAnswer do
    @moduledoc false
    defstruct [:name, :type, :question_ids, :mapping, __spark_metadata__: nil]
  end

  defmodule MappedListAnswer do
    @moduledoc false
    defstruct [:name, :type, :question_ids, :mapping, __spark_metadata__: nil]
  end

  defmodule CaseMeta do
    @moduledoc false
    defstruct [:name, :type, :keys, __spark_metadata__: nil]
  end

  @table %Spark.Dsl.Entity{
    name: :table,
    describe: "Maps caluma table row documents for the given question slug to an Ash Resource.",
    target: Table,
    schema: [
      name: [
        type: :atom,
        required: true,
        doc: "The relationship name."
      ],
      resource: [
        type: :atom,
        required: true,
        doc: "The target Ash resource module."
      ],
      question_ids: [
        type: {:map, :atom, {:or, [:string, {:list, :string}]}},
        required: true,
        doc: "Caluma question IDs for this table (supports versioned questions)."
      ]
    ],
    args: [:name, :resource]
  }

  @answer %Spark.Dsl.Entity{
    name: :answer,
    describe: "Declares a calculation that reads a Caluma document answer.",
    target: Answer,
    schema: [
      name: [
        type: :atom,
        required: true,
        doc: "The calculation name."
      ],
      type: [
        type: :atom,
        required: true,
        doc: "The Ash type (reserved for documentation; AnswerValue is used)."
      ],
      question_ids: [
        type: {:map, :atom, {:or, [:string, {:list, :string}]}},
        required: true,
        doc: "Map of canton atom to question ID(s). Must include :default."
      ]
    ],
    args: [:name, :type]
  }

  @mapped_answer %Spark.Dsl.Entity{
    name: :mapped_answer,
    describe:
      "Declares a DB-level calculation that reads a scalar Caluma answer and maps its value. Supports filtering and sorting.",
    target: MappedAnswer,
    schema: [
      name: [
        type: :atom,
        required: true,
        doc: "The calculation name."
      ],
      type: [
        type: :atom,
        required: true,
        doc: "The Ash type (reserved for documentation; AnswerValue is used)."
      ],
      question_ids: [
        type: {:map, :atom, {:or, [:string, {:list, :string}]}},
        required: true,
        doc: "Map of canton atom to question ID(s). Must include :default."
      ],
      mapping: [
        type: {:map, :string, {:or, [:string, :boolean]}},
        required: true,
        doc: "Map of scalar answer values to mapped values."
      ]
    ],
    args: [:name, :type]
  }

  @mapped_list_answer %Spark.Dsl.Entity{
    name: :mapped_list_answer,
    describe:
      "Declares an in-memory calculation that reads a list-valued Caluma answer and maps each element. Does not support DB-level filtering or sorting.",
    target: MappedListAnswer,
    schema: [
      name: [
        type: :atom,
        required: true,
        doc: "The calculation name."
      ],
      type: [
        type: :atom,
        required: true,
        doc: "The Ash type (reserved for documentation; AnswerValue is used)."
      ],
      question_ids: [
        type: {:map, :atom, {:or, [:string, {:list, :string}]}},
        required: true,
        doc: "Map of canton atom to question ID(s). Must include :default."
      ],
      mapping: [
        type: {:map, :string, {:or, [:string, :boolean]}},
        required: true,
        doc: "Map of list answer values to mapped values."
      ]
    ],
    args: [:name, :type]
  }

  @case_meta %Spark.Dsl.Entity{
    name: :case_meta,
    describe: "Declares a calculation that reads from case meta JSON.",
    target: CaseMeta,
    schema: [
      name: [
        type: :atom,
        required: true,
        doc: "The calculation name."
      ],
      type: [
        type: :atom,
        required: true,
        doc: "The Ash type for this calculation."
      ],
      keys: [
        type: {:map, :atom, :string},
        required: true,
        doc: "Map of canton atom to meta key. Must include :default."
      ]
    ],
    args: [:name, :type]
  }

  @master_data %Spark.Dsl.Section{
    name: :master_data,
    describe: "Declares master data fields on an Instance resource.",
    entities: [@table, @answer, @mapped_answer, @mapped_list_answer, @case_meta]
  }

  use Spark.Dsl.Extension,
    sections: [@master_data],
    transformers: [Ebau.MasterData.Extensions.MasterData.Transformer]
end

defmodule Ebau.MasterData.Extensions.MasterData.DocumentAnswer do
  @moduledoc """
  Calculation that looks up an answer on the instance's case document.

  Same as `Ebau.Caluma.Calculations.DocumentAnswer` but traverses
  `case.document.answers` instead of `answers`, since this runs on Instance.
  """

  use Ash.Resource.Calculation

  @impl true
  defdelegate init(opts), to: Ebau.Caluma.Calculations.DocumentAnswer

  @impl true
  def expression(opts, context) do
    question_ids = Ebau.Caluma.Helpers.get_question_slugs(opts, context)

    expr(first(case.document.answers, field: :value, filter: expr(question_id in ^question_ids)))
  end
end

defmodule Ebau.MasterData.Extensions.MasterData.MappedDocumentAnswer do
  @moduledoc """
  Calculation that looks up an answer on the instance's case document and maps it to given value.

  Same as `Ebau.MasterData.Extensions.MasterData.DocumentAnswer` but allows mapping of question values.
  """

  use Ash.Resource.Calculation

  @impl true
  defdelegate init(opts), to: Ebau.MasterData.Extensions.MasterData.DocumentAnswer

  @impl true
  def expression(opts, context) do
    question_ids = Ebau.Caluma.Helpers.get_question_slugs(opts, context)
    mapping = opts[:mapping]

    answer_expr =
      expr(
        first(case.document.answers, field: :value, filter: expr(question_id in ^question_ids))
      )

    Enum.reduce(mapping, expr(nil), fn {answer_value, mapped_value}, acc ->
      expr(
        if ^answer_expr == ^answer_value do
          ^mapped_value
        else
          ^acc
        end
      )
    end)
  end
end

defmodule Ebau.MasterData.Extensions.MasterData.MappedListDocumentAnswer do
  @moduledoc """
  In-memory calculation that reads a list-valued Caluma answer and maps each element.

  Use `mapped_list_answer` in the `master_data` DSL for multi-select questions.
  Does not support DB-level filtering or sorting.
  """

  use Ash.Resource.Calculation

  @impl true
  defdelegate init(opts), to: Ebau.MasterData.Extensions.MasterData.DocumentAnswer

  @impl true
  def calculate(records, opts, context) do
    question_ids = Ebau.Caluma.Helpers.get_question_slugs(opts, context)
    mapping = opts[:mapping]

    Enum.map(records, fn record ->
      answer =
        Enum.find(record.case.document.answers, fn a -> a.question_id in question_ids end)

      case answer do
        nil -> nil
        %{value: value} when is_list(value) -> Enum.map(value, &mapping[&1])
        %{value: value} -> [mapping[value]]
      end
    end)
  end
end

defmodule Ebau.MasterData.Extensions.MasterData.Transformer do
  use Spark.Dsl.Transformer

  require Ash.Expr

  def transform(dsl_state) do
    dsl_state =
      dsl_state
      |> add_tables()
      |> add_answers()
      |> add_mapped_answers()
      |> add_mapped_list_answers()
      |> add_case_metas()

    {:ok, dsl_state}
  end

  defp add_tables(dsl_state) do
    dsl_state
    |> Spark.Dsl.Transformer.get_entities([:master_data])
    |> Enum.filter(&is_struct(&1, Ebau.MasterData.Extensions.MasterData.Table))
    |> Enum.reduce(dsl_state, fn table, dsl ->
      question_ids = table.question_ids

      {:ok, rel} =
        Ash.Resource.Builder.build_relationship(:has_many, table.name, table.resource,
          no_attributes?: true
        )

      rel_with_filter = %{
        rel
        | filter:
            Ash.Expr.expr(
              family.id == parent(case.document.id) and
                exists(answer_documents, answer.question_id in ^question_ids)
            )
      }

      Spark.Dsl.Transformer.add_entity(dsl, [:relationships], rel_with_filter)
    end)
  end

  defp add_answers(dsl_state) do
    dsl_state
    |> Spark.Dsl.Transformer.get_entities([:master_data])
    |> Enum.filter(&is_struct(&1, Ebau.MasterData.Extensions.MasterData.Answer))
    |> Enum.reduce(dsl_state, fn answer, dsl ->
      {:ok, calc} =
        Ash.Resource.Builder.build_calculation(
          answer.name,
          Caluma.Form.Types.AnswerValue,
          {Ebau.MasterData.Extensions.MasterData.DocumentAnswer,
           question_ids: answer.question_ids}
        )

      Spark.Dsl.Transformer.add_entity(dsl, [:calculations], calc)
    end)
  end

  defp add_mapped_answers(dsl_state) do
    dsl_state
    |> Spark.Dsl.Transformer.get_entities([:master_data])
    |> Enum.filter(&is_struct(&1, Ebau.MasterData.Extensions.MasterData.MappedAnswer))
    |> Enum.reduce(dsl_state, fn mapped_answer, dsl ->
      {:ok, calc} =
        Ash.Resource.Builder.build_calculation(
          mapped_answer.name,
          Caluma.Form.Types.AnswerValue,
          {Ebau.MasterData.Extensions.MasterData.MappedDocumentAnswer,
           question_ids: mapped_answer.question_ids, mapping: mapped_answer.mapping}
        )

      Spark.Dsl.Transformer.add_entity(dsl, [:calculations], calc)
    end)
  end

  defp add_mapped_list_answers(dsl_state) do
    dsl_state
    |> Spark.Dsl.Transformer.get_entities([:master_data])
    |> Enum.filter(&is_struct(&1, Ebau.MasterData.Extensions.MasterData.MappedListAnswer))
    |> Enum.reduce(dsl_state, fn mapped_list_answer, dsl ->
      {:ok, calc} =
        Ash.Resource.Builder.build_calculation(
          mapped_list_answer.name,
          Caluma.Form.Types.AnswerValue,
          {Ebau.MasterData.Extensions.MasterData.MappedListDocumentAnswer,
           question_ids: mapped_list_answer.question_ids, mapping: mapped_list_answer.mapping}
        )

      Spark.Dsl.Transformer.add_entity(dsl, [:calculations], calc)
    end)
  end

  defp add_case_metas(dsl_state) do
    dsl_state
    |> Spark.Dsl.Transformer.get_entities([:master_data])
    |> Enum.filter(&is_struct(&1, Ebau.MasterData.Extensions.MasterData.CaseMeta))
    |> Enum.reduce(dsl_state, fn meta, dsl ->
      {:ok, calc} =
        Ash.Resource.Builder.build_calculation(
          meta.name,
          meta.type,
          {Ebau.Caluma.Calculations.CaseMeta, keys: meta.keys}
        )

      Spark.Dsl.Transformer.add_entity(dsl, [:calculations], calc)
    end)
  end
end
