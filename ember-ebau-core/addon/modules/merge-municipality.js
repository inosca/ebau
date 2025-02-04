import { registerModule } from "ember-ebau-core/modules";
import MergeMunicipalityRoute from "ember-ebau-core/routes/merge-municipality";
import MergeMunicipalityTemplate from "ember-ebau-core/templates/merge-municipality";

export default function register(router, options = {}) {
  router.route("merge-municipality", options, function () {});

  registerModule("merge-municipality", router.parent, options.resetNamespace, {
    routes: {
      "merge-municipality": MergeMunicipalityRoute,
    },
    templates: {
      "merge-municipality": MergeMunicipalityTemplate,
    },
  });
}
