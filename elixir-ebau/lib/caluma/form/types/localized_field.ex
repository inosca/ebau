defmodule Caluma.Form.Types.LocalizedField do
  @moduledoc """
  Ash type for localized Caluma fields stored as maps.

  Accepts either a localization map directly or a plain string, which is
  normalized to `%{"de" => value}` (default locale for this Swiss project).
  """

  use Ash.Type

  @impl Ash.Type
  def storage_type(_), do: :map

  @impl Ash.Type
  def cast_input(nil, _), do: {:ok, nil}
  def cast_input(value, _) when is_map(value), do: {:ok, value}
  # TODO: only de for now
  def cast_input(value, _) when is_binary(value), do: {:ok, %{"de" => value}}
  def cast_input(_, _), do: :error

  @impl Ash.Type
  def cast_stored(nil, _), do: {:ok, nil}
  def cast_stored(value, _) when is_map(value), do: {:ok, value}
  def cast_stored(_, _), do: :error

  @impl Ash.Type
  def dump_to_native(nil, _), do: {:ok, nil}
  def dump_to_native(value, _) when is_map(value), do: {:ok, value}
  def dump_to_native(_, _), do: :error
end
