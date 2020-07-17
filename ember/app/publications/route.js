import Route from "@ember/routing/route";

export default Route.extend({
  setupController(controller, ...args) {
    this._super(...args);

    controller.publications.perform();
    controller.publicationPermissions.perform();
  },
});
