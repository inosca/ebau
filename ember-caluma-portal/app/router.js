import EmberRouter from "@ember/routing/router";
import RouterScroll from "ember-router-scroll";
import config from "./config/environment";

const Router = EmberRouter.extend(RouterScroll, {
  location: config.locationType,
  rootURL: config.rootURL
});

const resetNamespace = true;

Router.map(function() {
  this.route("login");
  this.route("logout");
  this.route("protected", { path: "/" }, function() {
    this.route("index", { path: "/", resetNamespace });
    this.route("instances", { resetNamespace }, function() {
      this.route("new");
      this.route("edit", { path: "/:case_id" });
    });

    this.mount("ember-caluma", {
      as: "form-builder",
      path: "/form-builder",
      resetNamespace: true
    });
  });
});

export default Router;
