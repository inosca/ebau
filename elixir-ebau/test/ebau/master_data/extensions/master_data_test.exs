defmodule Caluma.Workflow.Extensions.CaseTest do
  use ExUnit.Case, async: true

  alias Caluma.Form.Calculations

  defmodule TestCaseResource do
    @moduledoc "Test resource that IS the case (no `through`)."

    use Ash.Resource,
      otp_app: :ebau,
      domain: nil,
      data_layer: Ash.DataLayer.Simple,
      extensions: [Caluma.Workflow.Extensions.Case]

    resource do
      require_primary_key? false
    end

    caluma_case do
      caluma_document do
        answer :proposal, :string, question_id: "proposal-q"
      end

      meta do
        attribute :dossier_number, :string, key: "dossier-number"
      end
    end
  end

  defmodule TestResource do
    use Ash.Resource,
      otp_app: :ebau,
      domain: nil,
      data_layer: Ash.DataLayer.Simple,
      extensions: [Caluma.Workflow.Extensions.Case]

    resource do
      require_primary_key? false
    end

    caluma_case do
      through :case

      caluma_document do
        answer :proposal, :string,
          question_id: {Ebau.Caluma.CantonResolver, %{default: "proposal-q", gr: "gr-proposal-q"}}

        mapped_answer :is_paper, :boolean,
          question_id: "is-paper-q",
          mapping: %{"is-paper-yes" => true, "is-paper-no" => false}

        mapped_answer :category_code, :integer,
          question_id: "category-q",
          mapping: %{"choice-a" => 10, "choice-b" => 20}

        mapped_list_answer :tags, :string,
          question_id: "tags-q",
          mapping: %{"tag-a" => "A", "tag-b" => "B"}

        mapped_list_answer :code_tags, :float,
          question_id: "code-tags-q",
          mapping: %{"tag-a" => 1.5, "tag-b" => 2.8}

        mapped_list_answer :canton_tags, :boolean,
          question_id: {Ebau.Caluma.CantonResolver, %{default: "tags-q", gr: "gr-tags-q"}},
          mapping:
            {Ebau.Caluma.CantonResolver,
             %{default: %{"tag-a" => true}, gr: %{"gr-tag-a" => true}}}

        table :plot_data, Ebau.MasterData.PlotDataRow,
          question_id: {Ebau.Caluma.CantonResolver, %{default: "parzellen", gr: "gr-parzellen"}}
      end

      meta do
        attribute :dossier_number, :string,
          key: {Ebau.Caluma.CantonResolver, %{default: "dossier-number", gr: "gr-dossier"}}
      end
    end
  end

  describe "answer transformer" do
    test "adds a calculation for each answer declaration" do
      calc_names = TestResource |> Ash.Resource.Info.calculations() |> Enum.map(& &1.name)
      assert :proposal in calc_names
    end

    test "uses DocumentAnswer as the calculation module" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :proposal))
      assert {Calculations.DocumentAnswer, _opts} = calc.calculation
    end

    test "generates a has_one relationship with the question_id slugs in its filter" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :proposal))
      {_mod, opts} = calc.calculation
      rel_name = opts[:relationship]
      assert is_atom(rel_name)

      rel = Ash.Resource.Info.relationship(TestResource, rel_name)
      assert rel.type == :has_one
      assert rel.destination == Caluma.Form.Answer

      filter = inspect(rel.filter)
      # answer_filter uses opts[:default] only for resolver tuples; runtime resolution is TODO
      assert filter =~ "\"proposal-q\""
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

    test "generates a has_one with the question_id and passes mapping to the calc" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :is_paper))
      {_mod, opts} = calc.calculation
      assert opts[:mapping] == %{"is-paper-yes" => true, "is-paper-no" => false}

      rel = Ash.Resource.Info.relationship(TestResource, opts[:relationship])
      assert inspect(rel.filter) =~ "\"is-paper-q\""
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

    test "generates a has_one with the question_id and passes mapping to the calc" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :tags))
      {_mod, opts} = calc.calculation
      assert opts[:mapping] == %{"tag-a" => "A", "tag-b" => "B"}

      rel = Ash.Resource.Info.relationship(TestResource, opts[:relationship])
      assert inspect(rel.filter) =~ "\"tags-q\""
    end

    test "uses an array of the declared element type" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :tags))
      assert calc.type == {:array, Ash.Type.String}
    end

    test "supports float mapped values" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :code_tags))
      {_mod, opts} = calc.calculation

      assert calc.type == {:array, Ash.Type.Float}
      assert opts[:mapping] == %{"tag-a" => 1.5, "tag-b" => 2.8}
    end

    test "supports canton-specific mappings" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :canton_tags))
      {_mod, opts} = calc.calculation

      assert calc.type == {:array, Ash.Type.Boolean}

      assert opts[:mapping] ==
               {Ebau.Caluma.CantonResolver,
                %{default: %{"tag-a" => true}, gr: %{"gr-tag-a" => true}}}
    end
  end

  describe "meta transformer" do
    test "adds a calculation for each meta attribute declaration" do
      calc_names = TestResource |> Ash.Resource.Info.calculations() |> Enum.map(& &1.name)
      assert :dossier_number in calc_names
    end

    test "uses CaseMeta as the calculation module" do
      calc =
        Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :dossier_number))

      assert {Caluma.Workflow.Calculations.CaseMeta, _opts} = calc.calculation
    end

    test "passes key to the calculation" do
      calc =
        Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :dossier_number))

      {_mod, opts} = calc.calculation

      assert opts[:key] ==
               {Ebau.Caluma.CantonResolver, %{default: "dossier-number", gr: "gr-dossier"}}
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

    test "matches all configured question_id values, not just the default" do
      rel = Ash.Resource.Info.relationship(TestResource, :plot_data)
      filter = inspect(rel.filter)

      # table_filter uses opts[:default] only for resolver tuples; runtime resolution is TODO
      assert filter =~ "\"parzellen\""
    end
  end

  describe "MappedListDocumentAnswer.calculate/3" do
    alias Caluma.Form.Calculations.MappedListDocumentAnswer

    setup do
      {:ok, opts} =
        MappedListDocumentAnswer.init(
          relationship: :_tags_answer,
          mapping: %{"tag-a" => "A", "tag-b" => "B"}
        )

      %{opts: opts}
    end

    test "maps list answer values using the provided mapping", %{opts: opts} do
      records = [%{_tags_answer: %{value: ["tag-a", "tag-b"]}}]

      assert MappedListDocumentAnswer.calculate(records, opts, %{}) == [["A", "B"]]
    end

    test "returns nil when no matching answer is found", %{opts: opts} do
      records = [%{_tags_answer: nil}]
      assert MappedListDocumentAnswer.calculate(records, opts, %{}) == [nil]
    end

    test "wraps a single (non-list) answer value in a list", %{opts: opts} do
      records = [%{_tags_answer: %{value: "tag-a"}}]

      assert MappedListDocumentAnswer.calculate(records, opts, %{}) == [["A"]]
    end

    test "handles multiple records independently", %{opts: opts} do
      records = [
        %{_tags_answer: %{value: ["tag-a"]}},
        %{_tags_answer: nil},
        %{_tags_answer: %{value: ["tag-b"]}}
      ]

      assert MappedListDocumentAnswer.calculate(records, opts, %{}) == [["A"], nil, ["B"]]
    end

    @tag canton: :so
    test "uses canton-specific answer mappings" do
      {:ok, opts} =
        MappedListDocumentAnswer.init(
          relationship: :_tags_answer,
          mapping:
            {Ebau.Caluma.CantonResolver,
             %{default: %{"tag-a" => true}, so: %{"so-tag-a" => true}}}
        )

      records = [%{_tags_answer: %{value: ["so-tag-a"]}}]

      assert MappedListDocumentAnswer.calculate(records, opts, %{}) == [[true]]
    end

    test "declares the relationship to load" do
      opts = [relationship: :_my_rel]
      assert MappedListDocumentAnswer.load(%Ash.Query{}, opts, %{}) == [{:_my_rel, :value}]
    end
  end

  describe "through: nil (resource IS the case)" do
    test "adds a calculation for the answer declaration" do
      calc_names =
        TestCaseResource |> Ash.Resource.Info.calculations() |> Enum.map(& &1.name)

      assert :proposal in calc_names
    end

    test "has_one filter joins on `document_id`, not `<through>.document_id`" do
      calc =
        Enum.find(
          Ash.Resource.Info.calculations(TestCaseResource),
          &(&1.name == :proposal)
        )

      {_mod, opts} = calc.calculation

      rel = Ash.Resource.Info.relationship(TestCaseResource, opts[:relationship])
      filter = inspect(rel.filter)

      # Expect the parent ref to be plain `document_id` (no `:case.` prefix).
      assert filter =~ "parent(document_id)"
      refute filter =~ "case.document_id"
    end

    test "meta calculation passes through: nil" do
      calc =
        Enum.find(
          Ash.Resource.Info.calculations(TestCaseResource),
          &(&1.name == :dossier_number)
        )

      {Caluma.Workflow.Calculations.CaseMeta, opts} = calc.calculation
      assert opts[:through] == nil
      assert opts[:key] == "dossier-number"
    end
  end
end
