defmodule Ebau.Test.GisLinkHelper do
  @moduledoc """
  Test helper for creating Caluma form trees with plot data for GIS link tests.
  """

  @spec create_caluma_form_and_document(Caluma.Case.Case.t()) :: Caluma.Form.Document.t()
  def create_caluma_form_and_document(case) do
    Caluma.Form.create_form_tree!(
      %{
        slug: "baugesuch",
        name: "Baugesuch",
        questions: [
          %{
            slug: "parzellen",
            label: "Grundstücke",
            type: :table,
            form: %{
              slug: "parzelle-tabelle",
              name: "Grundstück Tabelle"
            },
            questions: [
              %{
                slug: "lagekoordinaten-nord",
                label: "Lagekoordinaten - Nord",
                type: :float
              },
              %{
                slug: "lagekoordinaten-ost",
                label: "Lagekoordinaten - Ost",
                type: :float
              }
            ]
          }
        ]
      },
      authorize?: false
    )

    doc = Caluma.Form.create_document!(%{form: %{slug: "baugesuch"}, case: %{id: case.id}})

    Caluma.Form.create_row_document!(doc, %{slug: "parzellen"}, [
      %{question_id: "lagekoordinaten-nord", value: 123},
      %{question_id: "lagekoordinaten-ost", value: 456}
    ])

    doc
  end
end
