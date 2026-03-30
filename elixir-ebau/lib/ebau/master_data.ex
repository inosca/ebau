defmodule Ebau.MasterData do
  use Ash.Domain,
    otp_app: :ebau

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
