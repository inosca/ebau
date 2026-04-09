defmodule Ebau.Instances do
  use Ash.Domain,
    otp_app: :ebau,
    extensions: [AshJsonApi.Domain]

  resources do
    resource Ebau.Instances.Instance

    resource Ebau.Instances.GisLink do
      define :list_gis_links_for_instance, args: [:instance_id]
      define :create_gis_link
      define :read_gis_links
    end
  end

  json_api do
    routes do
      base_route "/gis-links", Ebau.Instances.GisLink do
        index :read_gis_links
        delete :destroy_gis_link
        post :create_gis_link, relationship_arguments: [:service]
      end
    end
  end
end
