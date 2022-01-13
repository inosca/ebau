import Route from "@ember/routing/route";
import { next } from "@ember/runloop";

export default class InstancesEditIndexRoute extends Route {
  model() {
    return this.modelFor("instances.edit");
  }

  redirect() {
    next(async () => {
      // eslint-disable-next-line ember/no-controller-access-in-routes
      const controller = this.controllerFor("instances.edit");
      const instance = await controller.instance;

      // redirect directly to the main form if the app is embedded
      if (instance && instance.mainForm && controller.embedded) {
        this.replaceWith("instances.edit.form", instance.mainForm.slug);
      }
    });
  }
}
