import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";
import { setupFeatures } from "ember-ebau-core/test-support";

module("Integration | Component | billing-global-table/row", function (hooks) {
  setupRenderingTest(hooks);
  setupFeatures(hooks);
  setupMirage(hooks);

  hooks.beforeEach(async function () {
    const service = this.server.create("service");
    const entry = this.server.create("billing-v2-entry", {
      calculation: "flat",
      taxMode: "inclusive",
      taxRate: "8.1",
      totalCost: "1210.13",
      finalRate: "1210.13",
      organization: "municipal",
      billingType: "direct",
      dateAdded: "2024-01-01",
      dateCharged: null,
      group: this.server.create("group", { service }),
    });

    this.entry = await this.owner
      .lookup("service:store")
      .findRecord("billing-v2-entry", entry.id, {
        include: "user,group,group.service",
      });

    this.owner.lookup("service:ebau-modules").serviceId = service.id;
  });

  test("it renders", async function (assert) {
    this.features.enable("billing.legalBasis");
    this.features.disable("billing.displayService");
    await render(hbs`<BillingGlobalTable::Row @entry={{this.entry}} />`);

    assert.dom("tr").exists({ count: 1 });
    assert.dom("td").exists({ count: 7 });

    assert
      .dom("td[data-test-entry-text]")
      .hasText(`${this.entry.text} (${this.entry.legalBasis})`);
    assert
      .dom("td[data-test-entry-group]")
      .hasText(this.entry.get("group.name"));
    assert
      .dom("td[data-test-entry-user]")
      .hasText(this.entry.get("user.fullName"));
    assert
      .dom("td[data-test-entry-amount]")
      .hasText("1’210.13 inkl. 8.1% MWSt");
    assert.dom("td[data-test-entry-final-rate]").hasText("1’210.13");
    assert.dom("td[data-test-entry-added]").hasText("01.01.2024");
  });

  test("it displays service instead of group if configured", async function (assert) {
    this.features.enable("billing.displayService");
    await render(hbs`<BillingGlobalTable::Row @entry={{this.entry}} />`);
    assert.dom("td[data-test-entry-group]").doesNotExist();
    assert
      .dom("td[data-test-entry-service]")
      .hasText(this.entry.get("group.service.name"));
  });
});
