import { setLocale } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";

module("Unit | Model | billing-v2-entry", function (hooks) {
  setupTest(hooks);

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
      [
        "ag_processing_fee",
        "exempt",
        "0.0",
        { totalCost: "1500000.50" },
        "1’500’000.50 CHF Baukosten, davon<br> 0-133'334.95 CHF = 400.00 CHF<br> 133'335 - 2Mio. = 3‰<br> 2-5Mio. = 2.5‰<br> >5Mio = 1.5‰",
        "",
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

      const cleanText = (text) =>
        String(text) // String casting is necessary because we use `htmlSave`
          .replace(/\s/g, " ") // ember-intl adds weird whitespaces in french
          .replace(/\n/g, ""); // remove newlines of multiline translations for comparison

      setLocale(["de-ch", "de"]);
      assert.strictEqual(cleanText(model.amount), de);
      setLocale(["de-fr", "fr"]);
      assert.strictEqual(cleanText(model.amount), fr);
    },
  );
});
