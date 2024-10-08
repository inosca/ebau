import { get } from "@ember/object";
import mainConfig from "ember-ebau-core/config/main";
import { module, test } from "qunit";

import { setupTest } from "caluma-portal/tests/helpers";
import testIf from "caluma-portal/tests/helpers/test-if";

module("Unit | Ability | instance", function (hooks) {
  setupTest(hooks);

  test("it computes form read/write permissions", async function (assert) {
    const ability = this.owner.lookup("ability:instance");

    ability.set("model", {
      meta: {
        permissions: {
          main: ["read", "write"],
          sb1: ["read"],
          sb2: [],
        },
      },
    });

    ability.set("form", { meta: { "is-main-form": true }, slug: "baugesuch" });

    assert.ok(await ability.canWriteForm());
    assert.ok(await ability.canReadForm());

    ability.set("form", { meta: { "is-main-form": false }, slug: "sb1" });

    assert.notOk(await ability.canWriteForm());
    assert.ok(await ability.canReadForm());

    ability.set("form", { meta: { "is-main-form": false }, slug: "sb2" });

    assert.notOk(await ability.canWriteForm());
    assert.notOk(await ability.canReadForm());
  });

  test("it computes create permissions", async function (assert) {
    const ability = this.owner.lookup("ability:instance");

    ability.set("session", {
      isInternal: true,
      group: {
        id: 1,
        service: {
          serviceGroup: {
            id: mainConfig.paperInstances.allowedGroups.serviceGroups[0],
          },
        },
        role: { id: mainConfig.paperInstances.allowedGroups.roles[0] },
        canCreatePaper: true,
      },
    });

    assert.notOk(ability.canCreateExternal);
    assert.ok(ability.canCreatePaper);
    assert.ok(ability.canCreate);

    ability.set("session", {
      isInternal: false,
    });

    assert.ok(ability.canCreateExternal);
    assert.notOk(ability.canCreatePaper);
    assert.ok(ability.canCreate);
  });

  testIf("be")("it computes delete permissions", async function (assert) {
    assert.expect(2);

    const ability = this.owner.lookup("ability:instance");

    ability.set("model", {
      get(path) {
        return get(this, path);
      },
      instanceState: {
        id: 1,
      },
    });

    assert.ok(await ability.canDelete());

    ability.set("model", {
      get(path) {
        return get(this, path);
      },
      instanceState: {
        id: 10000,
      },
    });

    assert.notOk(await ability.canDelete());
  });
});
