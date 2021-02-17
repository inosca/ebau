import Route from "@ember/routing/route";

export default class PublicationEditRoute extends Route {
  model({ workitem_uuid }) {
    return workitem_uuid;
  }

  setupController(controller, model) {
    super.setupController(controller, model);

    controller.fetchCreateWorkItem.perform();
    controller.fetchPublication.perform();
  }
}
