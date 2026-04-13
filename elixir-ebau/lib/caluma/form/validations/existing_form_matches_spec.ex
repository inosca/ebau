defmodule Caluma.Form.Validations.ExistingFormMatchesSpec do
  @moduledoc """
  Validates that an already persisted form matches a provided form-tree spec.

  Used by `Caluma.Form.apply_form_tree` before attaching or checking nested
  questions. Only fields present in incoming spec are compared. For localized
  fields like `name`, caller may provide either plain string or localization map;
  comparison only checks locales present in provided input.
  """

  use Ash.Resource.Validation

  alias Ash.Changeset
  alias Ash.Error.Changes.InvalidAttribute
  alias Caluma.Form.Types.LocalizedFieldHelpers

  @impl true
  def validate(changeset, _opts, _context) do
    form_spec = Changeset.get_argument(changeset, :form_spec) || %{}

    with :ok <- validate_optional_field(changeset, :name, Map.get(form_spec, :name)) do
      validate_optional_field(changeset, :meta, Map.get(form_spec, :meta))
    end
  end

  defp validate_optional_field(_changeset, _field, nil), do: :ok

  defp validate_optional_field(changeset, :name, value) do
    form = changeset.data
    actual = form.name
    expected = LocalizedFieldHelpers.normalize(value)

    if LocalizedFieldHelpers.matches?(actual, expected) do
      :ok
    else
      {:error,
       InvalidAttribute.exception(
         field: :name,
         value: value,
         message:
           "form #{inspect(form.slug)} already exists with name #{inspect(actual)}, got #{inspect(expected)}"
       )}
    end
  end

  defp validate_optional_field(changeset, field, value) do
    form = changeset.data
    actual = Map.fetch!(form, field)

    if actual == value do
      :ok
    else
      {:error,
       InvalidAttribute.exception(
         field: field,
         value: value,
         message:
           "form #{inspect(form.slug)} already exists with #{field}=#{inspect(actual)}, got #{inspect(value)}"
       )}
    end
  end
end
