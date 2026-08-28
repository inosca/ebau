defmodule Ebau.User.Token do
  @moduledoc """
  AshAuthentication token store, doubling as the map from Keycloak SSO
  sessions to Phoenix sessions.

  `store_all_tokens?` writes one row per sign-in, keyed by the token's `jti`.
  Keycloak's back-channel logout token identifies the session being ended by
  its `sid`, so `Ebau.User.Preparations.RecordKeycloakSession` stores the
  `sid` and the raw `id_token` in `extra_data` at sign-in. A logout token can
  then find every Phoenix session belonging to that `sid`, and sign-out can
  hand the `id_token` back to Keycloak as `id_token_hint`.

  Expired rows are removed by `AshAuthentication.TokenResource.Expunger`.
  """
  use Ash.Resource,
    otp_app: :ebau,
    domain: Ebau.User,
    authorizers: Ash.Policy.Authorizer,
    extensions: [AshAuthentication.TokenResource],
    data_layer: AshPostgres.DataLayer

  postgres do
    table "tokens"
    repo Ebau.Repo
  end

  actions do
    defaults [:read]

    read :expired do
      description "Look up all expired tokens."
      filter expr(expires_at < now())
    end

    read :get_token do
      description "Look up a token by JTI or token, and an optional purpose."
      get? true
      argument :token, :string, sensitive?: true
      argument :jti, :string, sensitive?: true
      argument :purpose, :string, sensitive?: false

      prepare AshAuthentication.TokenResource.GetTokenPreparation
    end

    read :by_keycloak_sid do
      description "All live session tokens belonging to one Keycloak SSO session."
      argument :sid, :string, allow_nil?: false

      filter expr(purpose == "user" and extra_data[:sid] == ^arg(:sid))
    end

    action :revoked?, :boolean do
      description "Returns true if a revocation token is found for the provided token"
      argument :token, :string, sensitive?: true
      argument :jti, :string, sensitive?: true

      run AshAuthentication.TokenResource.IsRevoked
    end

    create :revoke_token do
      description "Revoke a token. Creates a revocation token corresponding to the provided token."
      accept [:extra_data]
      argument :token, :string, allow_nil?: false, sensitive?: true

      change AshAuthentication.TokenResource.RevokeTokenChange
    end

    create :store_token do
      description "Stores a token used for the provided purpose."
      accept [:extra_data, :purpose]
      argument :token, :string, allow_nil?: false, sensitive?: true
      change AshAuthentication.TokenResource.StoreTokenChange
    end

    update :set_keycloak_session do
      description "Attaches (or with `nil`, detaches) the Keycloak `sid` and `id_token`."
      accept [:extra_data]
    end

    destroy :expunge_expired do
      description "Deletes expired tokens."
      change filter expr(expires_at < now())
    end
  end

  policies do
    bypass AshAuthentication.Checks.AshAuthenticationInteraction do
      description "AshAuthentication can interact with the token resource"
      authorize_if always()
    end

    bypass action([:get_token, :by_keycloak_sid, :set_keycloak_session]) do
      description "Sign-in, sign-out and back-channel logout run on behalf of no user"
      authorize_if Ebau.Policies.Checks.ActorIsSystem
    end

    policy always() do
      description "No one aside from AshAuthentication can interact with the tokens resource."
      forbid_if always()
    end
  end

  attributes do
    attribute :jti, :string do
      primary_key? true
      public? true
      allow_nil? false
      sensitive? true
    end

    attribute :subject, :string do
      allow_nil? false
    end

    attribute :expires_at, :utc_datetime do
      allow_nil? false
    end

    attribute :purpose, :string do
      allow_nil? false
      public? true
    end

    attribute :extra_data, :map do
      public? true
    end

    timestamps()
  end
end
