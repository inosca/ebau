import BabStatisticsExportController from "ember-ebau-core/controllers/bab-statistics-export";
import { registerModule } from "ember-ebau-core/modules";
import BabStatisticsExportRoute from "ember-ebau-core/routes/bab-statistics-export";
import BabStatisticsExportTemplate from "ember-ebau-core/templates/bab-statistics-export";

export default function register(router, options = {}) {
  router.route("bab-statistics-export", options);

  registerModule(
    "bab-statistics-export",
    router.parent,
    options.resetNamespace,
    {
      routes: { "bab-statistics-export": BabStatisticsExportRoute },
      controllers: { "bab-statistics-export": BabStatisticsExportController },
      templates: { "bab-statistics-export": BabStatisticsExportTemplate },
    },
  );
}
