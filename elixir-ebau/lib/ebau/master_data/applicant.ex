defmodule Ebau.MasterData.Applicant do
  @moduledoc """
  Permit applicant (Bauherr/in) extracted from a Caluma table question.

  Contains personal details (name, address, contact info) and optional
  representative/proxy fields. Each row corresponds to one row document
  under the `bauherrin` table question in the Caluma form.

  In Django, this is the `applicants` resolver in
  `camac.instance.master_data.MasterData`.
  """

  use Ash.Resource,
    otp_app: :ebau,
    domain: Ebau.MasterData,
    data_layer: AshPostgres.DataLayer,
    authorizers: Ash.Policy.Authorizer,
    extensions: [
      Caluma.Form.Extensions.Document,
      Ebau.MasterData.PersonFields
    ]

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
      authorize_if {Ebau.Policies.Checks.HasActiveInstanceACL, via: [:family, :case]}
    end
  end

  # TODO: Fields requiring value_parser (not yet supported):
  # - salutation (anrede, option parser)
  # - country_code (land, value_mapping to country codes)
  # - is_juristic_person (juristische-person, value_mapping to boolean)
  # - has_representative (vertretung, value_mapping to boolean)
  # - representative_is_juristic_person (vertretung-juristische-person, value_mapping)
  # - representative_salutation (vertretung-anrede, option parser)
  # - representative_country_code (land, value_mapping)
end
