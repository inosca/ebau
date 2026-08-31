defmodule Caluma.Form.Changes.SaveDocumentAnswers do
  @moduledoc """
  Writes `caluma_document` answers from action arguments of the same name.
  Only arguments the caller actually passed are written; `nil` clears the
  answer. Values are written as-is.

      update :update do
        argument :proposal, :string
        argument :is_paper, :boolean

        change {Caluma.Form.Changes.SaveDocumentAnswers, answers: [:proposal, :is_paper]}
      end

  The record itself is the document unless `relationship` names the
  relationship to it:

      has_one :document, Caluma.Form.Document, through: [:case, :document]

      change {Caluma.Form.Changes.SaveDocumentAnswers,
              answers: [:proposal], relationship: :document}

  `Caluma.Form.Extensions.Document.Verifier` checks the options at compile time.
  """

  use Ash.Resource.Change

  alias Caluma.Form.Extensions.Document.Info

  @impl true
  def atomic(changeset, opts, context), do: {:ok, change(changeset, opts, context)}

  @impl true
  def change(changeset, opts, context) do
    Ash.Changeset.after_action(changeset, fn changeset, record ->
      document_id = document_id(record, opts[:relationship], scope: context)

      for name <- opts[:answers],
          {:ok, value} <- [Ash.Changeset.fetch_argument(changeset, name)],
          entity <- [Info.entity!(changeset.resource, name)] do
        value =
          case entity do
            %Caluma.Form.Extensions.Document.MappedAnswer{} = entity ->
              entity.mapping
              |> map_answer_values(value)
              |> List.first()

            %Caluma.Form.Extensions.Document.MappedListAnswer{} = entity ->
              # handle mapped list answer
              map_answer_values(entity.mapping, value)

            %Caluma.Form.Extensions.Document.Answer{} = _entity ->
              value
          end

        Caluma.Form.save_answer!(
          document_id,
          Info.question_slug!(changeset.resource, name),
          value,
          scope: context
        )
      end

      {:ok, record}
    end)
  end

  defp map_answer_values(mapping, value) do
    Enum.reduce(mapping, [], fn {key, map_value}, acc ->
      cond do
        is_list(value) and map_value in value ->
          [key | acc]

        map_value == value ->
          [key | acc]

        true ->
          acc
      end
    end)
  end

  defp document_id(record, nil, _opts), do: record.id

  defp document_id(record, relationship, opts) do
    record |> Ash.load!(relationship, opts) |> Map.fetch!(relationship) |> Map.fetch!(:id)
  end
end
