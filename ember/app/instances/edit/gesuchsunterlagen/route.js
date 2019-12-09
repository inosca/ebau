import Route from "@ember/routing/route";

export default Route.extend({
  afterModel(model) {
    if (!model.meta["is-applicant"]) {
      this.transitionTo("instances.edit.index");
    }
  },

  setupController(controller, model) {
    this._super(controller, model);
    controller.set("params", this.paramsFor("instances.edit"));
  }
});
