defmodule Caluma.Form.Validations.SpecMatcher do
  @moduledoc false

  alias Caluma.Form.Types.LocalizedFieldHelpers

  # Caluma fields stored as `LocalizedField` maps — comparison only checks
  # the locales present in the expected value.
  @localized_fields ~w(label name)a

  @doc """
  Compares `value` against `record`'s `field`. Returns `:ok` or
  `{:mismatch, actual, expected_for_message}`. For fields known to hold a
  localized value, only the locales present in `value` are compared.

  The expected-for-message value is what the caller should display in error
  messages — for localized comparisons it's the normalized map, otherwise
  the raw value.
  """
  @spec compare(map, atom, term) :: :ok | {:mismatch, term, term}
  def compare(record, field, value) when field in @localized_fields do
    actual = Map.fetch!(record, field)
    expected = LocalizedFieldHelpers.normalize(value)

    if LocalizedFieldHelpers.matches?(actual, expected),
      do: :ok,
      else: {:mismatch, actual, expected}
  end

  def compare(record, field, value) do
    actual = Map.fetch!(record, field)

    if actual == value,
      do: :ok,
      else: {:mismatch, actual, value}
  end
end
