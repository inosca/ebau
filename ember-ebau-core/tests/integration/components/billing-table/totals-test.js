import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { t } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";
import setupFeatures from "dummy/tests/helpers/features";

module("Integration | Component | billing-table/totals", function (hooks) {
  setupRenderingTest(hooks);
  setupFeatures(hooks);

  hooks.beforeEach(function () {
    this.totals = {
      cantonal: { uncharged: 1, total: 2 },
      municipal: { uncharged: 3, total: 4 },
      all: { uncharged: 5, total: 6 },
    };
  });

  test("it renders with all features enabled", async function (assert) {
    this.features.enable("billing.charge", "billing.organization");
    await render(hbs`<BillingTable::Totals @totals={{this.totals}} />`);

    assert.dom("tr").exists({ count: 9 });

    assert.dom("tr:nth-of-type(1) hr").exists();
    assert
      .dom("tr:nth-of-type(2)")
      .hasText(`${t("billing.totals.cantonal.uncharged")} 1.00`);
    assert
      .dom("tr:nth-of-type(3)")
      .hasText(`${t("billing.totals.cantonal.total")} 2.00`);
    assert.dom("tr:nth-of-type(4) hr").exists();
    assert
      .dom("tr:nth-of-type(5)")
      .hasText(`${t("billing.totals.municipal.uncharged")} 3.00`);
    assert
      .dom("tr:nth-of-type(6)")
      .hasText(`${t("billing.totals.municipal.total")} 4.00`);
    assert.dom("tr:nth-of-type(7) hr").exists();
    assert
      .dom("tr:nth-of-type(8)")
      .hasText(`${t("billing.totals.all.uncharged")} 5.00`);
    assert
      .dom("tr:nth-of-type(9)")
      .hasText(`${t("billing.totals.all.total")} 6.00`);
  });

  test("it renders all features disabled", async function (assert) {
    this.features.disable("billing.charge", "billing.organization");
    await render(hbs`<BillingTable::Totals @totals={{this.totals}} />`);

    assert.dom("tr").exists({ count: 2 });

    assert.dom("tr:nth-of-type(1) hr").exists();
    assert
      .dom("tr:nth-of-type(2)")
      .hasText(`${t("billing.totals.all.total")} 6.00`);
  });

  test("it renders with organization feature enabled and charge feature disabled", async function (assert) {
    this.features.enable("billing.organization");
    this.features.disable("billing.charge");
    await render(hbs`<BillingTable::Totals @totals={{this.totals}} />`);

    assert.dom("tr").exists({ count: 6 });

    assert.dom("tr:nth-of-type(1) hr").exists();
    assert
      .dom("tr:nth-of-type(2)")
      .hasText(`${t("billing.totals.cantonal.total")} 2.00`);
    assert.dom("tr:nth-of-type(3) hr").exists();
    assert
      .dom("tr:nth-of-type(4)")
      .hasText(`${t("billing.totals.municipal.total")} 4.00`);
    assert.dom("tr:nth-of-type(5) hr").exists();
    assert
      .dom("tr:nth-of-type(6)")
      .hasText(`${t("billing.totals.all.total")} 6.00`);
  });

  test("it renders with organization feature disabled and charge feature enabled", async function (assert) {
    this.features.disable("billing.organization");
    this.features.enable("billing.charge");
    await render(hbs`<BillingTable::Totals @totals={{this.totals}} />`);

    assert.dom("tr").exists({ count: 3 });

    assert.dom("tr:nth-of-type(1) hr").exists();
    assert
      .dom("tr:nth-of-type(2)")
      .hasText(`${t("billing.totals.all.uncharged")} 5.00`);
    assert
      .dom("tr:nth-of-type(3)")
      .hasText(`${t("billing.totals.all.total")} 6.00`);
  });

  test("it removes organization totals if empty", async function (assert) {
    this.totals = {
      cantonal: { uncharged: 0, total: 0 },
      municipal: { uncharged: 1, total: 2 },
      all: { uncharged: 3, total: 4 },
    };

    // all features enabled
    this.features.enable("billing.charge", "billing.organization");
    await render(hbs`<BillingTable::Totals @totals={{this.totals}} />`);

    assert.dom("tr").exists({ count: 6 });

    assert.dom("tr:nth-of-type(1) hr").exists();
    assert
      .dom("tr:nth-of-type(2)")
      .hasText(`${t("billing.totals.municipal.uncharged")} 1.00`);
    assert
      .dom("tr:nth-of-type(3)")
      .hasText(`${t("billing.totals.municipal.total")} 2.00`);
    assert.dom("tr:nth-of-type(4) hr").exists();
    assert
      .dom("tr:nth-of-type(5)")
      .hasText(`${t("billing.totals.all.uncharged")} 3.00`);
    assert
      .dom("tr:nth-of-type(6)")
      .hasText(`${t("billing.totals.all.total")} 4.00`);
  });
});
