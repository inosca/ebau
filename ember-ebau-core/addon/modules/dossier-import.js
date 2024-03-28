import DossierImportDetailController from "ember-ebau-core/controllers/dossier-import/detail";
import DossierImportIndexController from "ember-ebau-core/controllers/dossier-import/index";
import DossierImportNewController from "ember-ebau-core/controllers/dossier-import/new";
import { registerModule } from "ember-ebau-core/modules";
import DossierImportRoute from "ember-ebau-core/routes/dossier-import";
import DossierImportDetailRoute from "ember-ebau-core/routes/dossier-import/detail";
import DossierImportIndexRoute from "ember-ebau-core/routes/dossier-import/index";
import DossierImportNewRoute from "ember-ebau-core/routes/dossier-import/new";
import DossierImportTemplate from "ember-ebau-core/templates/dossier-import";
import DossierImportDetailTemplate from "ember-ebau-core/templates/dossier-import/detail";
import DossierImportIndexTemplate from "ember-ebau-core/templates/dossier-import/index";
import DossierImportNewTemplate from "ember-ebau-core/templates/dossier-import/new";

export default function register(router, options = {}) {
  router.route("dossier-import", options, function () {
    this.route("new");
    this.route("detail", { path: "/:import_id" });
  });

  registerModule("dossier-import", router.parent, options.resetNamespace, {
    routes: {
      "dossier-import": DossierImportRoute,
      "dossier-import/index": DossierImportIndexRoute,
      "dossier-import/detail": DossierImportDetailRoute,
      "dossier-import/new": DossierImportNewRoute,
    },
    controllers: {
      "dossier-import/index": DossierImportIndexController,
      "dossier-import/detail": DossierImportDetailController,
      "dossier-import/new": DossierImportNewController,
    },
    templates: {
      "dossier-import": DossierImportTemplate,
      "dossier-import/index": DossierImportIndexTemplate,
      "dossier-import/detail": DossierImportDetailTemplate,
      "dossier-import/new": DossierImportNewTemplate,
    },
  });
}
