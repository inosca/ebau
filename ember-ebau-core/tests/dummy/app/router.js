import EmberRouter from "@ember/routing/router";
import { inject as service } from "@ember/service";

import config from "dummy/config/environment";
import registerBilling from "ember-ebau-core/modules/billing";

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
  this.route("communications", function () {
    this.route("edit", { path: "/:id" });
    this.route("new");
  });

  this.route("work-items");

  registerBilling(this);
});
