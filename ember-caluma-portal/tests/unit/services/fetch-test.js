import { setupMirage } from "ember-cli-mirage/test-support";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

import { setupTest } from "caluma-portal/tests/helpers";

module("Unit | Service | fetch", function (hooks) {
  setupTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(async function (assert) {
    await authenticateSession({ access_token: "opensesame" });

    const session = this.owner.lookup("service:session");

    session.language = "de";
    session.groupId = 5;
    Object.defineProperty(session, "refreshAuthentication", {
      value: {
        async perform() {
          assert.step("refresh");
          return true;
        },
      },
    });
  });

  test("it can fetch", async function (assert) {
    const service = this.owner.lookup("service:fetch");

    this.server.get("/foo", function (_, { requestHeaders }) {
      assert.deepEqual(requestHeaders, {
        authorization: "changed",
        "accept-language": "de",
        language: "de",
        "x-camac-group": "5",
        accept: "application/vnd.api+json",
        "content-type": "application/vnd.api+json",
        "x-some-header": "changed",
      });

      assert.step("fetch");
    });

    await service.fetch("/foo", {
      headers: {
        authorization: "changed",
        "x-some-header": "changed",
        "x-some-undefined-header": undefined,
      },
    });

    assert.verifySteps(["refresh", "fetch"]);
  });
});
