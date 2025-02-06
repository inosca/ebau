import Route from "@ember/routing/route";

export default class SnippetsAdminEditRoute extends Route {
  model({ id }) {
    return id;
  }
}
