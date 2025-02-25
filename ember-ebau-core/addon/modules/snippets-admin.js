import SnippetsAdminIndexController from "ember-ebau-core/controllers/snippets-admin/index";
import SnippetsAdminNewController from "ember-ebau-core/controllers/snippets-admin/new";
import { registerModule } from "ember-ebau-core/modules";
import SnippetsAdminRoute from "ember-ebau-core/routes/snippets-admin";
import SnippetsAdminEditRoute from "ember-ebau-core/routes/snippets-admin/edit";
import SnippetsAdminIndexRoute from "ember-ebau-core/routes/snippets-admin/index";
import SnippetsAdminNewRoute from "ember-ebau-core/routes/snippets-admin/new";
import SnippetsAdminTemplate from "ember-ebau-core/templates/snippets-admin";
import SnippetsAdminEditTemplate from "ember-ebau-core/templates/snippets-admin/edit";
import SnippetsAdminIndexTemplate from "ember-ebau-core/templates/snippets-admin/index";
import SnippetsAdminNewTemplate from "ember-ebau-core/templates/snippets-admin/new";

export default function register(router, options = {}) {
  router.route("snippets-admin", options, function () {
    this.route("edit", { path: "/:id" });
    this.route("new");
  });

  registerModule("snippets-admin", router.parent, options.resetNamespace, {
    routes: {
      "snippets-admin": SnippetsAdminRoute,
      "snippets-admin/index": SnippetsAdminIndexRoute,
      "snippets-admin/edit": SnippetsAdminEditRoute,
      "snippets-admin/new": SnippetsAdminNewRoute,
    },
    controllers: {
      "snippets-admin/index": SnippetsAdminIndexController,
      "snippets-admin/new": SnippetsAdminNewController,
    },
    templates: {
      "snippets-admin": SnippetsAdminTemplate,
      "snippets-admin/index": SnippetsAdminIndexTemplate,
      "snippets-admin/edit": SnippetsAdminEditTemplate,
      "snippets-admin/new": SnippetsAdminNewTemplate,
    },
  });
}
