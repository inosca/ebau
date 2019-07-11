import Route from "@ember/routing/route";

export default Route.extend({
  model({ case_id }) {
    return parseInt(case_id);
  },

  setupController(controller) {
    this._super(...arguments);

    controller.data.perform();
    controller.instance.perform();
  },

  resetController(controller, isExiting) {
    if (isExiting) {
      controller.data.cancelAll({ resetState: true });
      controller.instance.cancelAll({ resetState: true });

      controller.set("displayedForm", null);
    }
  }
});
