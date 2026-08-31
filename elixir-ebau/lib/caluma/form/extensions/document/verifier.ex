defmodule Caluma.Form.Extensions.Document.Verifier do
  @moduledoc false

  use Spark.Dsl.Verifier

  alias Caluma.Form.Changes.SaveDocumentAnswers

  def verify(dsl_state) do
    verify_save_document_answers(
      dsl_state,
      Spark.Dsl.Verifier.get_entities(dsl_state, [:caluma_document])
    )
  end

  @doc """
  Every name passed to `SaveDocumentAnswers` must be one of the given
  `caluma_document` entities and an argument of the action, otherwise the
  change would silently write nothing. Shared with extensions that declare the
  entities elsewhere (e.g. `Caluma.Workflow.Extensions.Case`).
  """
  def verify_save_document_answers(dsl_state, entities) do
    case unknown_answers(dsl_state, entities) do
      [] ->
        :ok

      unknown ->
        {:error,
         Spark.Error.DslError.exception(
           module: Spark.Dsl.Verifier.get_persisted(dsl_state, :module),
           path: [:actions],
           message: message(unknown)
         )}
    end
  end

  defp unknown_answers(dsl_state, entities) do
    entity_names = Enum.map(entities, & &1.name)

    dsl_state
    |> Ash.Resource.Info.actions()
    |> Enum.flat_map(fn action ->
      arguments = Enum.map(action.arguments, & &1.name)

      for %{change: {SaveDocumentAnswers, opts}} <- Map.get(action, :changes, []),
          name <- opts[:answers],
          name not in entity_names or name not in arguments,
          do: {action, name}
    end)
  end

  defp message(unknown) do
    unknown
    |> Enum.group_by(fn {action, _name} -> {action.type, action.name} end, &elem(&1, 1))
    |> Enum.map_join("\n\n", fn {{type, action}, [first | _] = names} ->
      """
      action #{inspect(action)}: #{inspect(names)} must be declared both as a \
      caluma_document answer and as an argument of the action, for example:

          caluma_document do
            answer #{inspect(first)}, :string, question_id: "#{first}"
          end

          #{type} #{inspect(action)} do
            argument #{inspect(first)}, :string

            change {#{inspect(SaveDocumentAnswers)}, answers: [#{inspect(first)}]}
          end
      """
    end)
  end
end
