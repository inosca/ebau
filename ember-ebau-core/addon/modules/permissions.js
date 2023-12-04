import { registerModule } from "ember-ebau-core/modules";
import PermissionsRoute from "ember-ebau-core/routes/permissions";
import PermissionsIndexRoute from "ember-ebau-core/routes/permissions/index";
import PermissionsTemplate from "ember-ebau-core/templates/permissions";
import PermissionsIndexTemplate from "ember-ebau-core/templates/permissions/index";

export default function register(router, options = {}) {
  router.route("permissions", options, function () {});

  registerModule("permissions", router.parent, options.resetNamespace, {
    routes: {
      permissions: PermissionsRoute,
      "permissions/index": PermissionsIndexRoute,
    },
    controllers: {},
    templates: {
      permissions: PermissionsTemplate,
      "permissions/index": PermissionsIndexTemplate,
    },
  });
}
