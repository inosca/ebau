import WorkItemsGlobalController from "ember-ebau-core/controllers/work-items-global";
import { registerModule } from "ember-ebau-core/modules";
import WorkItemsGlobalRoute from "ember-ebau-core/routes/work-items-global";
import WorkItemsGlobalTemplate from "ember-ebau-core/templates/work-items-global";

export default function register(router, options = {}) {
  router.route("work-items", options);

  registerModule("work-items-global", router.parent, options.resetNamespace, {
    routes: { "work-items": WorkItemsGlobalRoute },
    controllers: { "work-items": WorkItemsGlobalController },
    templates: { "work-items": WorkItemsGlobalTemplate },
  });
}
