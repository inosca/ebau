import Route from "@ember/routing/route";

export default class AuditRoute extends Route {
  model({ instance_id }) {
    return parseInt(instance_id);
  }
}
