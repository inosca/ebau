import graphqlHandler from "ember-caluma/mirage-graphql";

import config from "../config/environment";

export default function () {
  this.urlPrefix = "";
  this.namespace = "";
  this.timing = 400;

  this.get("/api/v1/me", function ({ users }) {
    return users.first();
  });

  this.get("/api/v1/public-groups");

  this.get("/api/v1/attachments");

  this.get("/api/v1/instances");
  this.get("/api/v1/instances/:id");

  this.get("/api/v1/applicants");
  this.del("/api/v1/applicants/:id");

  this.post("/api/v1/applicants", function ({ applicants, users }) {
    const { email, ...attrs } = this.normalizedRequestAttrs();

    return applicants.create({
      ...attrs,
      userId: parseInt(users.create().id),
      inviteeId: parseInt(users.create({ email }).id),
    });
  });

  this.post(config.apollo.apiURL, graphqlHandler(this), 200);
}
