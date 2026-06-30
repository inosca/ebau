defmodule Caluma.FormFixtureTest do
  use Ebau.DataCase, async: true

  test "reuses nested question slugs across different row forms" do
    form =
      Caluma.Form.create_form_tree!(
        %{
          slug: "baugesuch",
          name: "Baugesuch",
          questions: [
            %{
              slug: "parzellen",
              label: "Parzellen",
              type: :table,
              form: %{name: "Parzellen"},
              questions: [
                %{slug: "lagekoordinaten-nord", label: "Lagekoordinaten Nord", type: :float},
                %{slug: "lagekoordinaten-ost", label: "Lagekoordinaten Ost", type: :float}
              ]
            },
            %{
              slug: "parzellen-2",
              label: "Parzellen 2",
              type: :table,
              form: %{name: %{"de" => "Parzellen 2"}},
              questions: [
                %{slug: "lagekoordinaten-nord"},
                %{slug: "lagekoordinaten-ost"}
              ]
            }
          ]
        },
        load: [form_questions: [question: [row_form: :form_questions]]],
        authorize?: false,
        actor: nil
      )

    assert form.slug == "baugesuch"

    document =
      Caluma.Form.create_document!(%{form: %{slug: form.slug}}, authorize?: false, actor: nil)

    assert document.form_id == "baugesuch"

    assert_question("parzellen", :table, row_form_id: "parzellen")
    assert_question("parzellen-2", :table, row_form_id: "parzellen-2")
    assert_question("lagekoordinaten-nord", :float)
    assert_question("lagekoordinaten-ost", :float)

    assert row_form_question_slugs(form, "parzellen") == [
             "lagekoordinaten-nord",
             "lagekoordinaten-ost"
           ]

    assert row_form_question_slugs(form, "parzellen-2") == [
             "lagekoordinaten-nord",
             "lagekoordinaten-ost"
           ]

    assert_form_question_sort("baugesuch", "parzellen", 1)
    assert_form_question_sort("baugesuch", "parzellen-2", 0)
    assert_form_question_sort("parzellen", "lagekoordinaten-nord", 1)
    assert_form_question_sort("parzellen", "lagekoordinaten-ost", 0)
    assert_form_question_sort("parzellen-2", "lagekoordinaten-nord", 1)
    assert_form_question_sort("parzellen-2", "lagekoordinaten-ost", 0)
  end

  test "reuses nested table forms across different root forms" do
    Caluma.Form.create_form_tree!(
      %{
        slug: "baugesuch-a",
        name: "Baugesuch A",
        questions: [
          %{
            slug: "attachments",
            label: "Attachments",
            type: :table,
            form: %{name: "Attachments"},
            questions: [
              %{slug: "attachment-title", label: "Attachment Title", type: :text}
            ]
          }
        ]
      },
      authorize?: false,
      actor: nil
    )

    form =
      Caluma.Form.create_form_tree!(
        %{
          slug: "baugesuch-b",
          name: "Baugesuch B",
          questions: [
            %{
              slug: "attachments",
              label: "Attachments",
              type: :table,
              form: %{name: "Attachments"},
              questions: [
                %{slug: "attachment-title"}
              ]
            }
          ]
        },
        load: [form_questions: [question: [row_form: :form_questions]]],
        authorize?: false,
        actor: nil
      )

    assert_question("attachments", :table, row_form_id: "attachments")
    assert row_form_question_slugs(form, "attachments") == ["attachment-title"]
    assert_form_question_sort("baugesuch-b", "attachments", 0)
    assert_form_question_sort("attachments", "attachment-title", 0)
  end

  defp assert_question(slug, type, attrs \\ []) do
    question = Caluma.Form.get_question_by_slug!(slug, authorize?: false, actor: nil)

    assert question.type == type

    Enum.each(attrs, fn
      {:sub_form_id, value} -> assert question.sub_form_id == value
      {:row_form_id, value} -> assert question.row_form_id == value
    end)
  end

  defp assert_form_question_sort(form_id, question_id, sort) do
    form_question =
      Caluma.Form.get_form_question_by_form_and_question!(
        form_id,
        question_id,
        authorize?: false,
        actor: nil
      )

    assert form_question.sort == sort
    assert form_question.id == "#{form_id}.#{question_id}"
  end

  defp row_form_question_slugs(form, question_slug) do
    form.form_questions
    |> Enum.find(&(&1.question_id == question_slug))
    |> Map.fetch!(:question)
    |> Map.fetch!(:row_form)
    |> Map.fetch!(:form_questions)
    |> Enum.map(& &1.question_id)
  end
end
