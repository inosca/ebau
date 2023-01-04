import Route from "@ember/routing/route";

export default class DmsAdminEditRoute extends Route {
  model({ slug }) {
    return slug;
  }
}
