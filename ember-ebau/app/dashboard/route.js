import Route from "@ember/routing/route";

export default class DashboardRoute extends Route {
  model({ type }) {
    return type;
  }
}
