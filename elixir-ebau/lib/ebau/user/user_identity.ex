defmodule Ebau.User.UserIdentity do
  use Ash.Resource,
    data_layer: AshPostgres.DataLayer,
    extensions: [AshAuthentication.UserIdentity],
    domain: Ebau.User

  user_identity do
    user_resource Ebau.User.User
  end

  postgres do
    table "user_identities"
    repo Ebau.Repo
  end
end
