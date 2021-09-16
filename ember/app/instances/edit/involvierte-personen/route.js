import Route from "@ember/routing/route";

export default class InstancesEditInvolviertePersonenRoute extends Route {
  afterModel(model) {
    if (model.meta["access-type"] === "public") {
      this.transitionTo("instances.edit.index");
    }
  }

  setupController(controller, model) {
    super.setupController(controller, model);
    const applicants = this.store.query("applicant", {
      instance: model.instance.get("id"),
    });
    controller.set("applicants", applicants);
  }
}
