import LegalSubmissionEditController from "ember-ebau-core/controllers/legal-submission/edit";
import LegalSubmissionEditAppealController from "ember-ebau-core/controllers/legal-submission/edit-appeal";
import LegalSubmissionIndexController from "ember-ebau-core/controllers/legal-submission/index";
import { registerModule } from "ember-ebau-core/modules";
import LegalSubmissionRoute from "ember-ebau-core/routes/legal-submission";
import LegalSubmissionEditRoute from "ember-ebau-core/routes/legal-submission/edit";
import LegalSubmissionEditAppealRoute from "ember-ebau-core/routes/legal-submission/edit-appeal";
import LegalSubmissionIndexRoute from "ember-ebau-core/routes/legal-submission/index";
import LegalSubmissionTemplate from "ember-ebau-core/templates/legal-submission";
import LegalSubmissionEditTemplate from "ember-ebau-core/templates/legal-submission/edit";
import LegalSubmissionEditAppealTemplate from "ember-ebau-core/templates/legal-submission/edit-appeal";
import LegalSubmissionIndexTemplate from "ember-ebau-core/templates/legal-submission/index";

export default function register(router, options = {}) {
  router.route("legal-submission", options, function () {
    this.route("edit-appeal", { path: "/appeal/:document_uuid" });
    this.route("edit", { path: "/:document_uuid" });
  });

  registerModule("legal-submission", router.parent, options.resetNamespace, {
    routes: {
      "legal-submission": LegalSubmissionRoute,
      "legal-submission/index": LegalSubmissionIndexRoute,
      "legal-submission/edit-appeal": LegalSubmissionEditAppealRoute,
      "legal-submission/edit": LegalSubmissionEditRoute,
    },
    controllers: {
      "legal-submission/index": LegalSubmissionIndexController,
      "legal-submission/edit-appeal": LegalSubmissionEditAppealController,
      "legal-submission/edit": LegalSubmissionEditController,
    },
    templates: {
      "legal-submission": LegalSubmissionTemplate,
      "legal-submission/index": LegalSubmissionIndexTemplate,
      "legal-submission/edit-appeal": LegalSubmissionEditAppealTemplate,
      "legal-submission/edit": LegalSubmissionEditTemplate,
    },
  });
}
