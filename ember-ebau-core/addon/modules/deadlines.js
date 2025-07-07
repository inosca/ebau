import { registerModule } from "ember-ebau-core/modules";
import DeadlinesRoute from "ember-ebau-core/routes/deadlines";
import DeadlinesIndexRoute from "ember-ebau-core/routes/deadlines/index";
import DeadlinesTemplate from "ember-ebau-core/templates/deadlines";
import DeadlinesIndexTemplate from "ember-ebau-core/templates/deadlines/index";

export default function register(router, options = {}) {
  router.route("deadlines", options, function () {});

  registerModule("deadlines", router.parent, options.resetNamespace, {
    routes: {
      deadlines: DeadlinesRoute,
      "deadlines/index": DeadlinesIndexRoute,
    },
    controllers: {},
    templates: {
      deadlines: DeadlinesTemplate,
      "deadlines/index": DeadlinesIndexTemplate,
    },
  });
}
