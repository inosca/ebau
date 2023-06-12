import EmberRouter from "@ember/routing/router";
import { inject as service } from "@ember/service";
import registerCommunications from "ember-ebau-core/modules/communications";
import registerCommunicationsGlobal from "ember-ebau-core/modules/communications-global";

import config from "caluma-portal/config/environment";

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

const resetNamespace = true;

/* eslint-disable-next-line array-callback-return */
Router.map(function () {
  this.route("login");

  this.route("protected", { path: "/" }, function () {
    // this is needed to resolve ambiguity between the global index and protected index routes
    this.route("index", { path: "/", resetNamespace });
    this.route("instances", { resetNamespace }, function () {
      this.route("new");
      this.route("edit", { path: "/:instance" }, function () {
        this.route("form", { path: "/:form" });
        this.route("feedback");
        this.route("applicants");
        registerCommunications(this);
      });
    });

    this.route("form-builder", { resetNamespace }, function () {
      this.mount("@projectcaluma/ember-form-builder", {
        path: "/",
        resetNamespace: true,
      });
    });

    this.route("support", { resetNamespace });
    this.route("faq", { resetNamespace });
    registerCommunicationsGlobal(this, { resetNamespace });
  });

  this.route("notfound", { path: "/*path" });
  this.route("public-instances", { resetNamespace }, function () {
    this.route("detail", { path: "/:instance_id" }, function () {
      this.route("form");
      this.route("documents");
    });
  });
});
