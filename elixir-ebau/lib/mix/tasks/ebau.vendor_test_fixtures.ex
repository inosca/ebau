defmodule Mix.Tasks.Ebau.VendorTestFixtures do
  @shortdoc "Vendors the minimal fixture subset needed by Elixir tests"

  @moduledoc """
  Copies the minimal Django fixture subset needed by Elixir tests into
  `priv/test_fixtures`.

  This task vendors fixture files needed by Elixir tests so CI does not depend on
  a full `../django` checkout at test runtime.

  Source root resolution order:

  1. `LEGACY_FIXTURE_ROOT`
  2. fallback `../django`

  Currently vendored:

  - `kt_so/config/user.json`
  - `kt_so/config/caluma_workflow.json`

  Destination root:

      priv/test_fixtures

  ## Examples

      mix ebau.vendor_test_fixtures
  """

  use Mix.Task

  @impl true
  def run(args) do
    if args != [] do
      Mix.raise("mix ebau.vendor_test_fixtures does not accept arguments")
    end

    source_root = source_root()
    destination_root = destination_root()

    File.rm_rf!(destination_root)

    Enum.each(vendored_files(), fn relative_path ->
      source_path = Path.join(source_root, relative_path)
      destination_path = Path.join(destination_root, relative_path)

      if !File.exists?(source_path) do
        Mix.raise("fixture file #{source_path} does not exist")
      end

      File.mkdir_p!(Path.dirname(destination_path))
      File.cp!(source_path, destination_path)

      Mix.shell().info("Vendored #{relative_path}")
    end)
  end

  defp vendored_files do
    [
      "kt_so/config/user.json",
      "kt_so/config/caluma_workflow.json"
    ]
  end

  defp source_root do
    System.get_env("LEGACY_FIXTURE_ROOT") ||
      Mix.Project.project_file()
      |> Path.dirname()
      |> Path.join("../django")
      |> Path.expand()
  end

  defp destination_root do
    Mix.Project.project_file()
    |> Path.dirname()
    |> Path.join("priv/test_fixtures")
    |> Path.expand()
  end
end
