import StatisticsExportController from "ember-ebau-core/controllers/statistics-export";
import { registerModule } from "ember-ebau-core/modules";
import StatisticsExportRoute from "ember-ebau-core/routes/statistics-export";
import StatisticsExportTemplate from "ember-ebau-core/templates/statistics-export";

export default function register(router, options = {}) {
  router.route("statistics-export", options);

  registerModule("statistics-export", router.parent, options.resetNamespace, {
    routes: { "statistics-export": StatisticsExportRoute },
    controllers: { "statistics-export": StatisticsExportController },
    templates: { "statistics-export": StatisticsExportTemplate },
  });
}
