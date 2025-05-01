import { registerModule } from "ember-ebau-core/modules";
import GwrTasksRoute from "ember-ebau-core/routes/gwr-tasks";
import GwrTasksTemplate from "ember-ebau-core/templates/gwr-tasks";

export default function register(router, options = {}) {
  router.route("gwr-tasks", options);

  registerModule("gwr-tasks", router.parent, options.resetNamespace, {
    routes: { "gwr-tasks": GwrTasksRoute },
    controllers: {},
    templates: { "gwr-tasks": GwrTasksTemplate },
  });
}
