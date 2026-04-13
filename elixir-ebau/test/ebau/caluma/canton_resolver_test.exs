defmodule Ebau.Caluma.CantonResolverTest do
  use ExUnit.Case, async: true

  alias Ebau.Caluma.CantonResolver

  @mapping %{default: "nachname", gr: "familienname", be: ["name", "vorname"]}

  describe "resolve/2" do
    test "returns default when context has no canton" do
      assert CantonResolver.resolve(@mapping, %{unrelated: "value"}) == "nachname"
    end

    test "returns default when context is an empty map" do
      assert CantonResolver.resolve(@mapping, %{}) == "nachname"
    end

    test "returns canton-specific value when canton matches a key" do
      assert CantonResolver.resolve(@mapping, %{canton: :gr}) == "familienname"
    end

    test "falls back to default when canton does not match any key" do
      assert CantonResolver.resolve(@mapping, %{canton: :sz}) == "nachname"
    end

    test "reads canton from source_context.canton" do
      context = %{source_context: %{canton: :gr}}

      assert CantonResolver.resolve(@mapping, context) == "familienname"
    end

    test "returns canton-specific value that is a list" do
      assert CantonResolver.resolve(@mapping, %{canton: :be}) == ["name", "vorname"]
    end
  end
end
