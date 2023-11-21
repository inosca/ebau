import { click, render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { query } from "ember-data-resources";
import { setupIntl } from "ember-intl/test-support";
import { module, test } from "qunit";
import { stub } from "sinon";

import { setupRenderingTest } from "dummy/tests/helpers";
import setupFeatures from "dummy/tests/helpers/features";
import BillingV2EntryAbility from "ember-ebau-core/abilities/billing-v2-entry";

module("Integration | Component | billing-table", function (hooks) {
  setupRenderingTest(hooks);
  setupFeatures(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  hooks.beforeEach(function () {
    stub(BillingV2EntryAbility.prototype, "canCharge").get(() => true);
    stub(BillingV2EntryAbility.prototype, "canEdit").get(() => true);

    this.server.createList("billing-v2-entry", 2);
    this.server.createList("billing-v2-entry", 3, "charged");

    this.entries = query(this, "billing-v2-entry", () => ({
      include: "group,user",
    }));

    this.noop = () => {};
  });

  test("it renders", async function (assert) {
    this.features.enable("billing.charge", "billing.organization");
    this.features.disable("billing.displayService");

    await render(hbs`<BillingTable
      @entries={{this.entries}}
      @onToggleAll={{this.noop}}
      @onToggleRow={{this.noop}}
      @onRefresh={{this.noop}}
    />`);

    assert.dom("thead tr th").exists({ count: 10 });
    assert
      .dom(
        "thead tr th[data-test-charge] input[data-test-toggle-all][type=checkbox]",
      )
      .exists();
    assert.dom("thead tr th[data-test-text]").hasText("t:billing.position:()");
    assert.dom("thead tr th[data-test-user]").hasText("t:billing.user:()");
    assert.dom("thead tr th[data-test-group]").hasText("t:billing.group:()");
    assert.dom("thead tr th[data-test-amount]").hasText("t:billing.amount:()");
    assert
      .dom("thead tr th[data-test-final-rate]")
      .hasText("t:billing.total:()");
    assert
      .dom("thead tr th[data-test-added]")
      .hasText("t:billing.created-at:()");
    assert
      .dom("thead tr th[data-test-charged]")
      .hasText("t:billing.charged-at:()");
    assert
      .dom("thead tr th[data-test-organization]")
      .hasText("t:billing.organization:()");
    assert.dom("thead tr th[data-test-delete]").exists();

    assert.dom("tbody tr").exists({ count: 5 });
    assert.dom("tfoot tr").exists({ count: 9 });
  });

  test("it displays service instead of group if configured", async function (assert) {
    this.features.enable("billing.displayService");

    await render(hbs`<BillingTable
      @entries={{this.entries}}
      @onToggleAll={{this.noop}}
      @onToggleRow={{this.noop}}
      @onRefresh={{this.noop}}
    />`);

    assert.dom("th[data-test-group]").doesNotExist();
    assert.dom("th[data-test-service]").hasText("t:billing.service:()");
  });

  test("it can hide charged entries", async function (assert) {
    this.features.enable("billing.charge");

    await render(hbs`<BillingTable
      @entries={{this.entries}}
      @onToggleAll={{this.noop}}
      @onToggleRow={{this.noop}}
      @onRefresh={{this.noop}}
    />`);

    assert.dom("tbody tr").exists({ count: 5 });

    await click("input[data-test-toggle-charged]");

    assert.dom("tbody tr").exists({ count: 2 });
  });

  test("it can select entries for charging", async function (assert) {
    this.features.enable("billing.charge");

    this.toggleAll = () => assert.step("toggle-all");
    this.toggleRow = () => assert.step("toggle-row");

    await render(hbs`<BillingTable
      @entries={{this.entries}}
      @onToggleAll={{this.toggleAll}}
      @onToggleRow={{this.toggleRow}}
      @onRefresh={{this.noop}}
    />`);

    await click("input[data-test-toggle-all]");
    await click("input[data-test-toggle]:not([disabled])");

    assert.verifySteps(["toggle-all", "toggle-row"]);
  });
});
