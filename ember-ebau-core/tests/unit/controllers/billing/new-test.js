import { DateTime, Settings } from "luxon";
import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";
import setupFeatures from "dummy/tests/helpers/features";
import BillingNewController from "ember-ebau-core/controllers/billing/new";

module("Unit | Controller | billing/new", function (hooks) {
  setupTest(hooks);
  setupFeatures(hooks);

  hooks.beforeEach(function () {
    this.owner.register("controller:billing/new", BillingNewController);

    this._originalNow = Settings.now;

    this.freezeTime = (isoDate) => {
      const expectedNow = DateTime.fromISO(isoDate);
      Settings.now = () => expectedNow;
    };
  });

  hooks.afterEach(function () {
    Settings.now = this._originalNow;
  });

  test.each(
    "it computes the tax rates",
    [
      ["2023-11-30", false, [7.7]],
      ["2023-12-01", false, [8.1, 7.7]],
      ["2024-02-01", false, [8.1]],
      ["2023-11-30", true, [7.7, 2.5]],
      ["2023-12-01", true, [8.1, 7.7, 2.6, 2.5]],
      ["2024-02-01", true, [8.1, 2.6]],
    ],
    function (assert, [now, enableReducedTaxRate, expected]) {
      this.features.set("billing.reducedTaxRate", enableReducedTaxRate);
      this.freezeTime(now);

      const controller = this.owner.lookup("controller:billing/new");

      assert.deepEqual(controller.taxRates, expected);
    },
  );

  test.each(
    "it computes the tax mode options",
    [
      [[], ["exempt:0", "inclusive:7.7", "exclusive:7.7"]],
      [
        ["billing.reducedTaxRate"],
        [
          "exempt:0",
          "inclusive:7.7",
          "inclusive:2.5",
          "exclusive:7.7",
          "exclusive:2.5",
        ],
      ],
      [
        ["billing.orderTaxByRate"],
        ["inclusive:7.7", "exclusive:7.7", "exempt:0"],
      ],
      [
        ["billing.reducedTaxRate", "billing.orderTaxByRate"],
        [
          "inclusive:7.7",
          "exclusive:7.7",
          "inclusive:2.5",
          "exclusive:2.5",
          "exempt:0",
        ],
      ],
    ],
    function (assert, [enabledFeatures, expected]) {
      this.freezeTime("2023-11-10");

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
