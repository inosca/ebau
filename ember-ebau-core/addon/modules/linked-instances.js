import LinkedInstancesController from "ember-ebau-core/controllers/linked-instances";
import LinkedInstancesIndexController from "ember-ebau-core/controllers/linked-instances/index";
import { registerModule } from "ember-ebau-core/modules";
import LinkedInstancesRoute from "ember-ebau-core/routes/linked-instances";
import LinkedInstancesTemplate from "ember-ebau-core/templates/linked-instances";
import LinkedInstancesIndexTemplate from "ember-ebau-core/templates/linked-instances/index";

export default function register(router, options = {}) {
  router.route("linked-instances", options, function () {});

  registerModule("linked-instances", router.parent, options.resetNamespace, {
    routes: {
      "linked-instances": LinkedInstancesRoute,
    },
    controllers: {
      "linked-instances": LinkedInstancesController,
      "linked-instances/index": LinkedInstancesIndexController,
    },
    templates: {
      "linked-instances": LinkedInstancesTemplate,
      "linked-instances/index": LinkedInstancesIndexTemplate,
    },
  });
}
