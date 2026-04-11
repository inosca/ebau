defmodule Caluma.FormFixtureTest do
  use Ebau.DataCase, async: true

  test "creates nested form fixture tree and document from root form" do
    form =
      Caluma.Test.Form.create_form!("the-new-form-slug",
        questions: [
          [slug: "question-1", type: :string],
          [slug: "question-2", type: :text],
          [
            slug: "question-3",
            type: :form,
            questions: [
              [slug: "sub-form-question-1", type: :text],
              [slug: "sub-form-question-2", type: :text],
              [
                slug: "sub-form-table-question",
                type: :table,
                questions: [
                  [
                    slug: "question-3",
                    type: :form,
                    questions: [[slug: "sub-form-question-1", type: :text]]
                  ]
                ]
              ]
            ]
          ]
        ]
      )

    assert form.slug == "the-new-form-slug"

    document = Caluma.Form.create_document!(%{form: %{slug: form.slug}})

    assert document.form_id == "the-new-form-slug"

    assert_question("question-1", :text)
    assert_question("question-2", :text)
    assert_question("question-3", :form, sub_form_id: "question-3")
    assert_question("question-3.sub-form-question-1", :text)
    assert_question("question-3.sub-form-question-2", :text)

    assert_question("question-3.sub-form-table-question", :table,
      row_form_id: "question-3.sub-form-table-question"
    )

    assert_question("question-3.sub-form-table-question.question-3", :form,
      sub_form_id: "question-3.sub-form-table-question.question-3"
    )

    assert_question(
      "question-3.sub-form-table-question.question-3.sub-form-question-1",
      :text
    )

    assert_form_question_sort("the-new-form-slug", "question-1", 1)
    assert_form_question_sort("the-new-form-slug", "question-2", 2)
    assert_form_question_sort("the-new-form-slug", "question-3", 3)
    assert_form_question_sort("question-3", "question-3.sub-form-question-1", 1)
    assert_form_question_sort("question-3", "question-3.sub-form-question-2", 2)
    assert_form_question_sort("question-3", "question-3.sub-form-table-question", 3)
  end

  defp assert_question(slug, type, attrs \\ []) do
    question = Caluma.Form.get_question_by_slug!(slug, authorize?: false)

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
        authorize?: false
      )

    assert form_question.sort == sort
    assert form_question.id == "#{form_id}.#{question_id}"
  end
end
