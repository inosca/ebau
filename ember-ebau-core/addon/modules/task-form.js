import TaskFormController from "ember-ebau-core/controllers/task-form";
import { registerModule } from "ember-ebau-core/modules";
import TaskFormRoute from "ember-ebau-core/routes/task-form";
import TaskFormTemplate from "ember-ebau-core/templates/task-form";

export default function register(router, options = {}) {
  router.route("task-form", { ...options, path: "/task-form/:task" });

  registerModule("task-form", router.parent, options.resetNamespace, {
    routes: { "task-form": TaskFormRoute },
    controllers: { "task-form": TaskFormController },
    templates: { "task-form": TaskFormTemplate },
  });
}
