import Route from "@ember/routing/route";

export default Route.extend({
  afterModel(model) {
    if (!model.meta["is-applicant"]) {
      this.transitionTo("instances.edit.index");
    }
  },

  setupController(controller, model) {
    this._super(...arguments);
    let applicants = this.store.query("applicant", {
      instance: model.instance.get("id")
    });
    controller.set("applicants", applicants);
  }
});
