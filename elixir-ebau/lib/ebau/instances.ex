defmodule Ebau.Instances do
  use Ash.Domain,
    otp_app: :ebau

  resources do
    resource Ebau.Instances.Instance

    resource Ebau.Instances.GisLinks do
      define :list_gis_links_for_instance, args: [:instance_id]
      define :create_gis_link
    end
  end
end
