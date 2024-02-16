import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";
import BillingNewController from "ember-ebau-core/controllers/billing/new";
import { setupFeatures } from "ember-ebau-core/test-support";

module("Unit | Controller | billing/new", function (hooks) {
  setupTest(hooks);
  setupFeatures(hooks);

  hooks.beforeEach(function () {
    this.owner.register("controller:billing/new", BillingNewController);
  });

  test.each(
    "it computes the tax rates",
    [
      [false, [8.1]],
      [true, [8.1, 2.6]],
    ],
    function (assert, [enableReducedTaxRate, expected]) {
      this.features.set("billing.reducedTaxRate", enableReducedTaxRate);

      const controller = this.owner.lookup("controller:billing/new");

      assert.deepEqual(controller.taxRates, expected);
    },
  );

  test.each(
    "it computes the tax mode options",
    [
      [[], ["exempt:0", "inclusive:8.1", "exclusive:8.1"]],
      [
        ["billing.reducedTaxRate"],
        [
          "exempt:0",
          "inclusive:8.1",
          "inclusive:2.6",
          "exclusive:8.1",
          "exclusive:2.6",
        ],
      ],
      [
        ["billing.orderTaxByRate"],
        ["inclusive:8.1", "exclusive:8.1", "exempt:0"],
      ],
      [
        ["billing.reducedTaxRate", "billing.orderTaxByRate"],
        [
          "inclusive:8.1",
          "exclusive:8.1",
          "inclusive:2.6",
          "exclusive:2.6",
          "exempt:0",
        ],
      ],
    ],
    function (assert, [enabledFeatures, expected]) {
      this.features.disableAll();
      this.features.enable(...enabledFeatures);

      const controller = this.owner.lookup("controller:billing/new");

      assert.deepEqual(
        controller.taxModeOptions.map(({ value }) => value),
        expected,
      );
    },
  );
});
