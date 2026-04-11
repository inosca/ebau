defmodule Ebau.Test.CantonFixtures do
  @moduledoc """
  Explicit helpers for loading canton fixture files in tests.

  This module is thin test-facing wrapper around `Ebau.Legacy.ConfigLoader`.
  It keeps test setup readable and avoids hidden fixture magic.

  Use this in test `setup` blocks when test needs real canton config:

      setup do
        Ebau.Test.CantonFixtures.load_canton_config!(:so)
        :ok
      end

  For smaller, more explicit setup, load only selected files:

      setup do
        Ebau.Test.CantonFixtures.load_canton_files!(:so, [
          "user.json",
          "caluma_workflow.json",
          "caluma_form.json"
        ])

        :ok
      end

  Available levels:

  - `load_canton_config!/1`: all `config/*.json`
  - `load_canton_fixtures!/1`: all `config/*.json` and `data/*.json`
  - `load_canton_files!/3`: explicit selected files

  Keep this explicit. Most tests should still prefer small builders/factories over
  loading full canton config.
  """

  alias Ebau.Legacy.ConfigLoader

  @type canton :: atom()
  @type scope :: :config | :all
  @type fixture_filename :: String.t()
  @type fixture_path :: String.t()
  @type model :: String.t()

  @doc """
  Loads all `config/*.json` files for given canton.

  ## Examples

      iex> Ebau.Test.CantonFixtures.load_canton_config!(:so)
      :ok
  """
  @spec load_canton_config!(canton()) :: :ok
  def load_canton_config!(canton) do
    ConfigLoader.load_application_config!("kt_#{canton}")
  end

  @doc """
  Loads all `config/*.json` and `data/*.json` files for given canton.

  ## Examples

      iex> Ebau.Test.CantonFixtures.load_canton_fixtures!(:so)
      :ok
  """
  @spec load_canton_fixtures!(canton()) :: :ok
  def load_canton_fixtures!(canton) do
    ConfigLoader.load_application_config!("kt_#{canton}", scope: :all)
  end

  @doc """
  Loads explicit selected fixture filenames for given canton.

  Filenames are matched against files returned by `canton_files!/2`.
  Raises if requested file is missing.

  ## Examples

      iex> Ebau.Test.CantonFixtures.load_canton_files!(:so, [
      ...>   "user.json",
      ...>   "caluma_workflow.json",
      ...>   "caluma_form.json"
      ...> ])
      :ok
  """
  @spec load_canton_files!(canton(), [fixture_filename()], scope()) :: :ok
  def load_canton_files!(canton, filenames, scope \\ :config) when is_list(filenames) do
    available_files = canton_files!(canton, scope)

    selected_files =
      Enum.map(filenames, fn filename ->
        Enum.find(available_files, &String.ends_with?(&1, "/#{filename}")) ||
          raise ArgumentError,
                "fixture file #{inspect(filename)} not found for canton #{inspect(canton)} in scope #{inspect(scope)}"
      end)

    ConfigLoader.load_files!(selected_files)
  end

  @doc """
  Returns available fixture files for given canton and scope.
  """
  @spec canton_files!(canton(), scope()) :: [fixture_path()]
  def canton_files!(canton, scope \\ :config) do
    ConfigLoader.application_files!("kt_#{canton}", scope)
  end

  @doc """
  Returns supported Django fixture model names.
  """
  @spec supported_models() :: [model()]
  def supported_models do
    ConfigLoader.supported_models()
  end

  @doc """
  Loads explicit list of absolute fixture paths.

  ## Examples

      iex> Ebau.Test.CantonFixtures.load_files!([
      ...>   "/abs/path/to/django/kt_so/config/user.json"
      ...> ])
      :ok
  """
  @spec load_files!([fixture_path()]) :: :ok
  def load_files!(paths) do
    ConfigLoader.load_files!(paths)
  end
end
