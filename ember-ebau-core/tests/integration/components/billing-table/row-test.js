import { click, settled, waitFor, render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";
import { stub } from "sinon";

import { setupRenderingTest } from "dummy/tests/helpers";
import setupFeatures from "dummy/tests/helpers/features";
import BillingV2EntryAbility from "ember-ebau-core/abilities/billing-v2-entry";

module("Integration | Component | billing-table/row", function (hooks) {
  setupRenderingTest(hooks);
  setupFeatures(hooks);
  setupMirage(hooks);

  hooks.beforeEach(async function () {
    stub(BillingV2EntryAbility.prototype, "canCharge").get(() => true);
    stub(BillingV2EntryAbility.prototype, "canEdit").get(() => true);

    const service = this.server.create("service");
    const entry = this.server.create("billing-v2-entry", {
      calculation: "flat",
      taxMode: "inclusive",
      taxRate: "7.7",
      totalCost: "1210.13",
      finalRate: "1210.13",
      organization: "municipal",
      billingType: "direct",
      dateAdded: "2023-11-01",
      dateCharged: "2023-11-08",
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
    this.features.enable(
      "billing.charge",
      "billing.organization",
      "billing.billingType",
    );
    this.features.disable("billing.displayService");
    await render(hbs`<BillingTable::Row @entry={{this.entry}} />`);

    assert.dom("tr").exists({ count: 1 });
    assert.dom("td").exists({ count: 11 });

    assert
      .dom("td[data-test-entry-charge] input[data-test-toggle][type=checkbox]")
      .exists();
    assert.dom("td[data-test-entry-text]").hasText(this.entry.text);
    assert
      .dom("td[data-test-entry-group]")
      .hasText(this.entry.get("group.name"));
    assert
      .dom("td[data-test-entry-user]")
      .hasText(this.entry.get("user.fullName"));
    assert
      .dom("td[data-test-entry-amount]")
      .hasText("1’210.13 inkl. 7.7% MWSt");
    assert.dom("td[data-test-entry-final-rate]").hasText("1’210.13");
    assert.dom("td[data-test-entry-added]").hasText("01.11.2023");
    assert.dom("td[data-test-entry-charged]").hasText("08.11.2023");
    assert.dom("td[data-test-entry-organization]").hasText("Kommunal");
    assert.dom("td[data-test-entry-billing-type]").hasText("Direkt verrechnet");
    assert.dom("td[data-test-entry-delete] button[data-test-delete]").exists();

    this.features.disable("billing.charge");
    stub(BillingV2EntryAbility.prototype, "canCharge").get(() => false);
    await render(hbs`<BillingTable::Row @entry={{this.entry}} />`);
    assert.dom("td[data-test-entry-charged]").doesNotExist();
    assert.dom("td[data-test-entry-charge]").doesNotExist();

    this.features.disable("billing.organization");
    await render(hbs`<BillingTable::Row @entry={{this.entry}} />`);
    assert.dom("td[data-test-entry-organization]").doesNotExist();

    stub(BillingV2EntryAbility.prototype, "canEdit").get(() => false);
    await render(hbs`<BillingTable::Row @entry={{this.entry}} />`);
    assert.dom("td[data-test-entry-delete]").doesNotExist();
  });

  test("it displays service instead of group if configured", async function (assert) {
    this.features.enable("billing.displayService");
    await render(hbs`<BillingTable::Row @entry={{this.entry}} />`);
    assert.dom("td[data-test-entry-group]").doesNotExist();
    assert
      .dom("td[data-test-entry-service]")
      .hasText(this.entry.get("group.service.name"));
  });

  test("it can delete", async function (assert) {
    this.refresh = () => assert.step("refresh");
    this.server.delete(
      "/api/v1/billing-v2-entries/:id",
      () => {
        assert.step("delete");
        return;
      },
      204,
    );

    await render(
      hbs`<BillingTable::Row @entry={{this.entry}} @onRefresh={{this.refresh}} />`,
    );

    await click("button[data-test-delete]");

    // Confirm dialog
    await waitFor(".uk-modal.uk-open");
    await click(".uk-modal-footer .uk-button-primary");

    assert.verifySteps(["delete", "refresh"]);
  });

  test("it can select for charging", async function (assert) {
    this.toggle = (value) => {
      assert.step("toggle");
      assert.strictEqual(value, this.entry.id);
    };

    await render(
      hbs`<BillingTable::Row @entry={{this.entry}} @onToggle={{this.toggle}} />`,
    );

    assert.dom("input[data-test-toggle]").isDisabled();
    this.entry.dateCharged = null;
    await settled();
    assert.dom("input[data-test-toggle]").isEnabled();

    await click("input[data-test-toggle]");

    assert.verifySteps(["toggle"]);
  });
});
