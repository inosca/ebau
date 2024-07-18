import { module, test } from "qunit";
import { spy, restore } from "sinon";

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

  test("it populate the cache for an instance", async function (assert) {
    const permissions = this.owner.lookup("service:permissions");
    const store = this.owner.lookup("service:store");

    // populate ember store to make sure the next call really triggers an API
    // call in all cases
    await store.findRecord("instance-permission", 1, { reload: true });

    const findSpy = spy(store, "findRecord");
    await permissions.populateCacheFor(1);

    assert.strictEqual(
      findSpy.callCount,
      1,
      "Permissions were fetched from the API",
    );

    const peekSpy = spy(store, "peekRecord");
    assert.true(await permissions.hasAll(1, ["form-read"]));
    assert.strictEqual(
      findSpy.callCount,
      1,
      "Permissions weren't fetched from the API",
    );
    assert.strictEqual(
      peekSpy.callCount,
      1,
      "Permissions were peeked from the store cache",
    );

    restore();
  });
});
