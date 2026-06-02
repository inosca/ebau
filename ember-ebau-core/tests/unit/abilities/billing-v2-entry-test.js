import { module, test } from "qunit";
import { stub } from "sinon";

import { setupTest } from "dummy/tests/helpers";
import setupPermissions from "dummy/tests/helpers/permissions";
import BillingV2EntryAbility from "ember-ebau-core/abilities/billing-v2-entry";
import mainConfig from "ember-ebau-core/config/main";
import { setupFeatures } from "ember-ebau-core/test-support";

module("Unit | Ability | billing-v2-entry", function (hooks) {
  setupTest(hooks);
  setupFeatures(hooks);
  setupPermissions(hooks);

  test("it computes delete permission", async function (assert) {
    const service = this.server.create("service");
    const entry = this.server.create("billing-v2-entry", {
      group: this.server.create("group", { service }),
    });
    const model = await this.owner
      .lookup("service:store")
      .findRecord("billing-v2-entry", entry.id, {
        include: "group,group.service",
      });

    const ability = this.owner.lookup("ability:billing-v2-entry");
    ability.model = model;

    this.owner.lookup("service:ebau-modules").serviceId = service.id + 1;
    assert.notOk(await ability.canDelete());

    this.owner.lookup("service:ebau-modules").serviceId = service.id;
    assert.ok(await ability.canDelete());

    model.dateCharged = "2024-04-17";
    assert.notOk(await ability.canDelete());
  });

  test.each(
    "it computes edit permission",
    [
      ["circulation", true],
      ["sb1", false],
    ],
    async function (assert, [instanceState, expected]) {
      const originalBillingConfig = mainConfig.billing;
      const originalInstanceStateConfig = mainConfig.instanceStates;

      mainConfig.instanceStates = {
        circulation: this.server.create("instance-state").id,
        sb1: this.server.create("instance-state").id,
      };
      mainConfig.billing = { readOnlyInstanceStates: ["sb1"] };

      const instance = this.server.create("instance", {
        instanceStateId: mainConfig.instanceStates[instanceState],
      });
      this.owner.lookup("service:ebau-modules").instanceId = instance.id;
      await this.owner
        .lookup("service:store")
        .findRecord("instance", instance.id);

      const ability = this.owner.lookup("ability:billing-v2-entry");
      assert.strictEqual(await ability.canEdit(), expected);

      mainConfig.billing = originalBillingConfig;
      mainConfig.instanceStates = originalInstanceStateConfig;
    },
  );

  test.each(
    "it computes charge permission",
    [
      [false, false, false, false],
      [true, false, false, false],
      [true, true, false, false],
      [true, true, true, true],
    ],
    async function (
      assert,
      [enableChargeFeature, canEdit, isAutority, expected],
    ) {
      const service = this.server.create("public-service");
      const instance = this.server.create("instance", {
        activeService: service,
      });

      await this.owner
        .lookup("service:store")
        .findRecord("instance", instance.id);

      const ebauModules = this.owner.lookup("service:ebau-modules");

      ebauModules.instanceId = instance.id;
      ebauModules.serviceId = isAutority ? service.id : service.id + 1;

      this.features.set("billing.charge", enableChargeFeature);
      stub(BillingV2EntryAbility.prototype, "canEdit").get(
        () => async () => canEdit,
      );

      const ability = this.owner.lookup("ability:billing-v2-entry");
      assert.strictEqual(await ability.canCharge(), expected);
    },
  );

  test("it computes charge permission with new permission module", async function (assert) {
    this.features.enable("billing.charge");

    const instanceId = parseInt(this.server.create("instance").id);

    this.owner.lookup("service:permissions").fullyEnabled = true;
    this.owner.lookup("service:ebau-modules").instanceId = instanceId;

    await this.owner.lookup("service:store").findRecord("instance", instanceId);

    this.permissions.grant(instanceId, ["billing-charge"]);

    const ability = this.owner.lookup("ability:billing-v2-entry");
    assert.strictEqual(await ability.canCharge(), true);
  });
});
