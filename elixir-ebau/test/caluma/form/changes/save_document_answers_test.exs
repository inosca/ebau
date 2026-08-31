defmodule Caluma.Form.Changes.SaveDocumentAnswersTest do
  use Ebau.DataCase, async: true

  import Caluma.Test.Fixtures

  setup [:create_form]

  @load [:title, :is_paper, :tags]

  defp update!(document, params) do
    Caluma.Test.Domain.update_document!(document, params, authorize?: false, actor: nil)
  end

  defp reload(document) do
    Ash.load!(document, @load, authorize?: false, actor: nil)
  end

  describe "create" do
    test "writes provided answers" do
      document = create_document!(title: "Neubau", is_paper: true)

      assert %{title: "Neubau", is_paper: true} = reload(document)
    end

    test "leaves answers alone whose argument is not provided" do
      document = create_document!(title: "Neubau")

      assert %{title: "Neubau", is_paper: nil} = reload(document)
    end
  end

  describe "update" do
    setup [:create_document]

    test "sets an answer readable through the calculation", %{document: document} do
      update!(document, %{title: "Neubau"})

      assert reload(document).title == "Neubau"
    end

    test "overwrites instead of duplicating", %{document: document} do
      update!(document, %{title: "first"})
      update!(document, %{title: "second"})

      assert reload(document).title == "second"

      assert [_one] =
               Caluma.Form.list_answers_by_document!(document.id, authorize?: false, actor: nil)
    end

    test "leaves answers alone whose argument is not provided", %{document: document} do
      update!(document, %{title: "Neubau"})
      update!(document, %{is_paper: false})

      assert %{title: "Neubau", is_paper: false} = reload(document)
    end

    test "stores the option slug deduced from the mapping", %{document: document} do
      update!(document, %{is_paper: true})

      assert reload(document).is_paper == true

      assert [%{value: "is-paper-yes"}] =
               Caluma.Form.list_answers_by_document!(document.id, authorize?: false, actor: nil)
    end

    test "stores option slugs for a mapped list", %{document: document} do
      update!(document, %{tags: ["A", "B"]})
      reloaded_document = reload(document)
      assert Enum.all?(reloaded_document.tags, fn v -> v in ["A", "B"] end)
    end

    test "clears a mapped answer when given nil", %{document: document} do
      update!(document, %{is_paper: true})
      update!(document, %{is_paper: nil})

      assert reload(document).is_paper == nil
    end
  end
end
