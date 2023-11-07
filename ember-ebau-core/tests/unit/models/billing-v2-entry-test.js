import { setLocale, setupIntl } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";

module("Unit | Model | billing-v2-entry", function (hooks) {
  setupTest(hooks);
  setupIntl(hooks, ["de-ch", "de"]);

  test.each(
    "it computes the amount text",
    [
      [
        "flat",
        "exclusive",
        "7.7",
        { totalCost: "1234.56" },
        "1’234.56 exkl. 7.7% MWSt",
        "1.234,56 sans la TVA de 7,7 %",
      ],
      [
        "flat",
        "inclusive",
        "2.5",
        { totalCost: "12345.67" },
        "12’345.67 inkl. 2.5% MWSt",
        "12.345,67 TVA de 2,5 % incluse",
      ],
      [
        "flat",
        "exempt",
        "0.0",
        { totalCost: "123.45" },
        "123.45 nicht MWSt-pflichtig",
        "123,45 non soumis à la TVA",
      ],
      [
        "percentage",
        "exempt",
        "0.0",
        { percentage: "15.50", totalCost: "1000.00" },
        "15.50% von 1’000.00 nicht MWSt-pflichtig",
        "15,50 % de 1.000,00 non soumis à la TVA",
      ],
      [
        "hourly",
        "exempt",
        "0.0",
        { hours: "2.50", hourlyRate: "175.50" },
        "2.50 Std à 175.50 nicht MWSt-pflichtig",
        "2,50 heures à 175,50 non soumis à la TVA",
      ],
    ],
    async function (assert, [calculation, taxMode, taxRate, args, de, fr]) {
      const store = this.owner.lookup("service:store");
      const model = store.createRecord("billing-v2-entry", {
        calculation,
        taxMode,
        taxRate,
        ...args,
      });

      setLocale(["de-ch", "de"]);
      assert.strictEqual(model.amount, de);
      setLocale(["de-fr", "fr"]);
      // ember-intl adds weird whitespaces
      assert.strictEqual(model.amount.replace(/\s/g, " "), fr);
    },
  );
});
