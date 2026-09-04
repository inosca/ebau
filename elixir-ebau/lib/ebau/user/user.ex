defmodule Ebau.User.User do
  @moduledoc """
  A CAMAC user from the legacy `USER` table.

  Authenticates via OIDC (Keycloak) using `AshAuthentication`. Users
  are not created through the Elixir app; they are managed by
  Keycloak and synced into the `USER` table by Django.

  Users belong to groups via `Ebau.User.UserGroup`. The authenticated
  user becomes `actor.user` in the `Ebau.Actor` struct.
  """
  use Ash.Resource,
    otp_app: :ebau,
    domain: Ebau.User,
    authorizers: Ash.Policy.Authorizer,
    extensions: [AshAuthentication],
    data_layer: AshPostgres.DataLayer

  authentication do
    tokens do
      enabled? true
      token_resource Ebau.User.Token
      signing_secret Ebau.Secrets
      store_all_tokens? true
      require_token_presence_for_authentication? true

      # Matches Keycloak's `ssoSessionMaxLifespan`. Keycloak only sends a
      # back-channel logout token on an explicit logout, never when a session
      # expires (keycloak#25171), so without this a session here would outlive
      # the Keycloak session that created it by the default 14 days.
      token_lifetime {10, :hours}
    end

    strategies do
      oidc :ebau do
        client_id Ebau.Secrets
        client_secret Ebau.Secrets
        base_url Ebau.Secrets
        authorization_params Ebau.Secrets
        redirect_uri Ebau.Secrets
        registration_enabled? false
        trust_email_verified? true
        code_verifier true
        identity_resource Ebau.User.UserIdentity
      end
    end
  end

  relationships do
    many_to_many :groups, Ebau.User.Group do
      through Ebau.User.UserGroup
      sort :name
    end

    has_many :user_groups, Ebau.User.UserGroup

    has_one :default_user_group, Ebau.User.UserGroup do
      filter expr(default_group == 1)
      # The legacy table has no unique constraint on the default flag,
      # so pick deterministically if duplicates ever exist.
      sort id: :asc
      from_many? true
    end

    has_one :default_group, Ebau.User.Group do
      through [:default_user_group, :group]
    end
  end

  postgres do
    table "USER"
    repo Ebau.Repo
    migrate? false
  end

  actions do
    defaults [:read, create: :*]

    read :get_by_subject do
      description "Get a user by the subject claim in a JWT"
      argument :subject, :string, allow_nil?: false
      get? true
      prepare AshAuthentication.Preparations.FilterBySubject
    end

    read :sign_in_with_ebau do
      argument :user_info, :map, allow_nil?: false
      argument :oauth_tokens, :map, allow_nil?: false
      prepare Ebau.User.Preparations.TrustKeycloakEmail
      # Read after_action hooks run in reverse order of registration, so this
      # must come before `SignInPreparation`, whose token it records.
      prepare Ebau.User.Preparations.RecordKeycloakSession
      prepare AshAuthentication.Strategy.OAuth2.SignInPreparation
      prepare Ebau.User.Preparations.SignInFilter
    end

    update :set_default_language do
      accept [:language]
    end
  end

  policies do
    bypass AshAuthentication.Checks.AshAuthenticationInteraction do
      authorize_if always()
    end

    policy action(:read) do
      authorize_if expr(id == ^actor([:user, :id]))
    end

    policy action(:set_default_language) do
      authorize_if expr(id == ^actor([:user, :id]))
    end

    policy action([:create, :update, :destroy]) do
      # We don't allow creating users. This is only for testing at the moment
      forbid_if always()
    end
  end

  attributes do
    integer_primary_key :id do
      source :USER_ID
    end

    attribute :username, :string,
      public?: true,
      allow_nil?: false,
      constraints: [max_length: 250],
      source: :USERNAME

    attribute :email, :string, constraints: [max_length: 100], source: :EMAIL

    attribute :name, :string,
      public?: true,
      allow_nil?: false,
      constraints: [max_length: 100],
      source: :NAME

    attribute :surname, :string,
      public?: true,
      allow_nil?: false,
      constraints: [max_length: 100],
      source: :SURNAME

    attribute :language, :atom,
      public?: true,
      allow_nil?: false,
      constraints: [one_of: [:de, :fr, :it]],
      source: :LANGUAGE
  end

  identities do
    identity :unique_email, [:email]
  end
end
