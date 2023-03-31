import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";

module("Unit | Serializer | template", function (hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function (assert) {
    const store = this.owner.lookup("service:store");
    const serializer = store.serializerFor("template");

    assert.ok(serializer);
  });

  test("it serializes records", function (assert) {
    const store = this.owner.lookup("service:store");
    const record = store.createRecord("template", {});

    const serializedRecord = record.serialize();

    assert.ok(serializedRecord);
  });
});
