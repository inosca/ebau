import { registerModule } from "ember-ebau-core/modules";
import SanctionTemplatesEditRoute from "ember-ebau-core/routes/sanction-templates/edit";
import SanctionTemplatesIndexRoute from "ember-ebau-core/routes/sanction-templates/index";
import SanctionTemplatesNewRoute from "ember-ebau-core/routes/sanction-templates/new";
import SanctionTemplatesEditTemplate from "ember-ebau-core/templates/sanction-templates/edit";
import SanctionTemplatesIndexTemplate from "ember-ebau-core/templates/sanction-templates/index";
import SanctionTemplatesNewTemplate from "ember-ebau-core/templates/sanction-templates/new";

export default function register(router, options = {}) {
  router.route("sanction-templates", options, function () {
    this.route("edit", { path: "/:id/edit" });
    this.route("new");
  });

  registerModule("sanction-templates", router.parent, options.resetNamespace, {
    routes: {
      "sanction-templates": SanctionTemplatesIndexRoute,
      "sanction-templates/new": SanctionTemplatesNewRoute,
      "sanction-templates/edit": SanctionTemplatesEditRoute,
    },
    templates: {
      "sanction-templates/index": SanctionTemplatesIndexTemplate,
      "sanction-templates/new": SanctionTemplatesNewTemplate,
      "sanction-templates/edit": SanctionTemplatesEditTemplate,
    },
  });
}
