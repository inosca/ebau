import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";
import {
  CLAIMS_EMPTY,
  CLAIMS_NOT_EMPTY,
  LEGACY_CLAIMS_EMPTY,
  LEGACY_CLAIMS_NOT_EMPTY,
  DISTRIBUTION_EMPTY,
  DISTRIBUTION_NOT_EMPTY,
} from "dummy/tests/unit/controllers/rejection-data";
import RejectionController from "ember-ebau-core/controllers/rejection";
import { setupFeatures } from "ember-ebau-core/test-support";

module("Unit | Controller | rejection", function (hooks) {
  setupTest(hooks);
  setupMirage(hooks);
  setupFeatures(hooks);

  hooks.beforeEach(function () {
    this.owner.register("controller:rejection", RejectionController);
  });

  test.each(
    "it computes validations",
    [
      [
        ["rejection.useLegacyClaims"],
        [LEGACY_CLAIMS_EMPTY, DISTRIBUTION_EMPTY],
        { hasOpenClaims: false },
      ],
      [
        ["rejection.useLegacyClaims"],
        [LEGACY_CLAIMS_NOT_EMPTY, DISTRIBUTION_EMPTY],
        { hasOpenClaims: true },
      ],
      [[], [CLAIMS_EMPTY, DISTRIBUTION_EMPTY], { hasOpenClaims: false }],
      [[], [CLAIMS_NOT_EMPTY, DISTRIBUTION_EMPTY], { hasOpenClaims: true }],
      [
        [],
        [DISTRIBUTION_EMPTY, CLAIMS_EMPTY],
        { hasActiveDistribution: false },
      ],
      [
        [],
        [DISTRIBUTION_NOT_EMPTY, CLAIMS_EMPTY],
        { hasActiveDistribution: true },
      ],
    ],
    async function (assert, [enabledFeatures, responses, expected]) {
      this.features.disableAll();
      this.features.enable(...enabledFeatures);

      const controller = this.owner.lookup("controller:rejection");

      this.server.post(
        "/graphql",
        { data: responses.reduce((full, part) => ({ ...full, ...part }), {}) },
        200,
      );

      // trigger request and wait for response
      controller.validations;
      await controller.validations.fetchData.last;

      Object.entries(expected).forEach(([key, value]) => {
        assert.strictEqual(controller.validations.value[key], value);
      });
    },
  );
});
