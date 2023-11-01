import Route from "@ember/routing/route";

export default class CasesIndexRoute extends Route {
  resetController(controller, isExiting, transition) {
    super.resetController(controller, isExiting, transition);

    if (isExiting) {
      controller.caseFilter = {};
    }
  }
}
