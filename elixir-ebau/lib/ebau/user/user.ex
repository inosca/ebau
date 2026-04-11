defmodule Ebau.User.User do
  @moduledoc """
  User resource.
  """
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
        client_id Ebau.Secrets
        base_url Ebau.Secrets
        authorization_params Ebau.Secrets
        redirect_uri Ebau.Secrets
        registration_enabled? false
      end
    end
  end

  relationships do
    many_to_many :groups, Ebau.User.Group do
      through Ebau.User.UserGroup
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
      prepare AshAuthentication.Strategy.OAuth2.SignInPreparation

      filter expr(email == get_path(^arg(:user_info), [:email]))
    end
  end

  policies do
    bypass AshAuthentication.Checks.AshAuthenticationInteraction do
      authorize_if always()
    end

    policy action(:read) do
      # Example on how to only allow reading your own user
      authorize_if expr(id == ^actor(:id))
    end

    policy action_type([:create, :update, :destroy]) do
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

    attribute :language, :string,
      public?: true,
      allow_nil?: false,
      constraints: [max_length: 2],
      source: :LANGUAGE
  end

  json_api do
    type "user"
  end

  identities do
    identity :unique_email, [:email]
  end
end
