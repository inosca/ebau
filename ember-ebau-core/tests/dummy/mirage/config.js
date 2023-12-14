import { faker } from "@faker-js/faker";
import graphqlHandler from "@projectcaluma/ember-testing/mirage-graphql";
import { discoverEmberDataModels } from "ember-cli-mirage";
import { DateTime } from "luxon";
import { createServer } from "miragejs";

import mainConfig from "ember-ebau-core/config/main";
import applyTestQueryParamsFilter from "ember-ebau-core/utils/apply-test-query-params-filter";

export default function makeServer(config) {
  return createServer({
    ...config,
    trackRequests: true,
    models: { ...discoverEmberDataModels(config.store), ...config.models },
    routes() {
      this.namespace = "/api/v1";
      this.timing = 400;

      this.resource("access-levels", { only: ["index"] });
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
      this.resource("notification-templates", { only: ["index", "show"] });

      this.resource("billing-v2-entries");
      this.post(
        "billing-v2-entries",
        function ({ billingV2Entries }) {
          return billingV2Entries.create({
            ...this.normalizedRequestAttrs(),
            finalRate: faker.finance.amount(1, 1000),
          });
        },
        201,
      );
      this.get("billing-v2-entries", function ({ billingV2Entries }) {
        const json = this.serialize(billingV2Entries.all());

        json.meta = {
          totals: {
            cantonal: {
              uncharged: faker.finance.amount(1, 1000),
              total: faker.finance.amount(1, 1000),
            },
            municipal: {
              uncharged: faker.finance.amount(1, 1000),
              total: faker.finance.amount(1, 1000),
            },
            all: {
              uncharged: faker.finance.amount(1, 1000),
              total: faker.finance.amount(1, 1000),
            },
          },
        };

        return json;
      });
      this.patch(
        "billing-v2-entries/:id/charge",
        ({ billingV2Entries }, request) => {
          const entry = billingV2Entries.find(request.params.id);
          entry.update({ dateCharged: DateTime.now().toISO() });
          return;
        },
        204,
      );

      this.resource("communications-topics");
      this.resource("communications-messages");
      this.resource("communications-attachments");
      this.resource("communications-entities");

      this.post(
        "/instances/:id/rejection",
        ({ instances }, request) => {
          const instance = instances.find(request.params.id);

          const rejectionId = parseInt(
            mainConfig.instanceStates[mainConfig.rejection.instanceState],
          );
          const previousId = parseInt(
            mainConfig.instanceStates[
              mainConfig.rejection.allowedInstanceStates[0]
            ],
          );

          if (parseInt(instance.instanceStateId) === rejectionId) {
            instance.update({ instanceStateId: previousId });
          } else {
            instance.update({ instanceStateId: rejectionId });
          }

          return null;
        },
        200,
      );

      this.patch("/instances/:id/rejection", () => {}, 204);

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

      this.resource("instance-acls");
      this.get("instance-acls", (schema, { queryParams }) => {
        const filtered = applyTestQueryParamsFilter(
          schema.instanceAcls.all(),
          queryParams,
        );
        return filtered;
      });

      this.namespace = ""; // reset namespace

      this.post("/graphql", graphqlHandler(this), 200);
    },
  });
}
