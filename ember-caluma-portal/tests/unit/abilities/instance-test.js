import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

import config from "../../../config/environment";

module("Unit | Ability | instance", function(hooks) {
  setupTest(hooks);

  test("it computes form read/write permissions", function(assert) {
    assert.expect(6);

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

  test("it computes read permissions", function(assert) {
    assert.expect(2);

    const ability = this.owner.lookup("ability:instance");

    ability.set("model", {
      meta: {
        permissions: {
          main: [],
          sb1: [],
          sb2: []
        }
      }
    });

    assert.notOk(ability.canRead);

    ability.set("model", {
      meta: {
        permissions: {
          main: ["read"],
          sb1: [],
          sb2: []
        }
      }
    });

    assert.ok(ability.canRead);
  });

  test("it computes write permissions", function(assert) {
    assert.expect(2);

    const ability = this.owner.lookup("ability:instance");

    ability.set("model", {
      meta: {
        permissions: {
          main: [],
          sb1: [],
          sb2: []
        }
      }
    });

    assert.notOk(ability.canWrite);

    ability.set("model", {
      meta: {
        permissions: {
          main: ["write"],
          sb1: [],
          sb2: []
        }
      }
    });

    assert.ok(ability.canWrite);
  });

  test("it computes create permissions", function(assert) {
    assert.expect(6);

    const ability = this.owner.lookup("ability:instance");

    ability.set("_allGroups", [
      {
        id: 1,
        service: {
          serviceGroup: {
            id: config.ebau.paperInstances.allowedGroups.serviceGroups[0]
          }
        },
        role: { id: config.ebau.paperInstances.allowedGroups.roles[0] }
      }
    ]);

    ability.set("session", {
      isInternal: true,
      group: 1
    });

    assert.notOk(ability.canCreateExternal);
    assert.ok(ability.canCreatePaper);
    assert.ok(ability.canCreate);

    ability.set("session", {
      isInternal: false
    });

    assert.ok(ability.canCreateExternal);
    assert.notOk(ability.canCreatePaper);
    assert.ok(ability.canCreate);
  });
});
