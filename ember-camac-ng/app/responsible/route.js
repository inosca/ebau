import Route from "@ember/routing/route";

export default class ResponsibleRoute extends Route {
  model({ instance_id }) {
    return instance_id;
  }
}
