import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Service | session", function(hooks) {
  setupTest(hooks);

  test("it computes the headers", function(assert) {
    assert.expect(1);

    const service = this.owner.lookup("service:session");

    service.setProperties({
      isAuthenticated: true,
      data: {
        authenticated: {
          access_token: "opensesame"
        },
        language: "de",
        group: 5
      }
    });

    assert.deepEqual(service.headers, {
      authorization: "Bearer opensesame",
      "accept-language": "de",
      language: "de",
      "x-camac-group": 5
    });
  });
});
