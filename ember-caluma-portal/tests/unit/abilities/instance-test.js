import { module, test } from "qunit";
import { setupTest } from "ember-qunit";

module("Unit | Ability | instance", function(hooks) {
  setupTest(hooks);

  test("it computes form read/write permissions", function(assert) {
    const ability = this.owner.lookup("ability:instance");

    ability.set("model", {
      meta: {
        permissions: {
          main: ["read", "write"],
          sb1: ["read"],
          sb2: []
        }
      }
    });

    ability.set("form", { meta: { "is-main-form": true }, slug: "baugesuch" });

    assert.ok(ability.canWriteForm);
    assert.ok(ability.canReadForm);

    ability.set("form", { meta: { "is-main-form": false }, slug: "sb1" });

    assert.notOk(ability.canWriteForm);
    assert.ok(ability.canReadForm);

    ability.set("form", { meta: { "is-main-form": false }, slug: "sb2" });

    assert.notOk(ability.canWriteForm);
    assert.notOk(ability.canReadForm);
  });
});
