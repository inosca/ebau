defmodule EbauWeb.AshJsonApiRouter do
  use AshJsonApi.Router,
    domains: [Ebau.User],
    open_api: "/open_api"
end
