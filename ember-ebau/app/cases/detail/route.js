import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class CasesDetailRoute extends Route {
  @service alexandriaConfig;
  model({ case_id }) {
    return case_id;
  }

  afterModel(caseId) {
    this.alexandriaConfig.caseId = caseId;
  }
}
