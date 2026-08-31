defmodule Caluma.Form.Changes.AddTableRowTest do
  use Ebau.DataCase, async: true

  import Caluma.Test.Fixtures

  setup [:create_form, :create_document]

  @opts [authorize?: false, actor: nil]

  defp rows(document) do
    Ash.load!(document, [rows: [:field]], @opts).rows
  end

  defp create_row!(document, params) do
    Caluma.Test.Domain.create_row!(Map.put(Map.new(params), :parent_id, document.id), @opts)
  end

  describe "question: {owner, name}, document_argument" do
    test "creates a row under the owner's table question", %{document: document} do
      create_row!(document, field: "x")

      assert [%{field: "x"}] = rows(document)
    end

    test "row form and family come from the table question", %{document: document} do
      row = create_row!(document, field: "x")

      assert row.form_id == "rows-row-form"
      assert row.family_id == document.id
    end

    test "new row takes sort 0 and shifts existing rows up", %{document: document} do
      create_row!(document, field: "first")
      create_row!(document, field: "second")

      assert [%{field: "first", sort: 1}, %{field: "second", sort: 0}] =
               Ash.load!(document, [rows: [:field, :sort]], @opts).rows
    end

    test "errors when the parent document does not exist" do
      assert {:error, %Ash.Error.Invalid{}} =
               Caluma.Test.Domain.create_row(%{parent_id: Ash.UUID.generate()}, @opts)
    end
  end

  describe "destroy" do
    test "removes the row and its answers", %{document: document} do
      row = create_row!(document, field: "x")

      Caluma.Test.Domain.destroy_row!(row, @opts)

      assert rows(document) == []
      assert Caluma.Form.list_answers_by_document!(row.id, @opts) == []
    end
  end
end
