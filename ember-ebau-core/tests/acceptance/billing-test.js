import {
  visit,
  settled,
  waitFor,
  click,
  currentURL,
  fillIn,
} from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { t } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupApplicationTest } from "dummy/tests/helpers";
import { setupFeatures } from "ember-ebau-core/test-support";

module("Acceptance | billing", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);
  setupFeatures(hooks);

  hooks.beforeEach(function () {
    this.features.disableAll();

    const service = this.server.create("service");
    const publicService = this.server.create("public-service", {
      id: service.id,
    });

    this.instance = this.server.create("instance", {
      activeService: publicService,
    });
    this.group = this.server.create("group", { service });

    this.owner.lookup("service:ebau-modules").instanceId = this.instance.id;
    this.owner.lookup("service:ebau-modules").serviceId = service.id;
  });

  test("it can list billing entries", async function (assert) {
    this.server.createList("billing-v2-entry", 10);

    await visit("/billing");

    assert.dom("div.uk-alert[data-test-billing-info]").exists();
    assert.dom("table[data-test-billing-table] tbody tr").exists({ count: 10 });
  });

  test("it can charge billing entries", async function (assert) {
    this.features.enable("billing.charge");

    this.server.createList("billing-v2-entry", 2, {
      group: this.group,
      instance: this.instance,
    });

    await visit("/billing");

    await click("input[data-test-toggle-all]");
    await click(
      "table[data-test-billing-table] tbody tr:nth-of-type(1) input[data-test-toggle]",
    );

    await click("button[data-test-charge-submit]");

    // Confirm dialog
    await waitFor(".uk-modal.uk-open");
    await click(".uk-modal-footer .uk-button-primary");

    // eslint-disable-next-line ember/no-settled-after-test-helper
    await settled();

    assert
      .dom(
        "table[data-test-billing-table] tbody tr:nth-of-type(1) td:nth-of-type(8)",
      )
      .hasNoText();
    assert
      .dom(
        "table[data-test-billing-table] tbody tr:nth-of-type(2) td:nth-of-type(8)",
      )
      .hasAnyText();
  });

  test("it can delete billing entries", async function (assert) {
    this.server.createList("billing-v2-entry", 2, {
      group: this.group,
      instance: this.instance,
    });

    await visit("/billing");

    assert.dom("table[data-test-billing-table] tbody tr").exists({ count: 2 });

    await click("button[data-test-delete]");

    // Confirm dialog
    await waitFor(".uk-modal.uk-open");
    await click(".uk-modal-footer .uk-button-primary");

    assert.dom("table[data-test-billing-table] tbody tr").exists({ count: 1 });
  });

  test("it can add billing entries", async function (assert) {
    this.features.enable(
      "billing.organization",
      "billing.billingType",
      "billing.legalBasis",
      "billing.costCenter",
    );

    await visit("/billing");

    assert
      .dom("table[data-test-billing-table] tbody tr td")
      .exists({ count: 1 });
    assert
      .dom("table[data-test-billing-table] tbody tr td")
      .hasText(t("global.empty"));

    await click("a[data-test-add]");
    assert.strictEqual(currentURL(), "/billing/new");
    await fillIn("input[name=text]", "Test 1");
    await fillIn("input[name=legal-basis]", "Test §§101");
    await fillIn("input[name=cost-center]", "1000121");
    await fillIn("select[name=calculation]", "flat");
    await fillIn("input[name=total-cost]", 1000.5);
    await fillIn("select[name=tax-mode]", "inclusive:8.1");
    await fillIn("select[name=organization]", "cantonal");
    await fillIn("select[name=billing-type]", "by_authority");
    await click("button[data-test-submit]");

    assert.strictEqual(currentURL(), "/billing");

    assert.dom("table[data-test-billing-table] tbody tr").exists({ count: 1 });

    // second entry
    await click("a[data-test-add]");
    await fillIn("input[name=text]", "Test 2");
    await fillIn("input[name=legal-basis]", "Test §§102");
    await fillIn("input[name=cost-center]", "1000122");
    await fillIn("select[name=calculation]", "percentage");
    await fillIn("input[name=percentage]", 10.5);
    await fillIn("input[name=total-cost]", 1000.5);
    await fillIn("select[name=tax-mode]", "exclusive:8.1");
    await fillIn("select[name=organization]", "municipal");
    await fillIn("select[name=billing-type]", "direct");
    await click("button[data-test-submit]");
    assert.dom("table[data-test-billing-table] tbody tr").exists({ count: 2 });

    // third entry
    await click("a[data-test-add]");
    await fillIn("input[name=text]", "Test 3");
    await fillIn("input[name=legal-basis]", "Test §§103");
    await fillIn("input[name=cost-center]", "1000123");
    await fillIn("select[name=calculation]", "hourly");
    await fillIn("input[name=hours]", 1.5);
    await fillIn("input[name=hourly-rate]", 150.5);
    await fillIn("select[name=tax-mode]", "exempt:0");
    await fillIn("select[name=organization]", "");
    await fillIn("select[name=billing-type]", "forwarded");
    await click("button[data-test-submit]");
    assert.dom("table[data-test-billing-table] tbody tr").exists({ count: 3 });
  });
});
