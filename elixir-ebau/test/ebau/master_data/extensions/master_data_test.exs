defmodule Ebau.MasterData.Extensions.MasterDataTest do
  use ExUnit.Case, async: true

  alias Ebau.MasterData.Extensions.MasterData, as: Ext
  alias Ebau.MasterData.Extensions.MasterData.MappedListDocumentAnswer

  defmodule TestResource do
    use Ash.Resource,
      otp_app: :ebau,
      domain: nil,
      data_layer: Ash.DataLayer.Simple,
      extensions: [Ebau.MasterData.Extensions.MasterData]

    resource do
      require_primary_key? false
    end

    master_data do
      answer :proposal, :string, question_ids: %{default: "proposal-q", gr: "gr-proposal-q"}

      mapped_answer :is_paper, :boolean,
        question_ids: %{default: "is-paper-q"},
        mapping: %{"is-paper-yes" => true, "is-paper-no" => false}

      mapped_list_answer :tags, :string,
        question_ids: %{default: "tags-q"},
        mapping: %{"tag-a" => "A", "tag-b" => "B"}

      case_meta :dossier_number, :string, keys: %{default: "dossier-number", gr: "gr-dossier"}

      table :plot_data, Ebau.MasterData.PlotDataRow,
        question_ids: %{default: "parzellen", gr: "gr-parzellen"}
    end
  end

  describe "answer transformer" do
    test "adds a calculation for each answer declaration" do
      calc_names = TestResource |> Ash.Resource.Info.calculations() |> Enum.map(& &1.name)
      assert :proposal in calc_names
    end

    test "uses MasterData.DocumentAnswer as the calculation module" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :proposal))
      assert {Ext.DocumentAnswer, _opts} = calc.calculation
    end

    test "passes question_ids to the calculation" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :proposal))
      {_mod, opts} = calc.calculation
      assert opts[:question_ids] == %{default: "proposal-q", gr: "gr-proposal-q"}
    end
  end

  describe "mapped_answer transformer" do
    test "adds a calculation for each mapped_answer declaration" do
      calc_names = TestResource |> Ash.Resource.Info.calculations() |> Enum.map(& &1.name)
      assert :is_paper in calc_names
    end

    test "uses MappedDocumentAnswer as the calculation module" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :is_paper))
      assert {Ext.MappedDocumentAnswer, _opts} = calc.calculation
    end

    test "passes question_ids and mapping to the calculation" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :is_paper))
      {_mod, opts} = calc.calculation
      assert opts[:question_ids] == %{default: "is-paper-q"}
      assert opts[:mapping] == %{"is-paper-yes" => true, "is-paper-no" => false}
    end
  end

  describe "mapped_list_answer transformer" do
    test "adds a calculation for each mapped_list_answer declaration" do
      calc_names = TestResource |> Ash.Resource.Info.calculations() |> Enum.map(& &1.name)
      assert :tags in calc_names
    end

    test "uses MappedListDocumentAnswer as the calculation module" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :tags))
      assert {Ext.MappedListDocumentAnswer, _opts} = calc.calculation
    end

    test "passes question_ids and mapping to the calculation" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :tags))
      {_mod, opts} = calc.calculation
      assert opts[:question_ids] == %{default: "tags-q"}
      assert opts[:mapping] == %{"tag-a" => "A", "tag-b" => "B"}
    end
  end

  describe "case_meta transformer" do
    test "adds a calculation for each case_meta declaration" do
      calc_names = TestResource |> Ash.Resource.Info.calculations() |> Enum.map(& &1.name)
      assert :dossier_number in calc_names
    end

    test "uses CaseMeta as the calculation module" do
      calc =
        Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :dossier_number))

      assert {Ebau.Caluma.Calculations.CaseMeta, _opts} = calc.calculation
    end

    test "passes keys to the calculation" do
      calc =
        Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :dossier_number))

      {_mod, opts} = calc.calculation
      assert opts[:keys] == %{default: "dossier-number", gr: "gr-dossier"}
    end
  end

  describe "table transformer" do
    test "adds a has_many relationship for each table declaration" do
      rel = Ash.Resource.Info.relationship(TestResource, :plot_data)
      assert rel != nil
      assert rel.type == :has_many
    end

    test "sets the correct destination resource" do
      rel = Ash.Resource.Info.relationship(TestResource, :plot_data)
      assert rel.destination == Ebau.MasterData.PlotDataRow
    end

    test "attaches a filter expression to the relationship" do
      rel = Ash.Resource.Info.relationship(TestResource, :plot_data)
      assert rel.filter != nil
    end
  end

  describe "MappedListDocumentAnswer.calculate/3" do
    setup do
      {:ok, opts} =
        MappedListDocumentAnswer.init(
          question_ids: %{default: "tags-q"},
          mapping: %{"tag-a" => "A", "tag-b" => "B"}
        )

      %{opts: opts}
    end

    test "maps list answer values using the provided mapping", %{opts: opts} do
      records = [
        %{case: %{document: %{answers: [%{question_id: "tags-q", value: ["tag-a", "tag-b"]}]}}}
      ]

      assert MappedListDocumentAnswer.calculate(records, opts, %{}) == [["A", "B"]]
    end

    test "returns nil when no matching answer is found", %{opts: opts} do
      records = [%{case: %{document: %{answers: []}}}]
      assert MappedListDocumentAnswer.calculate(records, opts, %{}) == [nil]
    end

    test "wraps a single (non-list) answer value in a list", %{opts: opts} do
      records = [
        %{case: %{document: %{answers: [%{question_id: "tags-q", value: "tag-a"}]}}}
      ]

      assert MappedListDocumentAnswer.calculate(records, opts, %{}) == [["A"]]
    end

    test "handles multiple records independently", %{opts: opts} do
      records = [
        %{case: %{document: %{answers: [%{question_id: "tags-q", value: ["tag-a"]}]}}},
        %{case: %{document: %{answers: []}}},
        %{case: %{document: %{answers: [%{question_id: "tags-q", value: ["tag-b"]}]}}}
      ]

      assert MappedListDocumentAnswer.calculate(records, opts, %{}) == [["A"], nil, ["B"]]
    end

    test "uses canton-specific question_ids from context" do
      {:ok, opts} =
        MappedListDocumentAnswer.init(
          question_ids: %{default: "tags-q", gr: "gr-tags-q"},
          mapping: %{"tag-a" => "A"}
        )

      records = [
        %{case: %{document: %{answers: [%{question_id: "gr-tags-q", value: ["tag-a"]}]}}}
      ]

      assert MappedListDocumentAnswer.calculate(records, opts, %{canton: :gr}) == [["A"]]
    end
  end
end
