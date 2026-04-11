defmodule Mix.Tasks.Ebau.VendorTestFixtures do
  @shortdoc "Vendors all canton fixture directories into priv/test_fixtures"

  @moduledoc """
  Copies all Django canton fixture directories (`kt_*`) into `priv/test_fixtures`.

  This task vendors fixture files needed by Elixir tests so CI does not depend on
  a full `../django` checkout at test runtime.

  Source root resolution order:

  1. `LEGACY_FIXTURE_ROOT`
  2. fallback `../django`

  Destination root:

      priv/test_fixtures

  All directories matching `kt_*` under source root are copied recursively.
  Existing vendored canton directories are replaced.

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

    applications =
      source_root
      |> Path.join("kt_*")
      |> Path.wildcard()
      |> Enum.filter(&File.dir?/1)
      |> Enum.sort()

    if applications == [] do
      Mix.raise("no canton fixture directories found under #{source_root}")
    end

    Enum.each(applications, fn application_path ->
      application = Path.basename(application_path)
      destination_path = Path.join(destination_root, application)

      File.rm_rf!(destination_path)
      File.mkdir_p!(destination_root)
      File.cp_r!(application_path, destination_path)

      Mix.shell().info("Vendored #{application}")
    end)
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
