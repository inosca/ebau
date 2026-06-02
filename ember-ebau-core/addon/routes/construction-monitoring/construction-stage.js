import Route from "@ember/routing/route";

export default class ConstructionMonitoringConstructionStageRoute extends Route {
  model({ construction_stage_id: constructionStageId }) {
    return { constructionStageId };
  }
}
