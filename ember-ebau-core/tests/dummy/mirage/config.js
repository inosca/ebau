import graphqlHandler from "@projectcaluma/ember-testing/mirage-graphql";
import { discoverEmberDataModels } from "ember-cli-mirage";
import { DateTime } from "luxon";
import { createServer } from "miragejs";

export default function makeServer(config) {
  return createServer({
    ...config,
    models: { ...discoverEmberDataModels(), ...config.models },
    routes() {
      this.namespace = "/api/v1";
      this.timing = 400;

      this.resource("history-entries", { only: ["index"] });
      this.resource("journal-entries");
      this.resource("attachments");
      this.resource("instances", { only: ["index", "show"] });
      this.resource("instance-states", { only: ["index", "show"] });
      this.resource("services");
      this.resource("users");
      this.resource("public-users");
      this.resource("public-services");
      this.resource("public-groups");

      this.resource("communications-topics");
      this.resource("communications-messages");
      this.resource("communications-attachments");
      this.resource("communications-entities");

      this.post("/communications-messages", function (schema, request) {
        const topicId = JSON.parse(request.requestBody.get("topic")).id;

        const attrs = {};
        attrs.topic = schema.communicationsTopics.find(topicId);
        attrs.body = request.requestBody.get("body");
        attrs.createdAt = new Date();

        return schema.communicationsMessages.create(attrs);
      });

      this.patch("/communications-messages/:id/read", (schema, request) => {
        const message = schema.communicationsMessages.find(request.params.id);
        message.update({ readAt: DateTime.now().toISO() });
        return message;
      });

      this.patch("/communications-messages/:id/unread", (schema, request) => {
        const message = schema.communicationsMessages.find(request.params.id);
        message.update({ readAt: undefined });
        return message;
      });

      this.namespace = ""; // reset namespace

      this.post("/graphql", graphqlHandler(this), 200);
    },
  });
}
