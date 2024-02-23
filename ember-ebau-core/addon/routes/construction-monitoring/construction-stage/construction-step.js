import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";

export default class ConstructionMonitoringConstructionStageConstructionStepRoute extends Route {
  @service constructionMonitoring;
  @service ebauModules;

  async model({ construction_step_id }) {
    const constructionStageId = this.modelFor(
      this.ebauModules.resolveModuleRoute(
        "construction-monitoring",
        "construction-stage",
      ),
    )?.constructionStageId;
    // Need to fetch stages, in case route is accessed through direct link
    this.constructionMonitoring.refetchConstructionStages();
    await this.constructionMonitoring.fetchConstructionStages.last;
    const constructionStageChildCaseId = decodeId(
      this.constructionMonitoring.findConstructionStage(constructionStageId)
        ?.childCase.id,
    );
    return {
      constructionStageId,
      constructionStageChildCaseId,
      constructionStepId: construction_step_id,
    };
  }
}
