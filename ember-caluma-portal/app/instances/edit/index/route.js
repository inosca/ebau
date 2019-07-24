import Route from "@ember/routing/route";
import { next } from "@ember/runloop";

export default Route.extend({
  redirect() {
    next(async () => {
      const controller = this.controllerFor("instances.edit");
      const mainForm = await controller.mainFormTask.last;

      if (mainForm) {
        this.replaceWith("instances.edit.form", mainForm.slug);
      }
    });
  }
});
