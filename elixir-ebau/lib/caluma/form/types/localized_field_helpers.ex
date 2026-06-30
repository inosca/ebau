defmodule Caluma.Form.Types.LocalizedFieldHelpers do
  @moduledoc false

  alias Caluma.Form.Types.LocalizedField

  @doc """
  Normalizes a value through `LocalizedField.cast_input/2`, returning the
  original value on cast failure.
  """
  def normalize(value) do
    case LocalizedField.cast_input(value, []) do
      {:ok, normalized_value} -> normalized_value
      :error -> value
    end
  end

  @doc """
  Checks whether `actual` matches `expected`, comparing only the locales
  present in `expected` when both are maps.
  """
  def matches?(actual, expected) when is_map(actual) and is_map(expected) do
    Enum.all?(expected, fn {locale, value} -> Map.get(actual, locale) == value end)
  end

  def matches?(actual, expected), do: actual == expected
end
