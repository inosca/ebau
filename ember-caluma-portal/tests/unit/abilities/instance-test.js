import { get } from "@ember/object";
import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

import config from "../../../config/environment";

import testIf from "caluma-portal/tests/helpers/test-if";

module("Unit | Ability | instance", function (hooks) {
  setupTest(hooks);

  test("it computes form read/write permissions", async function (assert) {
    assert.expect(6);

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

    assert.ok(ability.canWriteForm);
    assert.ok(ability.canReadForm);

    ability.set("form", { meta: { "is-main-form": false }, slug: "sb1" });

    assert.notOk(ability.canWriteForm);
    assert.ok(ability.canReadForm);

    ability.set("form", { meta: { "is-main-form": false }, slug: "sb2" });

    assert.notOk(ability.canWriteForm);
    assert.notOk(ability.canReadForm);
  });

  test("it computes read permissions", async function (assert) {
    assert.expect(2);

    const ability = this.owner.lookup("ability:instance");

    ability.set("model", {
      meta: {
        permissions: {
          main: [],
          sb1: [],
          sb2: [],
        },
      },
    });

    assert.notOk(ability.canRead);

    ability.set("model", {
      meta: {
        permissions: {
          main: ["read"],
          sb1: [],
          sb2: [],
        },
      },
    });

    assert.ok(ability.canRead);
  });

  test("it computes write permissions", async function (assert) {
    assert.expect(2);

    const ability = this.owner.lookup("ability:instance");

    ability.set("model", {
      meta: {
        permissions: {
          main: [],
          sb1: [],
          sb2: [],
        },
      },
    });

    assert.notOk(ability.canWrite);

    ability.set("model", {
      meta: {
        permissions: {
          main: ["write"],
          sb1: [],
          sb2: [],
        },
      },
    });

    assert.ok(ability.canWrite);
  });

  test("it computes create permissions", async function (assert) {
    assert.expect(6);

    const ability = this.owner.lookup("ability:instance");

    ability.set("session", {
      isInternal: true,
      group: 1,
      groups: [
        {
          id: 1,
          service: {
            serviceGroup: {
              id: config.ebau.paperInstances.allowedGroups.serviceGroups[0],
            },
          },
          role: { id: config.ebau.paperInstances.allowedGroups.roles[0] },
          canCreatePaper: true,
        },
      ],
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

    assert.ok(ability.canDelete);

    ability.set("model", {
      get(path) {
        return get(this, path);
      },
      instanceState: {
        id: 10000,
      },
    });

    assert.notOk(ability.canDelete);
  });
});
