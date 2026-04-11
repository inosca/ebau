defmodule Caluma.Form.Validations.EnsureFixtureFormMatches do
  use Ash.Resource.Validation

  alias Ash.Changeset
  alias Ash.Error.Changes.InvalidAttribute
  alias Caluma.Form.Types.LocalizedField

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
    expected = normalize_localized_field(value)

    if actual == expected do
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

  defp normalize_localized_field(value) do
    case LocalizedField.cast_input(value, []) do
      {:ok, normalized_value} -> normalized_value
      :error -> value
    end
  end
end
