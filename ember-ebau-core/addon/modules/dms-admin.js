import { registerModule } from "ember-ebau-core/modules";
import DMSAdminRoute from "ember-ebau-core/routes/dms-admin";
import DMSAdminEditRoute from "ember-ebau-core/routes/dms-admin/edit";
import DMSAdminIndexRoute from "ember-ebau-core/routes/dms-admin/index";
import DMSAdminNewRoute from "ember-ebau-core/routes/dms-admin/new";
import DMSAdminTemplate from "ember-ebau-core/templates/dms-admin";
import DMSAdminEditTemplate from "ember-ebau-core/templates/dms-admin/edit";
import DMSAdminIndexTemplate from "ember-ebau-core/templates/dms-admin/index";
import DMSAdminNewTemplate from "ember-ebau-core/templates/dms-admin/new";

export default function register(router, options = {}) {
  router.route("dms-admin", options, function () {
    this.route("edit", { path: "/:slug" });
    this.route("new");
  });

  registerModule("dms-admin", router.parent, options.resetNamespace, {
    routes: {
      "dms-admin": DMSAdminRoute,
      "dms-admin/index": DMSAdminIndexRoute,
      "dms-admin/edit": DMSAdminEditRoute,
      "dms-admin/new": DMSAdminNewRoute,
    },
    controllers: {},
    templates: {
      "dms-admin": DMSAdminTemplate,
      "dms-admin/index": DMSAdminIndexTemplate,
      "dms-admin/edit": DMSAdminEditTemplate,
      "dms-admin/new": DMSAdminNewTemplate,
    },
  });
}
