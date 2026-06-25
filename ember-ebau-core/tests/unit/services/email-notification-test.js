import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";

module("Unit | Service | email-notification", function (hooks) {
  setupTest(hooks);
  setupMirage(hooks);

  test("it can send email notifications", async function (assert) {
    const service = this.owner.lookup("service:email-notification");

    this.server.post(
      "/api/v1/notification-templates/sendmail",
      (_, { requestHeaders, requestBody }) => {
        const jsonApi = "application/vnd.api+json";
        const body = JSON.parse(requestBody);

        assert.deepEqual(requestHeaders, {
          accept: jsonApi,
          "content-type": jsonApi,
        });
        assert.deepEqual(body, {
          data: {
            attributes: {
              "recipient-types": ["applicant", "municipality"],
              "template-slug": "my-custom-template",
            },
            relationships: {
              inquiry: {
                data: {
                  id: "da9d71c3-f270-4341-9d5c-938a9ec50b8f",
                  type: "work-items",
                },
              },
              instance: {
                data: {
                  id: 99,
                  type: "instances",
                },
              },
            },
            type: "notification-template-sendmails",
          },
        });

        assert.step("api-call");
      },
    );

    await service.send(
      99,
      "my-custom-template",
      ["applicant", "municipality"],
      {
        inquiry: {
          data: {
            type: "work-items",
            id: "da9d71c3-f270-4341-9d5c-938a9ec50b8f",
          },
        },
      },
    );

    assert.verifySteps(["api-call"]);
  });
});
