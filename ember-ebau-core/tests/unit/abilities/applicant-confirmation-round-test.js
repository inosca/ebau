import { settled } from "@ember/test-helpers";
import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

import setupPermissions from "dummy/tests/helpers/permissions";

module("Unit | Ability | applicant-confirmation-round", function (hooks) {
  setupTest(hooks);
  setupPermissions(hooks);

  hooks.beforeEach(async function () {
    const store = this.owner.lookup("service:store");

    const instance = this.server.create("instance");
    const user = this.server.create("user");
    this.instanceId = parseInt(instance.id);
    this.owner.lookup("service:ebau-modules").instanceId = this.instanceId;
    this.owner.lookup("service:session").user = user;

    this.running = await store.findRecord(
      "applicant-confirmation-round",
      this.server.create("applicant-confirmation-round", {
        status: "running",
        instance,
      }).id,
    );
    this.completed = await store.findRecord(
      "applicant-confirmation-round",
      this.server.create("applicant-confirmation-round", {
        status: "completed",
        instance,
      }).id,
    );
    this.canceled = await store.findRecord(
      "applicant-confirmation-round",
      this.server.create("applicant-confirmation-round", {
        status: "canceled",
        instance,
      }).id,
    );

    const withPending = this.server.create("applicant-confirmation-round", {
      instance,
      status: "running",
    });
    this.server.create("applicant-confirmation", {
      user,
      round: withPending,
      status: "pending",
    });
    this.withPending = await store.findRecord(
      "applicant-confirmation-round",
      withPending.id,
    );

    const withoutPending = this.server.create("applicant-confirmation-round", {
      instance,
      status: "completed",
    });
    this.server.create("applicant-confirmation", {
      user,
      round: withoutPending,
      status: "confirmed",
    });
    this.withoutPending = await store.findRecord(
      "applicant-confirmation-round",
      withoutPending.id,
    );
  });

  test("it computes start permission", async function (assert) {
    const ability = this.owner.lookup("ability:applicant-confirmation-round");
    const permission = "applicant-confirmation-start";

    this.permissions.grant(this.instanceId, [permission]);

    ability.model = this.running;
    assert.false(await ability.canStart());

    ability.model = this.completed;
    assert.false(await ability.canStart());

    ability.model = this.canceled;
    assert.true(await ability.canStart());

    ability.model = null;
    ability.instanceId = this.instanceId;
    assert.true(await ability.canStart());

    this.permissions.revoke(this.instanceId, [permission]);
    assert.false(await ability.canStart());
  });

  test("it computes confirm permission", async function (assert) {
    const ability = this.owner.lookup("ability:applicant-confirmation-round");
    const permission = "applicant-confirmation-confirm";

    this.permissions.grant(this.instanceId, [permission]);

    ability.model = this.withoutPending;
    this.withoutPending.currentUserConfirmation;
    await settled();
    assert.false(await ability.canConfirm());

    ability.model = this.withPending;
    this.withPending.currentUserConfirmation;
    await settled();
    assert.true(await ability.canConfirm());

    this.permissions.revoke(this.instanceId, [permission]);
    assert.false(await ability.canConfirm());
  });

  test("it computes cancel permission", async function (assert) {
    const ability = this.owner.lookup("ability:applicant-confirmation-round");
    const permission = "applicant-confirmation-cancel";

    this.permissions.grant(this.instanceId, [permission]);

    ability.model = this.completed;
    assert.false(await ability.canCancel());

    ability.model = this.running;
    assert.true(await ability.canCancel());

    this.permissions.revoke(this.instanceId, [permission]);
    assert.false(await ability.canCancel());
  });

  test("it computes invalidate permission", async function (assert) {
    const ability = this.owner.lookup("ability:applicant-confirmation-round");
    const permission = "applicant-confirmation-invalidate";

    this.permissions.grant(this.instanceId, [permission]);

    ability.model = this.canceled;
    assert.false(await ability.canInvalidate());

    ability.model = this.completed;
    assert.true(await ability.canInvalidate());

    this.permissions.revoke(this.instanceId, [permission]);
    assert.false(await ability.canInvalidate());
  });
});
