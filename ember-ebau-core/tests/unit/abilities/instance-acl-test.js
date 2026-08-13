import { setupMirage } from "ember-cli-mirage/test-support";
import { setupTest } from "ember-qunit";
import { DateTime } from "luxon";
import { module, test } from "qunit";
import { replace, replaceGetter, stub } from "sinon";

import { setupConfig, setupPermissions } from "ember-ebau-core/test-support";

module("Unit | Ability | instance-acl", function (hooks) {
  setupTest(hooks);
  setupMirage(hooks);
  setupConfig(hooks);
  setupPermissions(hooks);

  hooks.beforeEach(async function () {
    const accessLevel = this.server.create("access-level", { id: "foo" });
    const activeService = this.server.create("service");
    const instance = this.server.create("instance", { activeService });
    const acl = this.server.create("instance-acl", "active", {
      accessLevel,
      instance,
    });

    this.ability = this.owner.lookup("ability:instance-acl");

    const store = this.owner.lookup("service:store");

    this.model = await store.findRecord("instance-acl", acl.id);
    this.instance = await store.findRecord("instance", instance.id);
    this.service = await store.findRecord("service", activeService.id);
  });

  test("computes grant permissions", async function (assert) {
    await assert.rejects(
      this.ability.canGrant(),
      /`instanceId` must be passed/,
      "throws without an instance ID",
    );

    this.ability.instanceId = this.instance.id;
    this.ability.accessLevels = ["foo"];

    assert.false(await this.ability.canGrant());

    this.permissions.grant(this.instance.id, ["permissions-grant-any"]);
    assert.true(await this.ability.canGrant());

    this.permissions.revoke(this.instance.id, ["permissions-grant-any"]);
    assert.false(await this.ability.canGrant());

    this.permissions.grant(this.instance.id, ["permissions-grant-foo"]);
    assert.true(await this.ability.canGrant());
  });

  test("computes revoke permissions", async function (assert) {
    await assert.rejects(
      this.ability.canRevoke(),
      /`instance-acl` model must be passed/,
      "throws without a model",
    );

    this.ability.model = this.model;

    assert.false(await this.ability.canRevoke());

    this.permissions.grant(this.instance.id, ["permissions-revoke-any"]);
    assert.true(await this.ability.canRevoke());

    this.permissions.revoke(this.instance.id, ["permissions-revoke-any"]);
    assert.false(await this.ability.canRevoke());

    this.permissions.grant(this.instance.id, ["permissions-revoke-foo"]);
    assert.true(await this.ability.canRevoke());

    this.model.endTime = DateTime.now().minus({ days: 1 }).toISO();
    assert.false(await this.ability.canRevoke());
  });

  module("SZ", function () {
    test("computes grant permissions", async function (assert) {
      assert.false(await this.ability.canGrantSZ());

      this.ability.instanceId = this.instance.id;
      assert.false(await this.ability.canGrantSZ());

      this.owner.lookup("service:ebau-modules").serviceId = this.service.id;
      assert.true(await this.ability.canGrantSZ());
    });

    test("computes revoke permissions", async function (assert) {
      const revokeable = stub().returns(false);
      const canGrant = stub().returns(true);

      replaceGetter(this.model, "revokeable", revokeable);
      replace(this.ability, "canGrantSZ", canGrant);

      assert.false(await this.ability.canRevokeSZ());
      assert.true(revokeable.notCalled);
      assert.true(canGrant.notCalled);

      this.ability.model = this.model;

      assert.false(await this.ability.canRevokeSZ());
      assert.true(revokeable.calledOnce);
      assert.true(canGrant.notCalled);

      revokeable.returns(true);
      assert.true(await this.ability.canRevokeSZ());
      assert.true(canGrant.calledOnce);

      canGrant.returns(false);
      assert.false(await this.ability.canRevokeSZ());
    });
  });

  module("UR", function () {
    test("computes grant permissions", async function (assert) {
      assert.false(await this.ability.canGrantUR());

      this.ability.instanceId = this.instance.id;
      assert.false(await this.ability.canGrantUR());

      this.owner.lookup("service:ebau-modules").serviceId = this.service.id;
      assert.true(await this.ability.canGrantUR());

      this.owner.lookup("service:ebau-modules").serviceId = 999;
      assert.false(await this.ability.canGrantUR());

      this.owner.lookup("service:ebau-modules").isTrustedServiceRole = true;
      assert.true(await this.ability.canGrantUR());

      this.owner.lookup("service:ebau-modules").isTrustedServiceRole = false;
      this.owner.lookup("service:ebau-modules").isCoordinationRole = true;
      assert.true(await this.ability.canGrantUR());
    });

    test("computes revoke permissions", async function (assert) {
      const revokeable = stub().returns(false);
      const canGrant = stub().returns(true);

      replaceGetter(this.model, "revokeable", revokeable);
      replace(this.ability, "canGrantUR", canGrant);

      assert.false(await this.ability.canRevokeUR());
      assert.true(revokeable.notCalled);
      assert.true(canGrant.notCalled);

      this.ability.model = this.model;

      assert.false(await this.ability.canRevokeUR());
      assert.true(revokeable.calledOnce);
      assert.true(canGrant.notCalled);

      revokeable.returns(true);
      assert.true(await this.ability.canRevokeUR());
      assert.true(canGrant.calledOnce);

      canGrant.returns(false);
      assert.false(await this.ability.canRevokeUR());
    });
  });
});
