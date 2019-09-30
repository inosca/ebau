import { module, test } from "qunit";
import { setupTest } from "ember-qunit";

module("Unit | Service | document-export", function(hooks) {
  setupTest(hooks);

  test("it exists", function(assert) {
    let service = this.owner.lookup("service:document-export");
    assert.ok(service);
  });
});
