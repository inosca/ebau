import EmberRouter from "@ember/routing/router";
import { inject as service } from "@ember/service";
import registerDMSAdmin from "ember-ebau-core/modules/dms-admin";
import registerLegalSubmission from "ember-ebau-core/modules/legal-submission";
import registerServicePermissions from "ember-ebau-core/modules/service-permissions";
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
      }
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
    this.route("detail", { path: "/:case_id" }, function () {
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
  this.route("responsible", { path: "instances/:instance_id/responsible" });
  this.route(
    "publication",
    { path: "instances/:instance_id/publication/:type" },
    function () {
      this.route("edit", { path: "/:work_item_id" });
    }
  );
  this.route("statistics", function () {
    this.route("avg-cycle-time");
    this.route("cycle-time");
    this.route("process-time");
    this.route("processing-time");
  });

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
});
