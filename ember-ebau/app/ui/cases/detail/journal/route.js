import Route from "@ember/routing/route";

export default class JournalRoute extends Route {
  model() {
    return this.modelFor("cases.detail");
  }

  setupController(controller, model) {
    super.setupController(controller, model);

    controller.refetchEntries();
  }
}
