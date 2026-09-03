defmodule Ebau.MasterData.PlotDataRow do
  @moduledoc """
  Plot/parcel data (Parzelle) extracted from a Caluma table question.

  Contains the plot number, EGRID number, east/north coordinates, and
  postal code. Each row corresponds to one row document under the
  `parzellen` table question.

  The coordinates are used by `Ebau.Instances.Calculations.GisLinkForInstance`
  to overwrite the coordinates query parameter in GIS link URLs.
  """

  use Ash.Resource,
    otp_app: :ebau,
    domain: Ebau.MasterData,
    data_layer: AshPostgres.DataLayer,
    authorizers: Ash.Policy.Authorizer,
    extensions: [Caluma.Form.Extensions.Document]

  postgres do
    table "caluma_form_document"
    repo Ebau.Repo
    migrate? false
  end

  policies do
    policy action_type([:create, :update, :destroy]) do
      forbid_if always()
    end

    policy action_type(:read) do
      authorize_if accessing_from(Ebau.Instances.Instance, :plot_data)
    end
  end

  actions do
    defaults [:read]

    create :create do
      argument :document_id, :uuid, allow_nil?: false
      argument :plot_number, :string
      argument :egrid_number, :string
      argument :coord_east, :string
      argument :coord_north, :string
      argument :zip, :string

      change {Caluma.Form.Changes.AddTableRow,
              question: {Ebau.Instances.Instance, :plot_data}, document_argument: :document_id}

      change {Caluma.Form.Changes.SaveDocumentAnswers,
              answers: [:plot_number, :egrid_number, :coord_east, :coord_north, :zip]}
    end

    update :update do
      argument :plot_number, :string
      argument :egrid_number, :string
      argument :coord_east, :string
      argument :coord_north, :string
      argument :zip, :string

      change {Caluma.Form.Changes.SaveDocumentAnswers,
              answers: [:plot_number, :egrid_number, :coord_east, :coord_north, :zip]}
    end

    destroy :destroy do
      require_atomic? false

      # Destroy the answers before the row document itself: the Caluma tables
      # have no ON DELETE CASCADE, so deleting the document first would
      # violate their foreign keys.
      change cascade_destroy(:answers, after_action?: false, return_notifications?: false)

      change cascade_destroy(:answer_documents,
               after_action?: false,
               return_notifications?: false
             )
    end
  end

  caluma_document do
    answer :plot_number, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "parzellennummer"}}

    answer :egrid_number, :string,
      question_id: {Ebau.Caluma.CantonResolver, %{default: "e-grid", sg: "e-grid-nr"}}

    answer :coord_east, :string,
      question_id:
        {Ebau.Caluma.CantonResolver, %{default: "lagekoordinaten-ost", sg: "koordinaten-ost"}}

    answer :coord_north, :string,
      question_id:
        {Ebau.Caluma.CantonResolver, %{default: "lagekoordinaten-nord", sg: "koordinaten-nord"}}

    answer :zip, :string, question_id: {Ebau.Caluma.CantonResolver, %{default: "plz"}}
  end
end
