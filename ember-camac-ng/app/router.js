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
  this.route("work-item-list-all", { path: "/work-items" });
  this.route("work-item-list-instance", {
    path: "/instances/:id/work-items"
  });
});
