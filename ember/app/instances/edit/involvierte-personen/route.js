import Route from "@ember/routing/route";

export default Route.extend({
  setupController(controller, model) {
    this._super(...arguments);
    let applicants = this.store.query("applicant", {
      instance: model.instance.get("id")
    });
    this.controller.set("applicants", applicants);
  }
});
