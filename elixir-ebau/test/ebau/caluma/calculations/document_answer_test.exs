defmodule Ebau.Caluma.Calculations.DocumentAnswerTest do
  use ExUnit.Case, async: true

  alias Ebau.Caluma.Calculations.DocumentAnswer

  describe "init/1" do
    test "accepts valid question_ids with a :default key" do
      assert {:ok, _} = DocumentAnswer.init(question_ids: %{default: "foo"})
    end

    test "accepts question_ids with canton-specific and default keys" do
      assert {:ok, _} = DocumentAnswer.init(question_ids: %{default: "foo", gr: "foo-gr"})
    end

    test "preserves opts through init" do
      {:ok, opts} = DocumentAnswer.init(question_ids: %{default: "foo", gr: "foo-gr"})
      assert opts[:question_ids] == %{default: "foo", gr: "foo-gr"}
    end

    test "rejects non-map question_ids" do
      assert {:error, _} = DocumentAnswer.init(question_ids: "not-a-map")
    end

    test "rejects nil question_ids" do
      assert {:error, _} = DocumentAnswer.init(question_ids: nil)
    end

    test "rejects question_ids without a :default key" do
      assert {:error, _} = DocumentAnswer.init(question_ids: %{gr: "gr-q"})
    end
  end
end
