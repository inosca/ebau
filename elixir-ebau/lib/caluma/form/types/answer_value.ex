defmodule Caluma.Form.Types.AnswerValue do
  @moduledoc """
  A custom Ash type for answer values stored as jsonb.

  Accepts any JSON-compatible value: string, integer, float, boolean,
  list, or map. Mirrors Django's `JSONField(null=True, blank=True)`.
  """

  use Ash.Type

  @impl Ash.Type
  def storage_type(_), do: :map

  @impl Ash.Type
  def cast_input(nil, _), do: {:ok, nil}
  def cast_input(value, _), do: {:ok, value}

  @impl Ash.Type
  def cast_stored(nil, _), do: {:ok, nil}
  def cast_stored(value, _), do: {:ok, value}

  @impl Ash.Type
  def dump_to_native(nil, _), do: {:ok, nil}
  def dump_to_native(value, _), do: {:ok, value}
end
