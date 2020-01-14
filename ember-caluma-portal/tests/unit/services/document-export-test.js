import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Service | document-export", function(hooks) {
  setupTest(hooks);

  test("it exists", function(assert) {
    const service = this.owner.lookup("service:document-export");
    assert.ok(service);
  });
});
