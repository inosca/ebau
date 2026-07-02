defmodule Ebau.MasterData do
  @moduledoc """
  Ash domain for read-only master data extracted from Caluma form documents.

  Master data is an abstraction layer that normalizes Caluma form answers into
  typed, structured records. Each canton uses different Caluma question slugs
  for the same logical data (e.g. "bauherrschaft" vs "personalien-gesuchstellerin"
  for applicants). The master data layer maps these canton-specific slugs to a
  uniform interface.

  Master data records are **not persisted in their own tables**. They are
  computed at query time from Caluma `caluma_form_document` rows via
  Ash calculations and relationships declared on `Ebau.Instances.Instance`.

  The Django equivalent is `camac.instance.master_data.MasterData` which uses a
  resolver/parser system to achieve the same normalization.

  ## Resources

  | Resource | Description |
  |---|---|
  | `PlotDataRow` | Plot/parcel info (number, EGRID, coordinates) |
  | `Applicant` | Permit applicant (person or organization) |
  | `Landowner` | Property owner |
  | `ProjectAuthor` | Architect or project designer |
  | `InvoiceRecipient` | Fee invoice recipient |
  | `TypeOfConstruction` | Building type classification |
  | `Dwelling` | Residential unit details |
  | `EnergyDevice` | HVAC/energy system info |

  ## How it works

  The `Caluma.Workflow.Extensions.Case` Spark DSL extension is applied to
  `Instance`. It reads `caluma_case do ... end` declarations and generates
  relationships (for table questions) and calculations (for scalar answers)
  at compile time.

  Each master data resource uses `Caluma.Form.Extensions.Document` to
  declare its fields. This maps Caluma question slugs to Ash calculations.

  See the [Ash Domains guide](ash-domains.html) for general domain usage.
  """

  use Ash.Domain,
    otp_app: :ebau

  authorization do
    authorize :by_default
    require_actor? true
  end

  resources do
    resource Ebau.MasterData.PlotDataRow
    resource Ebau.MasterData.Applicant
    resource Ebau.MasterData.Landowner
    resource Ebau.MasterData.ProjectAuthor
    resource Ebau.MasterData.InvoiceRecipient
    resource Ebau.MasterData.TypeOfConstruction
    resource Ebau.MasterData.Dwelling
    resource Ebau.MasterData.EnergyDevice
  end
end
