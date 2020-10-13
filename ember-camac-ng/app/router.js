import EmberRouter from "@ember/routing/router";

import config from "./config/environment";

export default class Router extends EmberRouter {
  location = config.locationType;
  rootURL = config.rootURL;
}

/* eslint-disable-next-line array-callback-return */
Router.map(function() {
  this.route("organisation");
  this.route("history", { path: "/instances/:id/history" });
  this.route("journal", { path: "/instances/:id/journal" });
  this.route("work-items", function() {
    this.route(
      "instance",
      {
        path: "instances/:instance_id/work-items"
      },
      function() {
        this.route("edit", { path: "/:work_item_id" });
        this.route("new");
      }
    );
  });
  this.route("form", { path: "/instances/:id/form" });

  this.mount("ember-caluma", {
    as: "form-builder",
    path: "/form-builder",
    resetNamespace: true
  });
  this.route("cases");
});
