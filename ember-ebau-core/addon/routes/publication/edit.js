import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class PublicationEditRoute extends Route {
  @service ebauModules;

  model({ work_item_id: workItemId }) {
    return {
      workItemId,
      ...this.modelFor(
        this.ebauModules.resolveModuleRoute("publication", "publication"),
      ),
    };
  }
}
