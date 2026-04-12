defmodule EbauWeb.AshJsonApiRouter do
  use AshJsonApi.Router,
    domains: [Ebau.Instances],
    open_api: "/open_api"
end
