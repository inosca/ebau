import Route from "@ember/routing/route";

export default class AdditionalDemandDetailRoute extends Route {
  model({ id }) {
    return id;
  }
}
