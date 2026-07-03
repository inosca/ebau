defmodule EbauWeb.Router do
  use EbauWeb, :router
  use AshAuthentication.Phoenix.Router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_live_flash
    plug :put_root_layout, html: {EbauWeb.Layouts, :root}
    plug :protect_from_forgery
    plug :put_secure_browser_headers
    plug :load_from_session
    plug EbauWeb.Plugs.InitialiseGettext
  end

  # LiveViews build their actor in `EbauWeb.LoadLiveContext`; only
  # plain controller routes need it on the conn.
  pipeline :actor do
    plug EbauWeb.Plugs.PutActorInSession
  end

  pipeline :api do
    plug :accepts, ["json"]
    plug EbauWeb.Plugs.KeycloakBearerAuth
  end

  scope "/api/v2" do
    pipe_through [:api]

    forward "/swaggerui", OpenApiSpex.Plug.SwaggerUI,
      path: "/api/v2/open_api",
      default_model_expand_depth: 4

    forward "/", EbauWeb.AshJsonApiRouter
  end

  scope "/", EbauWeb do
    pipe_through :browser

    ash_authentication_live_session :authentication_required,
      on_mount: [
        {EbauWeb.LiveUserAuth, :live_user_required},
        EbauWeb.Plugs.InitialiseGettext,
        EbauWeb.LoadLiveContext
      ] do
      live "/service-permissions/gis-links", Live.ServicePermissions.GisLinks
    end

    auth_routes AuthController, Ebau.User.User, path: "/auth"
    sign_out_route AuthController

    get "/sign-in", AuthController, :sign_in

    scope "/" do
      pipe_through :actor

      post "/switch-group/:id", GroupController, :switch
    end
  end

  # Other scopes may use custom stacks.
  # scope "/api", EbauWeb do
  #   pipe_through :api
  # end

  # Enable LiveDashboard and Swoosh mailbox preview in development
  if Application.compile_env(:ebau, :dev_routes) do
    # If you want to use the LiveDashboard in production, you should put
    # it behind authentication and allow only admins to access it.
    # If your application does not have an admins-only section yet,
    # you can use Plug.BasicAuth to set up some basic authentication
    # as long as you are also using SSL (which you should anyway).
    import Phoenix.LiveDashboard.Router

    scope "/dev" do
      pipe_through :browser

      live_dashboard "/dashboard", metrics: EbauWeb.Telemetry
      forward "/mailbox", Plug.Swoosh.MailboxPreview
    end
  end
end
