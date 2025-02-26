import { registerModule } from "ember-ebau-core/modules";
import SanctionsControlRoute from "ember-ebau-core/routes/sanctions/control";
import SanctionsEditRoute from "ember-ebau-core/routes/sanctions/edit";
import SanctionsIndexRoute from "ember-ebau-core/routes/sanctions/index";
import SanctionsNewRoute from "ember-ebau-core/routes/sanctions/new";
import SanctionsShowRoute from "ember-ebau-core/routes/sanctions/show";
import SanctionsTemplatesRoute from "ember-ebau-core/routes/sanctions/templates";
import SanctionsControlTemplate from "ember-ebau-core/templates/sanctions/control";
import SanctionsEditTemplate from "ember-ebau-core/templates/sanctions/edit";
import SanctionsIndexTemplate from "ember-ebau-core/templates/sanctions/index";
import SanctionsNewTemplate from "ember-ebau-core/templates/sanctions/new";
import SanctionsShowTemplate from "ember-ebau-core/templates/sanctions/show";
import SanctionsTemplatesTemplate from "ember-ebau-core/templates/sanctions/templates";

export default function register(router, options = {}) {
  router.route("sanctions", options, function () {
    this.route("show", { path: "/:id" });
    this.route("edit", { path: "/:id/edit" });
    this.route("control", { path: "/:id/control" });
    this.route("new");
    this.route("templates");
  });

  registerModule("sanctions", router.parent, options.resetNamespace, {
    routes: {
      sanctions: SanctionsIndexRoute,
      "sanctions/show": SanctionsShowRoute,
      "sanctions/new": SanctionsNewRoute,
      "sanctions/edit": SanctionsEditRoute,
      "sanctions/control": SanctionsControlRoute,
      "sanctions/templates": SanctionsTemplatesRoute,
    },
    templates: {
      "sanctions/index": SanctionsIndexTemplate,
      "sanctions/show": SanctionsShowTemplate,
      "sanctions/new": SanctionsNewTemplate,
      "sanctions/edit": SanctionsEditTemplate,
      "sanctions/control": SanctionsControlTemplate,
      "sanctions/templates": SanctionsTemplatesTemplate,
    },
  });
}
