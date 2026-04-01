defmodule Ebau.Instances.Instance do
  use Ash.Resource,
    otp_app: :ebau,
    domain: Ebau.Instances,
    data_layer: AshPostgres.DataLayer,
    extensions: [Ebau.MasterData.Extension]

  postgres do
    table "INSTANCE"
    repo Ebau.Repo
    migrate? false
  end

  actions do
    defaults [:read]

    read :list_instances
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
  end

  # calculations do
  #   calculate :gis_links, {:array, :struct}, Ebau.Instances.Calculations.GisLinkForInstance
  # end


  master_data do
    # Tables
    table :plot_data, Ebau.MasterData.PlotDataRow, question_ids: ["parzellen"]
    table :applicants, Ebau.MasterData.Applicant, question_ids: ["bauherrin"]
    table :landowners, Ebau.MasterData.Landowner, question_ids: ["grundeigentuemerin"]
    table :project_authors, Ebau.MasterData.ProjectAuthor, question_ids: ["projektverfasserin"]
    table :invoice_recipients, Ebau.MasterData.InvoiceRecipient, question_ids: ["rechnungsempfaengerin"]
    table :type_of_construction, Ebau.MasterData.TypeOfConstruction, question_ids: ["gebaeude"]
    table :dwellings, Ebau.MasterData.Dwelling, question_ids: ["wohnungen", "wohnungen-v2"]
    table :energy_devices, Ebau.MasterData.EnergyDevice, question_ids: ["gebaeudetechnik"]

    # Answers
    answer :proposal, :string, question_ids: %{default: "umschreibung-bauprojekt"}
    answer :short_proposal, :string, question_ids: %{default: "kurzbeschreibung-bauprojekt"}
    answer :street, :string, question_ids: %{default: "strasse-flurname"}
    answer :street_number, :string, question_ids: %{default: "strasse-nummer"}
    answer :city, :string, question_ids: %{default: "ort"}
    answer :bfs_number, :string, question_ids: %{default: "gemeindenummer-bfs"}
    answer :construction_costs, :string, question_ids: %{default: "gesamtkosten"}
    answer :land_use_planning_land_use, :string, question_ids: %{default: "nutzungsplanung-grundnutzung"}
    answer :land_use_additional_determinations, :string, question_ids: %{default: "nutzungsplanung-weitere-festlegungen"}
    answer :land_use_planning_land_use_canton, :string, question_ids: %{default: "nutzungsplanung-grundnutzung-kanton"}
    answer :national_inventory, :string, question_ids: %{default: "bundesinventare"}

    # Case meta
    case_meta :dossier_number, :string, keys: %{default: "dossier-number"}
    case_meta :submit_date, :string, keys: %{default: "submit-date"}

    # TODO: Not yet supported by the DSL:
    # - static values (joined_street_and_number)
    # - value_parser/value_mapping (is_paper, category, municipality_name, municipality_slug)
    # - document_from_work_item (decision_date)
  end
end
