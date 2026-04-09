defmodule Ebau.Caluma.HelpersTest do
  use ExUnit.Case, async: true

  alias Ebau.Caluma.Helpers

  describe "get_question_slugs/2" do
    test "returns canton-specific ids when canton matches" do
      opts = [question_ids: %{default: "default-q", gr: "gr-q"}]
      assert Helpers.get_question_slugs(opts, %{canton: :gr}) == ["gr-q"]
    end

    test "falls back to default when canton has no specific mapping" do
      opts = [question_ids: %{default: "default-q", gr: "gr-q"}]
      assert Helpers.get_question_slugs(opts, %{canton: :be}) == ["default-q"]
    end

    test "falls back to default when context has no canton key" do
      opts = [question_ids: %{default: "default-q"}]
      assert Helpers.get_question_slugs(opts, %{}) == ["default-q"]
    end

    test "wraps single string value in a list" do
      opts = [question_ids: %{default: "single-q"}]
      assert Helpers.get_question_slugs(opts, %{}) == ["single-q"]
    end

    test "returns a list value as-is" do
      opts = [question_ids: %{default: ["q-v1", "q-v2"]}]
      assert Helpers.get_question_slugs(opts, %{}) == ["q-v1", "q-v2"]
    end

    test "returns canton-specific list when present" do
      opts = [question_ids: %{default: "default-q", gr: ["gr-q-v1", "gr-q-v2"]}]
      assert Helpers.get_question_slugs(opts, %{canton: :gr}) == ["gr-q-v1", "gr-q-v2"]
    end
  end

  describe "get_canton_value/2" do
    test "returns canton-specific value when canton matches" do
      mapping = %{default: "default-key", gr: "gr-key"}
      assert Helpers.get_canton_value(mapping, %{canton: :gr}) == "gr-key"
    end

    test "falls back to default when canton has no specific value" do
      mapping = %{default: "default-key", gr: "gr-key"}
      assert Helpers.get_canton_value(mapping, %{canton: :be}) == "default-key"
    end

    test "returns default when context has no canton key" do
      mapping = %{default: "default-key"}
      assert Helpers.get_canton_value(mapping, %{}) == "default-key"
    end
  end
end
