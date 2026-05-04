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

  alias Ash.Changeset
  alias Ash.Error.Changes.InvalidAttribute
  alias Caluma.Form.Validations.SpecMatcher

  @localized_fields [:name]

  @impl true
  def init(opts) do
    case opts[:field] do
      field when is_atom(field) and not is_nil(field) -> {:ok, opts}
      _ -> {:error, "field option is required (atom)"}
    end
  end

  @impl true
  def validate(changeset, opts, _context) do
    field = opts[:field]

    case Changeset.get_argument(changeset, field) do
      nil ->
        :ok

      value ->
        form = changeset.data

        case SpecMatcher.compare(form, field, value, localized?: field in @localized_fields) do
          :ok ->
            :ok

          {:mismatch, actual, expected} ->
            {:error,
             InvalidAttribute.exception(
               field: field,
               value: value,
               message:
                 "form #{inspect(form.slug)} already exists with #{field}=#{inspect(actual)}, got #{inspect(expected)}"
             )}
        end
    end
  end
end
