defmodule Caluma.Form.QuestionIdTest do
  use ExUnit.Case, async: true

  alias Caluma.Form.QuestionId

  defmodule Resolver do
    @behaviour Caluma.Form.Behaviours.SlugResolver

    @impl true
    def resolve(opts), do: opts[:slug]
  end

  describe "slugs/1" do
    test "wraps a single slug" do
      assert QuestionId.slugs("a") == ["a"]
    end

    test "dedupes a list" do
      assert QuestionId.slugs(["a", "b", "a"]) == ["a", "b"]
    end

    test "resolves a {resolver, opts} tuple" do
      assert QuestionId.slugs({Resolver, %{slug: "a"}}) == ["a"]
      assert QuestionId.slugs({Resolver, %{slug: ["a", "b"]}}) == ["a", "b"]
    end
  end

  describe "slug/1" do
    test "is the last (current) slug" do
      assert QuestionId.slug("a") == "a"
      assert QuestionId.slug(["a-v1", "a-v2"]) == "a-v2"
      assert QuestionId.slug({Resolver, %{slug: ["a-v1", "a-v2"]}}) == "a-v2"
    end
  end
end
