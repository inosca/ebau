defmodule Ebau.Caluma.Helpers do
  @moduledoc """
  Shared helpers for canton-aware Caluma calculations.
  """

  @doc """
  Resolves the question slugs for the current canton from the given opts.

  Looks up `opts[:question_ids][canton]` when the context contains a `:canton` key,
  falling back to `opts[:question_ids][:default]`. Always returns a list.
  """
  @spec get_question_slugs(keyword(), map() | struct()) :: [binary()]
  def get_question_slugs(opts, context) do
    canton = get_canton(context)

    ids =
      if canton do
        opts[:question_ids][canton] || opts[:question_ids][:default]
      else
        opts[:question_ids][:default]
      end

    ids
    |> convert_to_list()
  end

  @doc """
  Resolves a canton-aware key from a map option.

  Looks up `mapping[canton]` when the context contains a `:canton` key,
  falling back to `mapping[:default]`.
  """
  @spec get_canton_value(map(), map() | struct()) :: term()
  def get_canton_value(mapping, context) do
    canton = get_canton(context)

    if canton do
      mapping[canton] || mapping[:default]
    else
      mapping[:default]
    end
  end

  @doc """
  Resolves a mapping option that may either be a flat answer-value map or a
  canton-aware map of answer-value maps.
  """
  @spec get_answer_mapping(map(), map() | struct()) :: map()
  def get_answer_mapping(mapping, context) when is_map(mapping) do
    if Enum.all?(Map.keys(mapping), &is_binary/1) do
      mapping
    else
      get_canton_value(mapping, context)
    end
  end

  defp get_canton(%{canton: canton}), do: canton
  defp get_canton(%{source_context: %{canton: canton}}), do: canton
  defp get_canton(_context), do: nil

  defp convert_to_list(nil), do: []
  defp convert_to_list(ids) when is_binary(ids), do: [ids]
  defp convert_to_list(ids) when is_list(ids), do: ids
end
