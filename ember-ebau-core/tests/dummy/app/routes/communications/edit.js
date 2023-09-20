import Route from "@ember/routing/route";

export default class CommunicationsEditRoute extends Route {
  model({ id }) {
    return id;
  }
}
