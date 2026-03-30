defmodule Ebau.MasterData.ProjectAuthor do
  use Ash.Resource,
    otp_app: :ebau,
    domain: Ebau.MasterData,
    data_layer: AshPostgres.DataLayer,
    extensions: [Caluma.Form.Extensions.Document]

  use Ebau.MasterData.PersonalData
end
