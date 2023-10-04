import ResponsibleController from "ember-ebau-core/controllers/responsible";
import { registerModule } from "ember-ebau-core/modules";
import ResponsibleRoute from "ember-ebau-core/routes/responsible";
import ResponsibleTemplate from "ember-ebau-core/templates/responsible";

export default function register(router, options = {}) {
  router.route("responsible", options);

  registerModule("responsible", router.parent, options.resetNamespace, {
    routes: { responsible: ResponsibleRoute },
    controllers: { responsible: ResponsibleController },
    templates: { responsible: ResponsibleTemplate },
  });
}
