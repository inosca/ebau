import Route from "@ember/routing/route";

export default class PublicationEditRoute extends Route {
  model({ work_item_id: workItemId }) {
    return { workItemId, ...this.modelFor("publication") };
  }
}
