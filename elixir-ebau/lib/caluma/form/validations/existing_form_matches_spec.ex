defmodule Caluma.Form.Validations.ExistingFormMatchesSpec do
  @moduledoc """
  Validates that one attribute on the existing form matches the corresponding
  action argument.

  Used by `Caluma.Form.apply_form_tree`. Apply once per field via the `field:`
  option. A `nil` argument is treated as "no expectation" and skipped.

  For the localized `:name` field, comparison considers only locales present
  in the provided value.
  """

  use Ash.Resource.Validation

  alias Caluma.Form.Validations.SpecMatcher

  @impl true
  def init(opts), do: SpecMatcher.init(opts)

  @impl true
  def validate(changeset, opts, _context) do
    SpecMatcher.validate_changeset(changeset, opts, &"form #{inspect(&1.slug)}")
  end
end
