import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Transform | journal visibility", function (hooks) {
  setupTest(hooks);

  test("it serializes", function (assert) {
    const transform = this.owner.lookup("transform:journal-visibility");
    assert.equal(transform.serialize(true), "authorities");
    assert.equal(transform.serialize(false), "own_organization");
    assert.equal(transform.serialize(undefined), "own_organization");
  });

  test("it deserializes", function (assert) {
    const transform = this.owner.lookup("transform:journal-visibility");
    assert.equal(transform.deserialize("authorities"), true);
    assert.equal(transform.deserialize("own_organization"), false);
    assert.equal(transform.deserialize("all"), false);
  });
});
