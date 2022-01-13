import Route from "@ember/routing/route";

export default class InstancesEditFormRoute extends Route {
  model({ form }) {
    return form;
  }

  resetController(controller) {
    controller.displayedForm = "";
  }
}
