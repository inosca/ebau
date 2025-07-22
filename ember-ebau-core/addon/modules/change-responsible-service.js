import ChangeResponsibleServiceController from "ember-ebau-core/controllers/change-responsible-service";
import { registerModule } from "ember-ebau-core/modules";
import ChangeResponsibleServiceRoute from "ember-ebau-core/routes/change-responsible-service";
import ChangeResponsibleServiceTemplate from "ember-ebau-core/templates/change-responsible-service";

export default function register(router, options = {}) {
  router.route("change-responsible-service", {
    ...options,
    path: "/change-responsible-service/:type",
  });

  registerModule(
    "change-responsible-service",
    router.parent,
    options.resetNamespace,
    {
      routes: {
        "change-responsible-service": ChangeResponsibleServiceRoute,
      },
      controllers: {
        "change-responsible-service": ChangeResponsibleServiceController,
      },
      templates: {
        "change-responsible-service": ChangeResponsibleServiceTemplate,
      },
    },
  );
}
