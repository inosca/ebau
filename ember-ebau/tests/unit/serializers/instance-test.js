import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Serializer | instance", function (hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function (assert) {
    const store = this.owner.lookup("service:store");
    const serializer = store.serializerFor("instance");

    assert.ok(serializer);
  });

  test("it serializes records", function (assert) {
    const store = this.owner.lookup("service:store");
    const record = store.createRecord("instance", {});

    const serializedRecord = record.serialize();

    assert.ok(serializedRecord);
  });
});
