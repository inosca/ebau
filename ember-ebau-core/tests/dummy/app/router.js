import EmberRouter from "@ember/routing/router";
import { service } from "@ember/service";

import config from "dummy/config/environment";
import registerBilling from "ember-ebau-core/modules/billing";
import registerDeadlines from "ember-ebau-core/modules/deadlines";
import registerHistory from "ember-ebau-core/modules/history";
import registerPermissions from "ember-ebau-core/modules/permissions";
import registerProfile from "ember-ebau-core/modules/profile";
import registerRejection from "ember-ebau-core/modules/rejection";
import registerResponsible from "ember-ebau-core/modules/responsible";
import registerRulesets from "ember-ebau-core/modules/rulesets";
import registerServicePermissions from "ember-ebau-core/modules/service-permissions";
import registerSnippets from "ember-ebau-core/modules/snippets";
import registerSnippetsAdmin from "ember-ebau-core/modules/snippets-admin";

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
  registerRejection(this);
  registerPermissions(this);
  registerSnippetsAdmin(this);
  registerSnippets(this);
  registerProfile(this);
  registerServicePermissions(this);
  registerRulesets(this);
  registerDeadlines(this);
  registerResponsible(this);
  registerHistory(this);
});
