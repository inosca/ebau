import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";
import { setupConfig } from "ember-ebau-core/test-support";

module("Unit | Ability | instance", function (hooks) {
  setupTest(hooks);
  setupMirage(hooks);
  setupConfig(hooks);

  module("rejection", function (hooks) {
    hooks.beforeEach(function () {
      this.instanceStates = {
        rejected: this.server.create("instance-state").id,
        circulation: this.server.create("instance-state").id,
        subm: this.server.create("instance-state").id,
      };

      this.config.set("instanceStates", this.instanceStates);
      this.config.set("rejection", {
        instanceState: "rejected",
        allowedInstanceStates: ["circulation"],
      });

      this.authorityId = this.server.create("public-service").id;
    });

    test.each(
      "it computes rejection permission",
      [
        [true, "circulation", false, false, true],
        [false, "circulation", false, false, false],
        [true, "subm", false, false, false],
        [true, "circulation", true, false, false],
        [true, "circulation", false, true, false],
      ],
      async function (
        assert,
        [
          isAuthority,
          instanceState,
          hasOpenClaims,
          hasActiveDistribution,
          expected,
        ],
      ) {
        const instanceId = this.server.create("instance", {
          instanceStateId: this.instanceStates[instanceState],
          activeServiceId: this.authorityId,
        }).id;

        this.owner.lookup("service:ebau-modules").serviceId = isAuthority
          ? this.authorityId
          : this.authorityId + 1;

        const instance = await this.owner
          .lookup("service:store")
          .findRecord("instance", instanceId);

        const ability = this.owner.lookup("ability:instance");

        ability.model = instance;
        ability.hasOpenClaims = hasOpenClaims;
        ability.hasActiveDistribution = hasActiveDistribution;

        assert.strictEqual(ability.canReject, expected);
      },
    );

    test.each(
      "it computes revert rejection permission",
      [
        [true, "rejected", true],
        [false, "rejected", false],
        [true, "subm", false],
      ],
      async function (assert, [isAuthority, instanceState, expected]) {
        const instanceId = this.server.create("instance", {
          instanceStateId: this.instanceStates[instanceState],
          activeServiceId: this.authorityId,
        }).id;

        this.owner.lookup("service:ebau-modules").serviceId = isAuthority
          ? this.authorityId
          : this.authorityId + 1;

        const instance = await this.owner
          .lookup("service:store")
          .findRecord("instance", instanceId);

        const ability = this.owner.lookup("ability:instance");

        ability.model = instance;

        assert.strictEqual(ability.canRevertRejection, expected);
      },
    );
  });
});
