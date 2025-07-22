import CorrectionsController from "ember-ebau-core/controllers/corrections";
import { registerModule } from "ember-ebau-core/modules";
import CorrectionsRoute from "ember-ebau-core/routes/corrections";
import CorrectionsTemplate from "ember-ebau-core/templates/corrections";

export default function register(router, options = {}) {
  router.route("corrections", options);

  registerModule("corrections", router.parent, options.resetNamespace, {
    routes: {
      corrections: CorrectionsRoute,
    },
    controllers: {
      corrections: CorrectionsController,
    },
    templates: {
      corrections: CorrectionsTemplate,
    },
  });
}
