import Route from "@ember/routing/route";

export default class CasesDetailWorkItemsNewRoute extends Route {
  model({ work_item_id: id }) {
    return id;
  }

  resetController(controller, isExiting) {
    if (isExiting) {
      controller.fetchWorkItems.cancelAll({ resetState: true });
    }
  }
}
