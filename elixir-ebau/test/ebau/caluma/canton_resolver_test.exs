defmodule Ebau.Caluma.CantonResolverTest do
  use ExUnit.Case, async: true

  alias Ebau.Caluma.CantonResolver

  @mapping %{default: "nachname", gr: "familienname", be: ["name", "vorname"]}

  describe "resolve/2" do
    test "returns default when context has no canton" do
      assert CantonResolver.resolve(@mapping) == "nachname"
    end

    test "returns default when context is an empty map" do
      assert CantonResolver.resolve(@mapping) == "nachname"
    end

    @tag canton: :gr
    test "returns canton-specific value when canton matches a key" do
      assert CantonResolver.resolve(@mapping) == "familienname"
    end

    @tag canton: :so
    test "falls back to default when canton does not match any key" do
      assert CantonResolver.resolve(@mapping) == "nachname"
    end

    @tag canton: :gr
    test "reads canton from source_context.canton" do
      assert CantonResolver.resolve(@mapping) == "familienname"
    end

    @tag canton: :be
    test "returns canton-specific value that is a list" do
      assert CantonResolver.resolve(@mapping) == ["name", "vorname"]
    end
  end
end
