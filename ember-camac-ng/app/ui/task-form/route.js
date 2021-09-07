import Route from "@ember/routing/route";

export default class TaskFormRoute extends Route {
  model({ instance_id: instanceId, task }) {
    return { instanceId, task };
  }

  setupController(controller, model) {
    super.setupController(controller, model);

    controller.fetchWorkItem.perform();
  }
}
