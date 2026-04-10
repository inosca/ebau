defmodule Caluma.Form.Extensions.DocumentTest do
  use ExUnit.Case, async: true

  defmodule TestResource do
    use Ash.Resource,
      otp_app: :ebau,
      data_layer: AshPostgres.DataLayer,
      extensions: [Caluma.Form.Extensions.Document],
      domain: nil
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

    test "sets the postgres table to caluma_form_document" do
      assert AshPostgres.DataLayer.Info.table(TestResource) == "caluma_form_document"
    end

    test "sets the postgres repo to Ebau.Repo" do
      assert AshPostgres.DataLayer.Info.repo(TestResource) == Ebau.Repo
    end
  end
end
