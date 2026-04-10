defmodule Ebau.Instances.Instance do
  use Ash.Resource,
    otp_app: :ebau,
    domain: Ebau.Instances,
    data_layer: AshPostgres.DataLayer,
    extensions: [Ebau.MasterData.Extensions.MasterData],
    authorizers: Ash.Policy.Authorizer

  postgres do
    table "INSTANCE"
    repo Ebau.Repo
    migrate? false
  end

  master_data do
    # Tables
    table :plot_data, Ebau.MasterData.PlotDataRow, question_ids: %{default: "parzellen"}
    table :applicants, Ebau.MasterData.Applicant, question_ids: %{default: "bauherrin"}
    table :landowners, Ebau.MasterData.Landowner, question_ids: %{default: "grundeigentuemerin"}

    table :project_authors, Ebau.MasterData.ProjectAuthor,
      question_ids: %{default: "projektverfasserin"}

    table :invoice_recipients, Ebau.MasterData.InvoiceRecipient,
      question_ids: %{default: "rechnungsempfaengerin"}

    table :type_of_construction, Ebau.MasterData.TypeOfConstruction,
      question_ids: %{default: "gebaeude"}

    table :dwellings, Ebau.MasterData.Dwelling,
      question_ids: %{default: ["wohnungen", "wohnungen-v2"]}

    table :energy_devices, Ebau.MasterData.EnergyDevice,
      question_ids: %{default: "gebaeudetechnik"}

    # Answers
    mapped_answer :is_paper, :boolean,
      question_ids: %{default: "is-paper"},
      mapping: %{"is-paper-yes" => true, "is-paper-no" => false}

    answer :proposal, :string, question_ids: %{default: "umschreibung-bauprojekt"}
    answer :short_proposal, :string, question_ids: %{default: "kurzbeschreibung-bauprojekt"}
    answer :street, :string, question_ids: %{default: "strasse-flurname"}
    answer :street_number, :string, question_ids: %{default: "strasse-nummer"}
    answer :city, :string, question_ids: %{default: "ort"}
    answer :bfs_number, :string, question_ids: %{default: "gemeindenummer-bfs"}
    answer :construction_costs, :string, question_ids: %{default: "gesamtkosten"}

    answer :land_use_planning_land_use, :string,
      question_ids: %{default: "nutzungsplanung-grundnutzung"}

    answer :land_use_additional_determinations, :string,
      question_ids: %{default: "nutzungsplanung-weitere-festlegungen"}

    answer :land_use_planning_land_use_canton, :string,
      question_ids: %{default: "nutzungsplanung-grundnutzung-kanton"}

    answer :national_inventory, :string, question_ids: %{default: "bundesinventare"}

    # Case meta
    case_meta :dossier_number, :string, keys: %{default: "dossier-number"}
    case_meta :submit_date, :string, keys: %{default: "submit-date"}

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
    belongs_to :case, Caluma.Workflow.Case
    has_many :instance_acls, Ebau.Permissions.InstanceACL

    has_many :active_instance_acls, Ebau.Permissions.InstanceACL do
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
      authorize_if expr(exists(active_instance_acls, user_id == ^actor([:user, :id])))
    end

    policy action_type([:create, :update, :destroy]) do
      # Only used for testing for now
      forbid_if always()
    end
  end
end
