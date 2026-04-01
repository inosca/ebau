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
    plug :store_language_header_in_session
  end

  pipeline :api do
    plug :accepts, ["json"]
    plug :load_from_bearer
  end

  scope "/", EbauWeb do
    pipe_through :browser

    ash_authentication_live_session :authentication_required,
      on_mount: [
        EbauWeb.InitialiseScope,
        EbauWeb.InitialiseLocale,
        {EbauWeb.LiveUserAuth, :live_user_required}
      ] do
      live "/test", LiveTest
    end

    auth_routes AuthController, Ebau.User.User, path: "/auth"
    sign_out_route AuthController

    get "/sign-in", AuthController, :sign_in
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

  def store_language_header_in_session(conn, _opts) do
    language_header = Plug.Conn.get_req_header(conn, "accept-language")

    if language_header == [] do
      conn
    else
      language_header
      |> List.first()
      |> String.split("-")
      |> List.first()
      |> then(fn locale ->
        Plug.Conn.put_session(conn, :locale, locale)
      end)
    end
  end
end
