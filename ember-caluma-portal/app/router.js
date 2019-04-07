import EmberRouter from "@ember/routing/router";
import config from "./config/environment";

const Router = EmberRouter.extend({
  location: config.locationType,
  rootURL: config.rootURL
});

const resetNamespace = true;

Router.map(function() {
  this.route("login");
  this.route("logout");
  this.route("protected", { path: "/" }, function() {
    this.route("index", { path: "/", resetNamespace });

    this.mount("ember-caluma", {
      as: "form-builder",
      path: "/form-builder",
      resetNamespace: true
    });
  });
});

export default Router;
