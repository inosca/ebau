defmodule Ebau.MasterData.Extensions.MasterDataTest do
  use ExUnit.Case, async: true

  alias Ebau.MasterData.Calculations
  alias Ebau.MasterData.Calculations.MappedListDocumentAnswer

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

      mapped_answer :category_code, :integer,
        question_ids: %{default: "category-q"},
        mapping: %{"choice-a" => 10, "choice-b" => 20}

      mapped_list_answer :tags, :string,
        question_ids: %{default: "tags-q"},
        mapping: %{"tag-a" => "A", "tag-b" => "B"}

      mapped_list_answer :code_tags, :integer,
        question_ids: %{default: "code-tags-q"},
        mapping: %{"tag-a" => 1, "tag-b" => 2}

      mapped_list_answer :canton_tags, :boolean,
        question_ids: %{default: "tags-q", gr: "gr-tags-q"},
        mapping: %{default: %{"tag-a" => true}, gr: %{"gr-tag-a" => true}}

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
      assert {Calculations.DocumentAnswer, _opts} = calc.calculation
    end

    test "passes question_ids to the calculation" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :proposal))
      {_mod, opts} = calc.calculation
      assert opts[:question_ids] == %{default: "proposal-q", gr: "gr-proposal-q"}
    end

    test "uses the declared Ash type" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :proposal))
      assert calc.type == Ash.Type.String
    end
  end

  describe "mapped_answer transformer" do
    test "adds a calculation for each mapped_answer declaration" do
      calc_names = TestResource |> Ash.Resource.Info.calculations() |> Enum.map(& &1.name)
      assert :is_paper in calc_names
    end

    test "uses MappedDocumentAnswer as the calculation module" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :is_paper))
      assert {Calculations.MappedDocumentAnswer, _opts} = calc.calculation
    end

    test "passes question_ids and mapping to the calculation" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :is_paper))
      {_mod, opts} = calc.calculation
      assert opts[:question_ids] == %{default: "is-paper-q"}
      assert opts[:mapping] == %{"is-paper-yes" => true, "is-paper-no" => false}
    end

    test "uses the declared Ash type" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :is_paper))
      assert calc.type == Ash.Type.Boolean
    end

    test "supports integer mapped values" do
      calc =
        Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :category_code))

      {_mod, opts} = calc.calculation

      assert calc.type == Ash.Type.Integer
      assert opts[:mapping] == %{"choice-a" => 10, "choice-b" => 20}
    end
  end

  describe "mapped_list_answer transformer" do
    test "adds a calculation for each mapped_list_answer declaration" do
      calc_names = TestResource |> Ash.Resource.Info.calculations() |> Enum.map(& &1.name)
      assert :tags in calc_names
    end

    test "uses MappedListDocumentAnswer as the calculation module" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :tags))
      assert {Calculations.MappedListDocumentAnswer, _opts} = calc.calculation
    end

    test "passes question_ids and mapping to the calculation" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :tags))
      {_mod, opts} = calc.calculation
      assert opts[:question_ids] == %{default: "tags-q"}
      assert opts[:mapping] == %{"tag-a" => "A", "tag-b" => "B"}
    end

    test "uses an array of the declared element type" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :tags))
      assert calc.type == {:array, Ash.Type.String}
    end

    test "supports integer mapped values" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :code_tags))
      {_mod, opts} = calc.calculation

      assert calc.type == {:array, Ash.Type.Integer}
      assert opts[:mapping] == %{"tag-a" => 1, "tag-b" => 2}
    end

    test "supports canton-specific mappings" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :canton_tags))
      {_mod, opts} = calc.calculation

      assert calc.type == {:array, Ash.Type.Boolean}
      assert opts[:mapping] == %{default: %{"tag-a" => true}, gr: %{"gr-tag-a" => true}}
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

    test "matches all configured question_ids, not just the default" do
      rel = Ash.Resource.Info.relationship(TestResource, :plot_data)
      filter = inspect(rel.filter)

      assert filter =~ "\"parzellen\""
      assert filter =~ "\"gr-parzellen\""
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

    test "uses canton-specific answer mappings from context" do
      {:ok, opts} =
        MappedListDocumentAnswer.init(
          question_ids: %{default: "tags-q", gr: "gr-tags-q"},
          mapping: %{default: %{"tag-a" => true}, gr: %{"gr-tag-a" => true}}
        )

      records = [
        %{case: %{document: %{answers: [%{question_id: "gr-tags-q", value: ["gr-tag-a"]}]}}}
      ]

      assert MappedListDocumentAnswer.calculate(records, opts, %{canton: :gr}) == [[true]]
    end

    test "declares the required relationship loads" do
      assert MappedListDocumentAnswer.load(%Ash.Query{}, [], %{}) == [case: [document: :answers]]
    end
  end
end
