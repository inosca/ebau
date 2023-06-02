import Route from "@ember/routing/route";

export default class CommunicationsRoute extends Route {
  model({ instance_id }) {
    return instance_id;
  }
}
