import Route from "@ember/routing/route";

export default class DmsGenerateRoute extends Route {
  model({ instance_id: instanceId }) {
    return instanceId;
  }
}
