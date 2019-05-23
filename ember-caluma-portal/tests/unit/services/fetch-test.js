import { module, test } from "qunit";
import { setupTest } from "ember-qunit";
import setupMirage from "ember-cli-mirage/test-support/setup-mirage";

module("Unit | Service | fetch", function(hooks) {
  setupTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(function() {
    const session = this.owner.lookup("service:session");

    session.set("data.authenticated.access_token", "opensesame");
  });

  test("it computes the headers", function(assert) {
    assert.expect(2);

    const service = this.owner.lookup("service:fetch");

    assert.equal(service.token, "opensesame");
    assert.deepEqual(service.headers, {
      authorization: "Bearer opensesame",
      accept: "application/vnd.api+json",
      "content-type": "application/vnd.api+json"
    });
  });

  test("it can fetch", function(assert) {
    assert.expect(3);

    const service = this.owner.lookup("service:fetch");

    this.server.get("/foo", function(_, { requestHeaders }) {
      assert.deepEqual(requestHeaders, {
        authorization: "changed",
        accept: "application/vnd.api+json",
        "content-type": "application/vnd.api+json",
        "x-some-header": "changed"
      });

      assert.step("fetch");
    });

    service.fetch("/foo", {
      headers: {
        authorization: "changed",
        "x-some-header": "changed",
        "x-some-undefined-header": undefined
      }
    });

    assert.verifySteps(["fetch"]);
  });
});
