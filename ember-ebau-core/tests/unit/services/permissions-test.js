import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";
import setupPermissions from "dummy/tests/helpers/permissions";

module("Unit | Service | permissions", function (hooks) {
  setupTest(hooks);
  setupPermissions(hooks, 1, ["form-read"]);

  test("it can check permissions", async function (assert) {
    const service = this.owner.lookup("service:permissions");

    assert.false(await service.hasAny(1, [], true));
    assert.false(await service.hasAny(1, ["form-write"], true));
    assert.true(await service.hasAny(1, ["form-read"], true));
    assert.true(await service.hasAny(1, ["form-read", "form-write"], true));

    assert.false(await service.hasAll(1, [], true));
    assert.false(await service.hasAll(1, ["form-write"], true));
    assert.true(await service.hasAll(1, ["form-read"], true));
    assert.false(await service.hasAll(1, ["form-read", "form-write"], true));
    this.permissions.grant(1, ["form-write"]);
    assert.true(await service.hasAll(1, ["form-read", "form-write"], true));
  });

  test("it can check permissions without an array", async function (assert) {
    const service = this.owner.lookup("service:permissions");

    assert.true(await service.hasAny(1, "form-read", true));
    assert.true(await service.hasAll(1, "form-read", true));
  });
});
