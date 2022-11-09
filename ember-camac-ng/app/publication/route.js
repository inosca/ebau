import Route from "@ember/routing/route";

export default class PublicationRoute extends Route {
  model({ instance_id, type }) {
    return { instanceId: parseInt(instance_id), type };
  }
}
