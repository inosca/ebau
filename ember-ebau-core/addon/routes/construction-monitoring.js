import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class ConstructionMonitoringRoute extends Route {
  @service constructionMonitoring;
  @service router;
  @service ebauModules;

  async afterModel(model, transition) {
    // Work-item direct links contain a url that is used
    // to transition to the relevant construction stage / step.
    // In this case we don't want to redirect to the latest
    // construction stage / step.
    if (
      !["construction-monitoring", "construction-monitoring.index"].includes(
        transition.to.name,
      )
    ) {
      return super.afterModel(model, transition);
    }
    if (transition.intent.url) {
      return super.afterModel(model, transition);
    }

    await this.constructionMonitoring.redirectToLatestConstructionStageStep();
  }
}
