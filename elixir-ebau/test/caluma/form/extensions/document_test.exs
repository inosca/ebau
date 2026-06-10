defmodule Caluma.Form.Extensions.DocumentTest do
  use ExUnit.Case, async: true

  defmodule TestResource do
    use Ash.Resource,
      otp_app: :ebau,
      data_layer: AshPostgres.DataLayer,
      extensions: [Caluma.Form.Extensions.Document],
      domain: nil

    postgres do
      table "caluma_form_document"
      repo Ebau.Repo
      migrate? false
    end
  end

  describe "transformer" do
    test "adds :id as a uuid primary key attribute" do
      attr = Enum.find(Ash.Resource.Info.attributes(TestResource), &(&1.name == :id))
      assert attr != nil
      assert attr.primary_key?
    end

    test "adds a primary :read action" do
      action = Enum.find(Ash.Resource.Info.actions(TestResource), &(&1.name == :read))
      assert action != nil
      assert action.primary?
    end

    test "adds a has_many :answers relationship to Caluma.Form.Answer" do
      rel = Ash.Resource.Info.relationship(TestResource, :answers)
      assert rel != nil
      assert rel.type == :has_many
      assert rel.destination == Caluma.Form.Answer
    end

    test "adds a has_many :answer_documents relationship to Caluma.Form.AnswerDocument" do
      rel = Ash.Resource.Info.relationship(TestResource, :answer_documents)
      assert rel != nil
      assert rel.type == :has_many
      assert rel.destination == Caluma.Form.AnswerDocument
    end

    test "adds a belongs_to :family relationship to Caluma.Form.Document" do
      rel = Ash.Resource.Info.relationship(TestResource, :family)
      assert rel != nil
      assert rel.type == :belongs_to
      assert rel.destination == Caluma.Form.Document
    end

    test "adds a :sort aggregate" do
      agg = Ash.Resource.Info.aggregate(TestResource, :sort)
      assert agg != nil
      assert agg.kind == :min
      assert agg.relationship_path == [:answer_documents]
      assert agg.field == :sort
    end
  end
end
