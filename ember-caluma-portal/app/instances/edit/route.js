import Route from "@ember/routing/route";

export default Route.extend({
  model({ case_id }) {
    return {
      caseId: case_id
    };
  },

  setupController(controller, model) {
    this._super(controller, model);

    controller.data.perform(model.caseId);
    controller.feedbackData.perform(model.caseId);
  }
});
