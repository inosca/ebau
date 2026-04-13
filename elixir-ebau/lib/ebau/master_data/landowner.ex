defmodule Ebau.MasterData.Landowner do
  @moduledoc """
  Property owner (Grundeigentuemer/in) extracted from a Caluma table question.

  Contains personal details (name, address, contact info) and optional
  representative/proxy fields. Each row corresponds to one row document
  under the `grundeigentuemerin` table question.
  """

  use Ash.Resource,
    otp_app: :ebau,
    domain: Ebau.MasterData,
    data_layer: AshPostgres.DataLayer,
    extensions: [
      Caluma.Form.Extensions.Document,
      Ebau.MasterData.PersonFields
    ]

  postgres do
    table "caluma_form_document"
    repo Ebau.Repo
    migrate? false
  end
end
