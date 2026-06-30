defmodule Ebau.Instances.Instance do
  @moduledoc """
  The central building permit application entity, backed by the legacy
  `INSTANCE` table.

  Each instance belongs to a Caluma `Case` (which holds the workflow state)
  and a Caluma `Document` (which holds the form answers). Access is
  controlled through `Ebau.Permissions.InstanceACL` records.

  The `Caluma.Workflow.Extensions.Case` Spark extension is applied here. It
  reads the `caluma_case do ... end` block and generates relationships
  (for table questions like applicants or plots) and calculations (for
  scalar answers like street or proposal) at compile time. This gives a
  typed, uniform interface over canton-specific Caluma question slugs.
  """

  use Ash.Resource,
    otp_app: :ebau,
    domain: Ebau.Instances,
    data_layer: AshPostgres.DataLayer,
    extensions: [Caluma.Workflow.Extensions.Case],
    authorizers: Ash.Policy.Authorizer

  postgres do
    table "INSTANCE"
    repo Ebau.Repo
    migrate? false
  end

  caluma_case do
    through :case

    caluma_document do
      # Tables
      table :plot_data, Ebau.MasterData.PlotDataRow,
        question_id: {Ebau.Caluma.CantonResolver, %{default: "parzellen"}}

      table :applicants, Ebau.MasterData.Applicant,
        question_id: {Ebau.Caluma.CantonResolver, %{default: "bauherrin"}}

      table :landowners, Ebau.MasterData.Landowner,
        question_id: {Ebau.Caluma.CantonResolver, %{default: "grundeigentuemerin"}}

      table :project_authors, Ebau.MasterData.ProjectAuthor,
        question_id: {Ebau.Caluma.CantonResolver, %{default: "projektverfasserin"}}

      table :invoice_recipients, Ebau.MasterData.InvoiceRecipient,
        question_id: {Ebau.Caluma.CantonResolver, %{default: "rechnungsempfaengerin"}}

      table :type_of_construction, Ebau.MasterData.TypeOfConstruction,
        question_id: {Ebau.Caluma.CantonResolver, %{default: "gebaeude"}}

      table :dwellings, Ebau.MasterData.Dwelling,
        question_id: {Ebau.Caluma.CantonResolver, %{default: ["wohnungen", "wohnungen-v2"]}}

      table :energy_devices, Ebau.MasterData.EnergyDevice,
        question_id: {Ebau.Caluma.CantonResolver, %{default: "gebaeudetechnik"}}

      # Answers
      mapped_answer :is_paper, :boolean,
        question_id: {Ebau.Caluma.CantonResolver, %{default: "is-paper"}},
        mapping: %{"is-paper-yes" => true, "is-paper-no" => false}

      answer :proposal, :string,
        question_id: {Ebau.Caluma.CantonResolver, %{default: "umschreibung-bauprojekt"}}

      answer :short_proposal, :string,
        question_id: {Ebau.Caluma.CantonResolver, %{default: "kurzbeschreibung-bauprojekt"}}

      answer :street, :string,
        question_id: {Ebau.Caluma.CantonResolver, %{default: "strasse-flurname"}}

      answer :street_number, :string,
        question_id: {Ebau.Caluma.CantonResolver, %{default: "strasse-nummer"}}

      answer :city, :string, question_id: {Ebau.Caluma.CantonResolver, %{default: "ort"}}

      answer :bfs_number, :string,
        question_id: {Ebau.Caluma.CantonResolver, %{default: "gemeindenummer-bfs"}}

      answer :construction_costs, :string,
        question_id: {Ebau.Caluma.CantonResolver, %{default: "gesamtkosten"}}

      answer :land_use_planning_land_use, :string,
        question_id: {Ebau.Caluma.CantonResolver, %{default: "nutzungsplanung-grundnutzung"}}

      answer :land_use_additional_determinations, :string,
        question_id:
          {Ebau.Caluma.CantonResolver, %{default: "nutzungsplanung-weitere-festlegungen"}}

      answer :land_use_planning_land_use_canton, :string,
        question_id:
          {Ebau.Caluma.CantonResolver, %{default: "nutzungsplanung-grundnutzung-kanton"}}

      answer :national_inventory, :string,
        question_id: {Ebau.Caluma.CantonResolver, %{default: "bundesinventare"}}
    end

    meta do
      attribute :dossier_number, :string,
        key: {Ebau.Caluma.CantonResolver, %{default: "dossier-number"}}

      attribute :submit_date, :string,
        key: {Ebau.Caluma.CantonResolver, %{default: "submit-date"}}
    end

    # TODO: Not yet supported by the DSL:
    # - static values (joined_street_and_number)
    # - document_from_work_item (decision_date)
  end

  attributes do
    integer_primary_key :id, source: :INSTANCE_ID
    create_timestamp :inserted_at, source: :CREATION_DATE, allow_nil?: false
    update_timestamp :modified_at, source: :MODIFICATION_DATE, allow_nil?: false

    attribute :form_id, :integer do
      source :FORM_ID
      allow_nil? false
      default 1

      description "Dummy value for legacy column that can't be null. Only required for testing for now."
    end

    attribute :group_id, :integer do
      source :GROUP_ID
      allow_nil? false
      default 1

      description "Dummy value for legacy column that can't be null. Only required for testing for now."
    end

    attribute :instance_state_id, :integer do
      source :INSTANCE_STATE_ID
      allow_nil? false
      default 1

      description "Dummy value for legacy column that can't be null. Only required for testing for now."
    end

    attribute :previous_instance_state_id, :integer do
      source :PREVIOUS_INSTANCE_STATE_ID
      allow_nil? false
      default 1

      description "Dummy value for legacy column that can't be null. Only required for testing for now."
    end

    attribute :user_id, :integer do
      source :USER_ID
      allow_nil? false
      default 1

      description "Dummy value for legacy column that can't be null. Only required for testing for now."
    end
  end

  relationships do
    belongs_to :case, Caluma.Workflow.Case, domain: Caluma.Workflow
    has_many :instance_acls, Ebau.Permissions.InstanceACL, domain: Ebau.Permissions

    has_many :active_instance_acls, Ebau.Permissions.InstanceACL do
      domain Ebau.Permissions
      read_action :active
    end
  end

  actions do
    defaults [:read, :destroy, create: :*, update: :*]

    read :list_instances

    create :create_instance do
      argument :case, :map

      change manage_relationship(:case, type: :append)
    end
  end

  policies do
    policy action_type(:read) do
      authorize_if {Ebau.Policies.Checks.HasActiveInstanceACL, via: []}
    end

    policy action_type([:create, :update, :destroy]) do
      # Only used for testing for now
      forbid_if always()
    end
  end
end
