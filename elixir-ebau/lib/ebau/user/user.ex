defmodule Ebau.User.User do
  @moduledoc false
  use Ash.Resource,
    otp_app: :ebau,
    domain: Ebau.User,
    authorizers: [Ash.Policy.Authorizer],
    extensions: [AshJsonApi.Resource, AshAuthentication],
    data_layer: AshPostgres.DataLayer

  authentication do
    tokens do
      enabled? true
      token_resource Ebau.User.Token
      signing_secret Ebau.Secrets
    end

    session_identifier :jti

    strategies do
      oidc :ebau do
        client_id System.get_env("KEYCLOAK_CLIENT", "camac")
        base_url System.get_env("KEYCLOAK_URL", "http://ebau-keycloak.localhost/auth/realms/ebau")
        redirect_uri "#{System.get_env("HOSTNAME", "http://ebau.localhost")}/elixir/auth/"
        registration_enabled? false
        # client_secret "not_needed"
      end
    end
  end

  postgres do
    table "USER"
    repo Ebau.Repo
    migrate? false
  end

  actions do
    defaults [:read]

    read :get_by_subject do
      description "Get a user by the subject claim in a JWT"
      argument :subject, :string, allow_nil?: false
      get? true
      prepare AshAuthentication.Preparations.FilterBySubject
    end

    read :sign_in_with_ebau do
      argument :user_info, :map, allow_nil?: false
      argument :oauth_tokens, :map, allow_nil?: false
      prepare AshAuthentication.Strategy.OAuth2.SignInPreparation

      filter expr(email == get_path(^arg(:user_info), [:email]))
    end
  end

  policies do
    bypass AshAuthentication.Checks.AshAuthenticationInteraction do
      authorize_if always()
    end

    policy do
      authorize_if actor_present()
      # authorize_if always()
    end
  end

  attributes do
    attribute :id, :integer,
      primary_key?: true,
      allow_nil?: false,
      sortable?: true,
      public?: true,
      source: :USER_ID

    attribute :username, :string,
      public?: true,
      allow_nil?: false,
      source: :USERNAME

    attribute :email, :string, source: :EMAIL
    attribute :name, :string, public?: true, source: :NAME
    attribute :surname, :string, public?: true, source: :SURNAME
    attribute :language, :string, public?: true, source: :LANGUAGE, allow_nil?: false
  end

  json_api do
    type "user"
  end
end
