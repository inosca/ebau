defmodule Caluma.Form.Changes.SetRootFamilyTest do
  use Ebau.DataCase, async: true

  setup do
    Caluma.Form.create_form_tree!(
      %{
        slug: "set-root-family-form",
        name: "Set Root Family Form",
        questions: [
          %{
            slug: "rows",
            label: "Rows",
            type: :table,
            form: %{name: "Row"},
            questions: [%{slug: "field", label: "Field", type: :text}]
          }
        ]
      },
      authorize?: false
    )

    :ok
  end

  test "root document family_id points at itself" do
    document =
      Caluma.Form.create_document!(%{form: %{slug: "set-root-family-form"}}, authorize?: false)

    assert document.family_id == document.id
  end

  test "row document inherits family from parent root" do
    root =
      Caluma.Form.create_document!(%{form: %{slug: "set-root-family-form"}}, authorize?: false)

    row =
      Caluma.Form.create_row_document!(
        root,
        %{slug: "rows"},
        [%{question_id: "field", value: "x"}],
        authorize?: false
      )

    assert row.family_id == root.id
    refute row.family_id == row.id
  end
end
