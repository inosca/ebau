defmodule Caluma.Form.Calculations.MappedListDocumentAnswerTest do
  use Ebau.DataCase, async: true

  require Ash.Query

  defmodule TestInstance do
    use Ash.Resource,
      otp_app: :ebau,
      domain: Caluma.Form.Calculations.MappedListDocumentAnswerTest.TestDomain,
      data_layer: AshPostgres.DataLayer,
      extensions: [Caluma.Workflow.Extensions.Case]

    postgres do
      table "INSTANCE"
      repo Ebau.Repo
      migrate? false
    end

    caluma_case do
      through :case

      caluma_document do
        mapped_answer :category_code, :integer,
          question_id: "category",
          mapping: %{"choice-a" => 10, "choice-b" => 20}

        mapped_list_answer :is_paper?, :boolean,
          question_id: {Ebau.Caluma.CantonResolver, %{default: "is-paper", so: "ist-papier"}},
          mapping:
            {Ebau.Caluma.CantonResolver,
             %{
               default: %{"is-paper-yes" => true, "is-paper-no" => false},
               so: %{"ist-papier-ja" => true, "ist-papier-nein" => false}
             }}
      end
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

  defmodule TestDomain do
    use Ash.Domain, validate_config_inclusion?: false

    resources do
      resource Caluma.Form.Calculations.MappedListDocumentAnswerTest.TestInstance do
        define :get_instance, action: :read, get_by: [:id]
        define :read_instances, action: :read
      end
    end
  end

  setup do
    Caluma.Workflow.create_workflow!(
      %{
        slug: "building-permit",
        name: %{"de" => "Building permit"}
      },
      authorize?: false, actor: nil
    )

    Caluma.Form.create_form_tree!(
      %{
        slug: "baugesuch",
        name: "Baugesuch",
        questions: [
          %{slug: "category", label: "Category", type: :choice},
          %{slug: "is-paper", label: "Is paper", type: :multiple_choice},
          %{slug: "ist-papier", label: "Ist Papier", type: :multiple_choice}
        ]
      },
      authorize?: false, actor: nil
    )

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
      without_answer: without_answer,
      so_matching:
        create_instance_with_answers(%{"ist-papier" => ["ist-papier-ja", "ist-papier-nein"]}).instance
    }
  end

  test "loads mapped list answers without loading relationship data", %{matching: matching} do
    instance = TestDomain.get_instance!(matching.id)
    assert %Ash.NotLoaded{} = instance.case

    loaded = Ash.load!(instance, [:category_code, :is_paper?])

    assert loaded.category_code == 10
    assert loaded.is_paper? == [true, false]
    assert %Ash.NotLoaded{} = loaded.case
  end

  test "supports filtering by the mapped answer in SQL", %{
    matching: matching,
    non_matching: non_matching,
    without_answer: without_answer
  } do
    matching_ids =
      TestDomain.read_instances!(
        query:
          TestInstance
          |> Ash.Query.filter(category_code == 10)
      )
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
      TestDomain.read_instances!(
        query:
          TestInstance
          |> Ash.Query.filter(is_paper? == ^[true, false])
      )
      |> Enum.map(& &1.id)

    assert matching.id in matching_ids
    refute non_matching.id in matching_ids
    refute without_answer.id in matching_ids
  end

  @tag :skip
  # TODO: requires runtime canton resolver in answer_filter; reverted for now
  test "uses canton-specific question_ids and answer mappings in SQL", %{so_matching: so_matching} do
    [loaded] =
      TestDomain.read_instances!(
        query:
          TestInstance
          |> Ash.Query.set_context(%{canton: :so})
          |> Ash.Query.filter(id == ^so_matching.id)
          |> Ash.Query.load([:is_paper?])
      )

    assert loaded.is_paper? == [true, false]

    matching_ids =
      TestDomain.read_instances!(
        query:
          TestInstance
          |> Ash.Query.set_context(%{canton: :so})
          |> Ash.Query.filter(is_paper? == ^[true, false])
      )
      |> Enum.map(& &1.id)

    assert so_matching.id in matching_ids
  end

  defp create_instance_with_answers(answers) do
    case_record =
      Caluma.Workflow.create_case!(%{workflow: %{slug: "building-permit"}}, authorize?: false, actor: nil)

    instance = Ebau.Instances.create_instance!(%{case: %{id: case_record.id}}, authorize?: false, actor: nil)

    document =
      Caluma.Form.create_document!(%{form: %{slug: "baugesuch"}, case: %{id: case_record.id}},
        authorize?: false, actor: nil
      )

    Enum.each(answers, fn {question_id, value} ->
      Caluma.Form.create_answer!(
        %{
          document_id: document.id,
          question_id: question_id,
          value: value
        },
        authorize?: false, actor: nil
      )
    end)

    %{instance: instance, case: case_record, document: document}
  end
end
