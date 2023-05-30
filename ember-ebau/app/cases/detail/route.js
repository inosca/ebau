import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class CasesDetailRoute extends Route {
  @service alexandriaConfig;
  @service ebauModules;

  model({ case_id }) {
    return parseInt(case_id);
  }

  afterModel(caseId) {
    this.alexandriaConfig.caseId = caseId;
    this.ebauModules.instanceId = caseId;
  }
}
