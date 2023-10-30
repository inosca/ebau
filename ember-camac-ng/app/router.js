import EmberRouter from "@ember/routing/router";
import { inject as service } from "@ember/service";
import registerAdditionalDemand from "ember-ebau-core/modules/additional-demand";
import registerCommunications from "ember-ebau-core/modules/communications";
import registerCommunicationsGlobal from "ember-ebau-core/modules/communications-global";
import registerDMSAdmin from "ember-ebau-core/modules/dms-admin";
import registerLegalSubmission from "ember-ebau-core/modules/legal-submission";
import registerPublication from "ember-ebau-core/modules/publication";
import registerResponsible from "ember-ebau-core/modules/responsible";
import registerServicePermissions from "ember-ebau-core/modules/service-permissions";
import registerStatistics from "ember-ebau-core/modules/statistics";
import registerTaskForm from "ember-ebau-core/modules/task-form";

import config from "camac-ng/config/environment";

export default class Router extends EmberRouter {
  @service ebauModules;

  location = config.locationType;
  rootURL = config.rootURL;

  setupRouter(...args) {
    const didSetup = super.setupRouter(...args);

    if (didSetup) {
      this.ebauModules.setupModules();
    }

    return didSetup;
  }
}

/* eslint-disable-next-line array-callback-return */
Router.map(function () {
  this.route("history", { path: "/instances/:instance_id/history" });
  this.route("journal", { path: "/instances/:instance_id/journal" });
  this.route("work-items", function () {
    this.route(
      "instance",
      {
        path: "instances/:instance_id/work-items",
      },
      function () {
        this.route("edit", { path: "/:work_item_id" });
        this.route("new");
      },
    );
  });
  this.route("form", { path: "/instances/:id/form" });

  this.mount("@projectcaluma/ember-form-builder", {
    as: "form-builder",
    path: "/form-builder",
    resetNamespace: true,
  });
  this.mount("ember-ebau-gwr", { as: "gwr-global", path: "/gwr" });
  this.mount("ember-ebau-gwr", { as: "gwr", path: "/gwr/:id" });
  this.route("cases", function () {
    this.route("detail", { path: "/:instance_id" }, function () {
      this.route("dashboard");
    });
    this.route("new");
  });
  this.route("audit", { path: "instances/:instance_id/audit" }, function () {
    this.route("edit", { path: "/edit/:document_uuid" });
  });
  this.route("assign-ebau-number", {
    path: "instances/:instance_id/assign-ebau-number",
  });
  this.route("support", { path: "instances/:instance_id/support" });
  this.route("dossier-import", function () {
    this.route("new");
    this.route("detail", { path: "/:import_id" });
  });

  this.mount("@projectcaluma/ember-distribution", {
    as: "distribution",
    path: "/distribution/:case",
  });

  this.route("dms-generate", { path: "instances/:instance_id/dms-generate" });

  registerLegalSubmission(this);
  registerDMSAdmin(this);
  registerTaskForm(this);
  registerServicePermissions(this);
  registerCommunicationsGlobal(this);
  registerCommunications(this);
  registerStatistics(this);
  registerPublication(this);
  registerAdditionalDemand(this);
  registerResponsible(this);
});
