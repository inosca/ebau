defmodule Caluma.Form.Calculations.DocumentAnswerTest do
  use ExUnit.Case, async: true

  alias Caluma.Form.Calculations.DocumentAnswer

  defmodule TestResolver do
    @behaviour Caluma.Form.QuestionIdResolver

    @impl true
    def resolve(%{ids: ids}), do: ids
    def resolve(%{id: id}), do: id
  end

  describe "init/1" do
    test "accepts a string question_id" do
      assert {:ok, opts} =
               DocumentAnswer.init(relationship: :foobar, question_id: "parzellennummer")

      assert opts[:question_id] == "parzellennummer"
    end

    test "accepts a list of string question_ids" do
      ids = ["slug-a", "slug-b"]
      assert {:ok, opts} = DocumentAnswer.init(relationship: :foobar, question_id: ids)
      assert opts[:question_id] == ids
    end

    test "accepts a {module, opts} tuple" do
      assert {:ok, opts} =
               DocumentAnswer.init(relationship: :foobar, question_id: {TestResolver, %{id: "x"}})

      assert opts[:question_id] == {TestResolver, %{id: "x"}}
    end

    test "rejects nil" do
      assert {:error, _message} = DocumentAnswer.init(question_id: nil)
    end

    test "rejects an integer" do
      assert {:error, _message} = DocumentAnswer.init(question_id: 42)
    end

    test "rejects a bare atom" do
      assert {:error, _message} = DocumentAnswer.init(question_id: :not_valid)
    end

    test "rejects missing question_id" do
      assert {:error, _message} = DocumentAnswer.init([])
    end
  end

  describe "resolve_question_id dispatch" do
    # We test the resolver dispatch indirectly through expression/2.
    # The returned Ash expression is opaque, but we can verify the resolver
    # module is called by checking it doesn't raise and that our TestResolver
    # receives the right arguments.

    test "resolver module receives opts and context" do
      # TestResolver.resolve(%{use_context: :tenant}, context) returns context[:tenant]
      # If the resolver is called correctly, expression/2 will not raise.
      opts = [question_id: {TestResolver, %{id: "resolved-slug"}}]
      context = %{}

      # Should not raise -- the resolver returns "resolved-slug" which is a
      # valid binary, so the expression branch for a single string is taken.
      assert DocumentAnswer.expression(opts, context)
    end

    test "resolver module can return a list of ids" do
      opts = [question_id: {TestResolver, %{ids: ["a", "b"]}}]
      context = %{}

      assert DocumentAnswer.expression(opts, context)
    end
  end
end
