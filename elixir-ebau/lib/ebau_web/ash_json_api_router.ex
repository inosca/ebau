defmodule EbauWeb.AshJsonApiRouter do
  use AshJsonApi.Router,
    domains: [Ebau.User, Ebau.Instances],
    open_api: "/open_api"
end
