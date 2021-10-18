import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Transform | journal visibility", function (hooks) {
  setupTest(hooks);

  test("it serializes", function (assert) {
    const transform = this.owner.lookup("transform:journal-visibility");
    assert.strictEqual(transform.serialize(true), "authorities");
    assert.strictEqual(transform.serialize(false), "own_organization");
    assert.strictEqual(transform.serialize(undefined), "own_organization");
  });

  test("it deserializes", function (assert) {
    const transform = this.owner.lookup("transform:journal-visibility");
    assert.true(transform.deserialize("authorities"));
    assert.false(transform.deserialize("own_organization"));
    assert.false(transform.deserialize("all"));
  });
});
