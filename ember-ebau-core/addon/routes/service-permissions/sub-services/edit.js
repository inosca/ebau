import Route from "@ember/routing/route";

export default class ServicePermissionsSubServicesEditRoute extends Route {
  model({ id }) {
    return id;
  }
}
