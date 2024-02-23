import Route from "@ember/routing/route";

export default class ConstructionMonitoringConstructionStageRoute extends Route {
  model({ construction_stage_id }) {
    return { constructionStageId: construction_stage_id };
  }
}
