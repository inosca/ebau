import { setupTest } from "ember-qunit";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

module("Unit | Service | session", function (hooks) {
  setupTest(hooks);

  test("it computes the headers", async function (assert) {
    assert.expect(1);

    const service = this.owner.lookup("service:session");

    await authenticateSession({
      access_token: "opensesame",
    });

    service.language = "de";
    service.group = 5;

    assert.deepEqual(service.headers, {
      authorization: "Bearer opensesame",
      "accept-language": "de",
      language: "de",
      "x-camac-group": 5,
    });
  });
});
