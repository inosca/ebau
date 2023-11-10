import { registerModule } from "ember-ebau-core/modules";
import PermissionsRoute from "ember-ebau-core/routes/permissions";
// import PermissionsDetailRoute from "ember-ebau-core/routes/permissions/detail";
import PermissionsIndexRoute from "ember-ebau-core/routes/permissions/index";
// import PermissionsNewRoute from "ember-ebau-core/routes/permissions/new";
import PermissionsTemplate from "ember-ebau-core/templates/permissions";
// import PermissionsDetailTemplate from "ember-ebau-core/templates/permissions/detail";
import PermissionsIndexTemplate from "ember-ebau-core/templates/permissions/index";
// import PermissionsNewTemplate from "ember-ebau-core/templates/permissions/new";

export default function register(router, options = {}) {
  router.route("permissions", options, function () {
    // this.route("detail", { path: "/:topic_id" });
    // this.route("new");
  });

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
