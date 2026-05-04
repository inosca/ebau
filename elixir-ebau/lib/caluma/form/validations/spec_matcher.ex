defmodule Caluma.Form.Validations.SpecMatcher do
  @moduledoc false

  alias Caluma.Form.Types.LocalizedFieldHelpers

  @doc """
  Compares `value` against `record`'s `field`. Localized fields (passed via
  `localized?: true`) compare only locales present in `value`; plain fields
  use `==`. Returns `:ok` or `{:mismatch, actual, expected_for_message}`.

  The expected-for-message value is what the caller should display in error
  messages — for localized comparisons it's the normalized map, otherwise
  the raw value.
  """
  @spec compare(map, atom, term, keyword) :: :ok | {:mismatch, term, term}
  def compare(record, field, value, opts \\ []) do
    actual = Map.fetch!(record, field)

    if Keyword.get(opts, :localized?, false) do
      expected = LocalizedFieldHelpers.normalize(value)

      if LocalizedFieldHelpers.matches?(actual, expected),
        do: :ok,
        else: {:mismatch, actual, expected}
    else
      if actual == value,
        do: :ok,
        else: {:mismatch, actual, value}
    end
  end
end
