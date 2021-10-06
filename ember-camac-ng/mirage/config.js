import graphqlHandler from "@projectcaluma/ember-testing/mirage-graphql";

import config from "../config/environment";

/* eslint-disable ember/no-get */
export default function () {
  // this.urlPrefix = "";
  // this.namespace = "";
  this.timing = 1000;

  this.get("/api/v1/instances/:id");

  this.get("/api/v1/users/");

  this.get("/api/v1/services");
  this.get("/api/v1/services/:id");
  this.patch("/api/v1/services/:id");

  this.get("/api/v1/history-entries");

  this.get("/api/v1/journal-entries");
  this.post("/api/v1/journal-entries");
  this.get("/api/v1/journal-entries/:id");
  this.patch("/api/v1/journal-entries/:id");

  this.get("/api/v1/responsible-services");
  this.post("/api/v1/responsible-services");
  this.patch("/api/v1/responsible-services/:id");

  this.get("/api/v1/notification-templates");

  this.post(config.apollo.apiURL, graphqlHandler(this), 200);

  this.passthrough("/index/token");
}
