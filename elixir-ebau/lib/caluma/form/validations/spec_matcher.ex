defmodule Caluma.Form.Validations.SpecMatcher do
  @moduledoc false

  alias Ash.ActionInput
  alias Ash.Changeset
  alias Ash.Error.Action.InvalidArgument
  alias Ash.Error.Changes.InvalidAttribute
  alias Caluma.Form.Types.LocalizedFieldHelpers

  # Caluma fields stored as `LocalizedField` maps — comparison only checks
  # the locales present in the expected value.
  @localized_fields [:label, :name]

  @doc "Shared `init/1` for validations that require a `field:` atom option."
  @spec init(keyword) :: {:ok, keyword} | {:error, String.t()}
  def init(opts) do
    case opts[:field] do
      field when is_atom(field) and not is_nil(field) -> {:ok, opts}
      _ -> {:error, "field option is required (atom)"}
    end
  end

  @doc """
  Full `validate/3` body for `Ash.Resource.Validation` on a changeset.
  `name_fn` receives the subject and returns the display name for error messages.
  """
  @spec validate_changeset(Changeset.t(), keyword, (map -> String.t())) :: :ok | {:error, term}
  def validate_changeset(changeset, opts, name_fn) do
    field = opts[:field]

    case Changeset.get_argument(changeset, field) do
      nil ->
        :ok

      value ->
        subject = changeset.data

        run(subject, field, value, fn actual, expected ->
          InvalidAttribute.exception(
            field: field,
            value: value,
            message:
              "#{name_fn.(subject)} already exists with #{field}=#{inspect(actual)}, got #{inspect(expected)}"
          )
        end)
    end
  end

  @doc """
  Full `validate/3` body for `Ash.Resource.Validation` on an action input.
  `subject_key` is the argument holding the subject; `name_fn` returns its display name.
  """
  @spec validate_action_input(ActionInput.t(), keyword, atom, (map -> String.t())) ::
          :ok | {:error, term}
  def validate_action_input(input, opts, subject_key, name_fn) do
    field = opts[:field]

    case ActionInput.get_argument(input, field) do
      nil ->
        :ok

      value ->
        subject = ActionInput.get_argument(input, subject_key)

        run(subject, field, value, fn actual, expected ->
          InvalidArgument.exception(
            field: field,
            value: value,
            message:
              "#{name_fn.(subject)} already exists with #{field}=#{inspect(actual)}, got #{inspect(expected)}"
          )
        end)
    end
  end

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

  @spec run(map, atom, term, (term, term -> term)) :: :ok | {:error, term}
  defp run(subject, field, value, error_fn) do
    case compare(subject, field, value) do
      :ok -> :ok
      {:mismatch, actual, expected} -> {:error, error_fn.(actual, expected)}
    end
  end
end
