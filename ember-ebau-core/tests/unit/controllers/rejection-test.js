import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";
import {
  CLAIMS_EMPTY,
  CLAIMS_NOT_EMPTY,
  DISTRIBUTION_EMPTY,
  DISTRIBUTION_NOT_EMPTY,
} from "dummy/tests/unit/controllers/rejection-data";
import RejectionController from "ember-ebau-core/controllers/rejection";

module("Unit | Controller | rejection", function (hooks) {
  setupTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(function () {
    this.owner.register("controller:rejection", RejectionController);
  });

  test.each(
    "it computes validations",
    [
      [CLAIMS_EMPTY, DISTRIBUTION_EMPTY, false, false],
      [CLAIMS_NOT_EMPTY, DISTRIBUTION_EMPTY, true, false],
      [CLAIMS_EMPTY, DISTRIBUTION_NOT_EMPTY, false, true],
      [CLAIMS_NOT_EMPTY, DISTRIBUTION_NOT_EMPTY, true, true],
    ],
    async function (
      assert,
      [
        claimsResponse,
        distributionResponse,
        hasOpenClaims,
        hasActiveDistribution,
      ],
    ) {
      const controller = this.owner.lookup("controller:rejection");

      this.server.post(
        "/graphql",
        { data: { ...distributionResponse, ...claimsResponse } },
        200,
      );

      // trigger request and wait for response
      controller.validations;
      await controller.validations.fetchData.last;

      assert.deepEqual(controller.validations.value, {
        hasOpenClaims,
        hasActiveDistribution,
      });
    },
  );
});
