defmodule EbauWeb.ConnCase do
  @moduledoc """
  This module defines the test case to be used by
  tests that require setting up a connection.

  Such tests rely on `Phoenix.ConnTest` and also
  import other functionality to make it easier
  to build common data structures and query the data layer.

  Finally, if the test case interacts with the database,
  we enable the SQL sandbox, so changes done to the database
  are reverted at the end of every test. If you are using
  PostgreSQL, you can even run database tests asynchronously
  by setting `use EbauWeb.ConnCase, async: true`, although
  this option is not recommended for other databases.
  """

  use ExUnit.CaseTemplate

  using do
    quote do
      use EbauWeb, :verified_routes

      import EbauWeb.ConnCase
      import Phoenix.ConnTest
      import Plug.Conn
      # The default endpoint for testing
      @endpoint EbauWeb.Endpoint

      # Import conveniences for testing with connections
      @doc """
      Creates an authenticated REST API conn for REST API endpoint testing.

      Accepts an actor struct. Validation is faked by creating a valid token
      and writing that to the token cache.
      """
      @spec authenticated_rest_api_conn(Plug.Conn.t(), Ebau.Actor.t()) :: Plug.Conn.t()
      def authenticated_rest_api_conn(conn, actor) do
        token = valid_token()
        exp = System.system_time(:second) + 3600

        :ets.insert(:token_cache, {token, {:ok, actor.user}, exp})

        conn
        |> put_req_header("accept", "application/vnd.api+json")
        |> put_req_header("authorization", "Bearer #{token}")
        |> put_req_header("x-camac-group", Integer.to_string(actor.group.id))
        |> put_req_header("content-type", "application/vnd.api+json")
      end

      defp valid_token do
        now = System.system_time(:second)
        jwk = JOSE.JWK.from_oct("test")

        {_, token} =
          JOSE.JWT.sign(jwk, %{"alg" => "HS256"}, %{
            "sub" => "gis-links-test",
            "exp" => now + 3600
          })
          |> JOSE.JWS.compact()

        token
      end
    end
  end

  setup tags do
    Ebau.DataCase.setup_sandbox(tags)
    {:ok, conn: Phoenix.ConnTest.build_conn()}
  end
end
