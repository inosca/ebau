import Route from "@ember/routing/route";

export default class CasesDetailRoute extends Route {
  model({ instance_id }) {
    return instance_id;
  }
}
