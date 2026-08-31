defmodule Caluma.Form.Extensions.Document.Info do
  @moduledoc """
  Introspection for `caluma_document` declarations. Works on a resource module
  or, inside transformers and verifiers, on the DSL state.

      Info.caluma_document(MyApp.Plot)          # all entities
      Info.entity!(MyApp.Plot, :plot_number)    # the entity struct
      Info.question_slug!(MyApp.Plot, :plots)   # "parzellen"
  """

  use Spark.InfoGenerator,
    extension: Caluma.Form.Extensions.Document,
    sections: [:caluma_document]

  alias Caluma.Form.QuestionId

  @doc """
  The `caluma_document` entities — at the top level for a document resource,
  nested under `caluma_case` for a `Caluma.Workflow.Extensions.Case` resource.
  """
  def caluma_document(dsl_or_resource) do
    case Spark.Dsl.Extension.get_entities(dsl_or_resource, [:caluma_case, :caluma_document]) do
      [] -> Spark.Dsl.Extension.get_entities(dsl_or_resource, [:caluma_document])
      entities -> entities
    end
  end

  @doc "The entity declared under `name`."
  @spec entity(module() | map(), atom()) :: {:ok, struct()} | :error
  def entity(dsl_or_resource, name) do
    dsl_or_resource
    |> caluma_document()
    |> Enum.find(&(&1.name == name))
    |> case do
      nil -> :error
      entity -> {:ok, entity}
    end
  end

  @doc "Same as `entity/2`, raises when there is no such entity."
  @spec entity!(module() | map(), atom()) :: struct()
  def entity!(dsl_or_resource, name) do
    case entity(dsl_or_resource, name) do
      {:ok, entity} ->
        entity

      :error ->
        raise ArgumentError,
              "no caluma_document entity #{inspect(name)} on #{inspect(module(dsl_or_resource))}"
    end
  end

  @doc "The Caluma question slug written for the entity `name`."
  @spec question_slug(module() | map(), atom()) :: {:ok, String.t()} | :error
  def question_slug(dsl_or_resource, name) do
    with {:ok, entity} <- entity(dsl_or_resource, name) do
      {:ok, QuestionId.slug(entity.question_id)}
    end
  end

  @doc "Same as `question_slug/2`, raises when there is no such entity."
  @spec question_slug!(module() | map(), atom()) :: String.t()
  def question_slug!(dsl_or_resource, name) do
    dsl_or_resource |> entity!(name) |> Map.fetch!(:question_id) |> QuestionId.slug()
  end

  defp module(resource) when is_atom(resource), do: resource
  defp module(dsl_state), do: Spark.Dsl.Extension.get_persisted(dsl_state, :module)
end
