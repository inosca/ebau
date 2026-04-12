defmodule Ebau.Caluma.Calculations.CaseMetaTest do
  use ExUnit.Case, async: true

  alias Ebau.Caluma.Calculations.CaseMeta

  describe "init/1" do
    test "accepts valid keys with a :default entry" do
      assert {:ok, _} = CaseMeta.init(keys: %{default: "dossier-number"})
    end

    test "accepts keys with canton-specific and default entries" do
      assert {:ok, _} = CaseMeta.init(keys: %{default: "dossier-number", gr: "gr-dossier"})
    end

    test "preserves opts through init" do
      {:ok, opts} = CaseMeta.init(keys: %{default: "dossier-number", gr: "gr-dossier"})
      assert opts[:keys] == %{default: "dossier-number", gr: "gr-dossier"}
    end

    test "rejects non-map keys" do
      assert {:error, _} = CaseMeta.init(keys: "not-a-map")
    end

    test "rejects nil keys" do
      assert {:error, _} = CaseMeta.init(keys: nil)
    end

    test "rejects keys without a :default entry" do
      assert {:error, _} = CaseMeta.init(keys: %{gr: "gr-key"})
    end
  end

  describe "expression/2" do
    test "returns a non-nil expression" do
      {:ok, opts} = CaseMeta.init(keys: %{default: "dossier-number"})
      refute is_nil(CaseMeta.expression(opts, %{}))
    end

    test "uses the canton-specific key when available" do
      keys = %{default: "dossier-number", gr: "gr-dossier"}
      assert Ebau.Caluma.Helpers.get_canton_value(keys, %{canton: :gr}) == "gr-dossier"
    end

    test "uses the default key when no canton-specific mapping exists" do
      keys = %{default: "dossier-number", gr: "gr-dossier"}
      assert Ebau.Caluma.Helpers.get_canton_value(keys, %{canton: :be}) == "dossier-number"
    end

    test "produces different expressions for different canton contexts" do
      {:ok, opts} = CaseMeta.init(keys: %{default: "dossier-number", gr: "gr-dossier"})
      expr_gr = CaseMeta.expression(opts, %{canton: :gr})
      expr_default = CaseMeta.expression(opts, %{})
      assert expr_gr != expr_default
    end
  end
end
