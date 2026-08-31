defmodule Caluma.Form.Extensions.Document.InfoTest do
  use ExUnit.Case, async: true

  alias Caluma.Form.Extensions.Document
  alias Caluma.Form.Extensions.Document.Info

  defmodule CaseResource do
    use Ash.Resource,
      otp_app: :ebau,
      domain: nil,
      data_layer: AshPostgres.DataLayer,
      extensions: [Caluma.Workflow.Extensions.Case]

    postgres do
      table "caluma_workflow_case"
      repo Ebau.Repo
      migrate? false
    end

    attributes do
      uuid_primary_key :id
      attribute :document_id, :uuid
    end

    caluma_case do
      caluma_document do
        answer :proposal, :string, question_id: ["umschreibung", "umschreibung-v2"]
      end
    end
  end

  describe "caluma_document/1" do
    test "lists the entities of a document resource" do
      names = Caluma.Test.Document |> Info.caluma_document() |> Enum.map(& &1.name)
      assert names == [:title, :is_paper, :tags, :rows]
    end

    test "falls back to the caluma_case nesting" do
      assert [%Document.Answer{name: :proposal}] = Info.caluma_document(CaseResource)
    end
  end

  describe "entity/2" do
    test "finds an entity by name" do
      assert {:ok, %Document.Table{name: :rows, resource: Caluma.Test.Row}} =
               Info.entity(Caluma.Test.Document, :rows)
    end

    test "is :error for unknown names" do
      assert Info.entity(Caluma.Test.Document, :nope) == :error
    end

    test "entity!/2 raises for unknown names" do
      assert_raise ArgumentError, ~r/no caluma_document entity :nope/, fn ->
        Info.entity!(Caluma.Test.Document, :nope)
      end
    end
  end

  describe "question_slug/2" do
    test "resolves the current slug of an entity" do
      assert Info.question_slug(Caluma.Test.Document, :rows) == {:ok, "rows"}
      assert Info.question_slug(CaseResource, :proposal) == {:ok, "umschreibung-v2"}
    end

    test "is :error for unknown names" do
      assert Info.question_slug(Caluma.Test.Document, :nope) == :error
    end

    test "question_slug!/2 returns the slug or raises" do
      assert Info.question_slug!(Caluma.Test.Document, :is_paper) == "is-paper"

      assert_raise ArgumentError, fn -> Info.question_slug!(Caluma.Test.Document, :nope) end
    end
  end
end
