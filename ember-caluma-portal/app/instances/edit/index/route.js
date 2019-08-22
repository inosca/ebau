import Route from "@ember/routing/route";
import { next } from "@ember/runloop";

export default Route.extend({
  redirect() {
    next(async () => {
      const controller = this.controllerFor("instances.edit");
      const instance = await controller.instanceTask.last;

      if (instance.mainForm) {
        this.replaceWith("instances.edit.form", instance.mainForm.slug);
      }
    });
  }
});
