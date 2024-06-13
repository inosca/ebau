import LinkedInstancesController from "ember-ebau-core/controllers/linked-instances";
import { registerModule } from "ember-ebau-core/modules";
import LinkedInstancesRoute from "ember-ebau-core/routes/linked-instances";
import LinkedInstancesTemplate from "ember-ebau-core/templates/linked-instances";

export default function register(router, options = {}) {
  router.route("linked-instances", options, function () {});

  registerModule("linked-instances", router.parent, options.resetNamespace, {
    routes: {
      "linked-instances": LinkedInstancesRoute,
    },
    controllers: {
      "linked-instances": LinkedInstancesController,
    },
    templates: {
      "linked-instances": LinkedInstancesTemplate,
    },
  });
}
