defmodule Caluma.Workflow.Calculations.CaseMetaTest do
  use ExUnit.Case, async: true

  alias Caluma.Workflow.Calculations.CaseMeta

  describe "init/1" do
    test "accepts a plain string key" do
      assert {:ok, _} = CaseMeta.init(key: "dossier-number")
    end

    test "accepts a {module, opts} resolver tuple" do
      assert {:ok, _} =
               CaseMeta.init(key: {Ebau.Caluma.CantonResolver, %{default: "dossier-number"}})
    end

    test "preserves opts through init" do
      resolver = {Ebau.Caluma.CantonResolver, %{default: "dossier-number", gr: "gr-dossier"}}
      {:ok, opts} = CaseMeta.init(key: resolver)
      assert opts[:key] == resolver
    end

    test "rejects nil key" do
      assert {:error, _} = CaseMeta.init(key: nil)
    end

    test "rejects integer key" do
      assert {:error, _} = CaseMeta.init(key: 42)
    end
  end
end
