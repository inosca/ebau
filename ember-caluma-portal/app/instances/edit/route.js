import Route from "@ember/routing/route";

export default class InstancesEditRoute extends Route {
  model({ instance }) {
    return parseInt(instance);
  }
}
