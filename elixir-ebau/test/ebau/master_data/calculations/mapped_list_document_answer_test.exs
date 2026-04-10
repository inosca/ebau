defmodule Ebau.MasterData.Calculations.MappedListDocumentAnswerTest do
  use Ebau.DataCase, async: true

  require Ash.Expr
  require Ash.Query

  defmodule TestDomain do
    use Ash.Domain, validate_config_inclusion?: false

    resources do
      resource Ebau.MasterData.Calculations.MappedListDocumentAnswerTest.TestInstance
    end
  end

  defmodule TestInstance do
    use Ash.Resource,
      otp_app: :ebau,
      domain: TestDomain,
      data_layer: AshPostgres.DataLayer,
      extensions: [Ebau.MasterData.Extensions.MasterData]

    postgres do
      table "INSTANCE"
      repo Ebau.Repo
      migrate? false
    end

    master_data do
      mapped_answer :category_code, :integer,
        question_ids: %{default: "category"},
        mapping: %{"choice-a" => 10, "choice-b" => 20}

      mapped_list_answer :tags, :integer,
        question_ids: %{default: "is-paper"},
        mapping: %{"is-paper-yes" => 1, "is-paper-no" => 2}
    end

    attributes do
      integer_primary_key :id, source: :INSTANCE_ID
    end

    relationships do
      belongs_to :case, Caluma.Workflow.Case
    end

    actions do
      defaults [:read]
    end
  end

  setup do
    %{instance: matching} =
      create_instance_with_answers(%{
        "category" => "choice-a",
        "is-paper" => ["is-paper-yes", "is-paper-no"]
      })

    %{instance: non_matching} =
      create_instance_with_answers(%{
        "category" => "choice-b",
        "is-paper" => ["is-paper-no"]
      })

    %{instance: without_answer} = create_instance_with_answers(%{})

    %{
      matching: matching,
      non_matching: non_matching,
      without_answer: without_answer
    }
  end

  test "loads mapped list answers without loading relationship data", %{matching: matching} do
    instance = Ash.get!(TestInstance, matching.id)
    assert %Ash.NotLoaded{} = instance.case

    loaded = Ash.load!(instance, [:category_code, :tags])

    assert loaded.category_code == 10
    assert loaded.tags == [1, 2]
    assert %Ash.NotLoaded{} = loaded.case
  end

  test "supports filtering by the mapped answer in SQL", %{
    matching: matching,
    non_matching: non_matching,
    without_answer: without_answer
  } do
    matching_ids =
      TestInstance
      |> Ash.Query.filter(Ash.Expr.expr(category_code == 10))
      |> Ash.read!()
      |> Enum.map(& &1.id)

    assert matching.id in matching_ids
    refute non_matching.id in matching_ids
    refute without_answer.id in matching_ids
  end

  test "supports filtering by the mapped list answer in SQL", %{
    matching: matching,
    non_matching: non_matching,
    without_answer: without_answer
  } do
    matching_ids =
      TestInstance
      |> Ash.Query.filter(Ash.Expr.expr(tags == ^[1, 2]))
      |> Ash.read!()
      |> Enum.map(& &1.id)

    assert matching.id in matching_ids
    refute non_matching.id in matching_ids
    refute without_answer.id in matching_ids
  end

  defp create_instance_with_answers(answers) do
    case_record = Caluma.Workflow.create_case!(%{workflow: %{slug: "building-permit"}})
    instance = Ebau.Instances.create_instance!(%{case: %{id: case_record.id}}, authorize?: false)

    document =
      Caluma.Form.create_document!(%{form: %{slug: "baugesuch"}, case: %{id: case_record.id}})

    Enum.each(answers, fn {question_id, value} ->
      Ash.create!(Caluma.Form.Answer, %{
        document_id: document.id,
        question_id: question_id,
        value: value
      })
    end)

    %{instance: instance, case: case_record, document: document}
  end
end
