import Route from "@ember/routing/route";

export default Route.extend({
  afterModel(model) {
    if (model.meta["access-type"] === "public") {
      this.transitionTo("instances.edit.index");
    }
  },

  setupController(controller, model) {
    this._super(controller, model);
    controller.set("params", this.paramsFor("instances.edit"));
    // We have to compare to "true" because localStorage returns strings
    controller.set(
      "visible",
      localStorage.getItem("hideDocumentInfo") !== "true"
    );
    controller.set(
      "hideDocumentInfo",
      localStorage.getItem("hideDocumentInfo") === "true"
    );
  },
});
