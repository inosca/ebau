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

  describe "expression/2" do
    setup do
      {:ok, opts} = DocumentAnswer.init(question_ids: %{default: "default-q", gr: "gr-q"})
      %{opts: opts}
    end

    test "returns a non-nil expression", %{opts: opts} do
      refute is_nil(DocumentAnswer.expression(opts, %{}))
    end

    test "produces different expressions for different cantons", %{opts: opts} do
      expr_gr = DocumentAnswer.expression(opts, %{canton: :gr})
      expr_be = DocumentAnswer.expression(opts, %{canton: :be})
      assert expr_gr != expr_be
    end

    test "produces the same expression for unknown canton and no canton", %{opts: opts} do
      expr_no_canton = DocumentAnswer.expression(opts, %{})
      expr_unknown = DocumentAnswer.expression(opts, %{canton: :be})
      assert expr_no_canton == expr_unknown
    end
  end
end
