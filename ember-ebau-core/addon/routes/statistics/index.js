import Route from "@ember/routing/route";

export default class StatisticsIndexRoute extends Route {
  queryParams = { from: { refresh: true }, to: { refresh: true } };

  setupController(controller, model) {
    super.setupController(controller, model);

    controller.fetchInstancesSummary.perform();
    controller.fetchClaimsSummary.perform();
  }

  resetController(controller, isExiting) {
    if (isExiting) {
      controller.from = "";
      controller.to = "";
    }
  }
}
