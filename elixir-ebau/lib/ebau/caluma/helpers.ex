defmodule Ebau.Caluma.Helpers do
  @moduledoc """
  Shared helpers for canton-aware Caluma calculations.
  """

  @doc """
  Resolves the question slugs for the current canton from the given opts.

  Looks up `opts[:question_ids][canton]` when the context contains a `:canton` key,
  falling back to `opts[:question_ids][:default]`. Always returns a list.
  """
  @spec get_question_slugs(keyword(), map()) :: [binary()]
  def get_question_slugs(opts, %{canton: canton} = _context) do
    (opts[:question_ids][canton] || opts[:question_ids][:default])
    |> convert_to_list()
  end

  def get_question_slugs(opts, _context) do
    opts[:question_ids][:default]
    |> convert_to_list()
  end

  @doc """
  Resolves a canton-aware key from a map option.

  Looks up `mapping[canton]` when the context contains a `:canton` key,
  falling back to `mapping[:default]`.
  """
  @spec get_canton_value(map(), map()) :: term()
  def get_canton_value(mapping, %{canton: canton}), do: mapping[canton] || mapping[:default]
  def get_canton_value(mapping, _context), do: mapping[:default]

  defp convert_to_list(ids) when is_binary(ids), do: [ids]
  defp convert_to_list(ids), do: ids
end
