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
import { selectChoose } from "ember-power-select/test-support";
import { clickTrigger } from "ember-power-select/test-support/helpers";
import { module, test } from "qunit";

import { setupApplicationTest } from "dummy/tests/helpers";
import { setupFeatures, setupConfig } from "ember-ebau-core/test-support";

module("Acceptance | billing", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);
  setupFeatures(hooks);
  setupConfig(hooks);

  hooks.beforeEach(function () {
    this.features.disableAll();

    const service = this.server.create("service", { slug: "service-slug" });
    const publicService = this.server.create("public-service", {
      id: service.id,
    });

    this.serviceGroup = publicService.serviceGroup;
    this.server.create("public-service-group", {
      id: this.serviceGroup.id,
      slug: this.serviceGroup.slug,
    });
    service.serviceGroup = this.serviceGroup;
    service.save();

    this.instance = this.server.create("instance", {
      activeService: publicService,
      form: this.server.create("form", { name: "test-form-v3" }),
    });
    this.group = this.server.create("group", { service });
    this.service = service;

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

  test("it can release billing entries for clearing", async function (assert) {
    this.features.enable("billing.releaseForClearing");
    this.features.enable("billing.charge");
    this.config.set("billing", {
      releaseForClearing: {
        allowedForServiceGroups: [this.serviceGroup.slug],
        subsequentChargeAllowedForServices: [this.service.slug],
        form: ["test-form"],
      },
    });

    this.server.createList("billing-v2-entry", 2, {
      group: this.group,
      instance: this.instance,
    });

    await visit("/billing");

    await click("input[data-test-toggle-all]");
    await click(
      "table[data-test-billing-table] tbody tr:nth-of-type(1) input[data-test-toggle]",
    );

    await click("button[data-test-release-for-clearing-submit]");

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
      "billing.productNumber",
      "billing.remark",
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
    await fillIn("textarea[name=remark]", "My remark 1");
    await fillIn("input[name=legal-basis]", "Test §§101");
    await fillIn("input[name=cost-center]", "1000121");
    await fillIn("select[name=product-number]", "100000");
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
    await fillIn("select[name=product-number]", "300000");
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
    await fillIn("select[name=product-number]", "100000");
    await fillIn("select[name=calculation]", "hourly");
    await fillIn("input[name=hours]", 1.5);
    await fillIn("input[name=hourly-rate]", 150.5);
    await fillIn("select[name=tax-mode]", "exempt:0");
    await fillIn("select[name=organization]", "");
    await fillIn("select[name=billing-type]", "forwarded");
    await click("button[data-test-submit]");
    assert.dom("table[data-test-billing-table] tbody tr").exists({ count: 3 });
  });

  module("templates", function (hooks) {
    const templateDefaults = {
      billingType: "direct",
      costCenter: "1000123",
      legalBasis: "Test §§100",
      organization: "municipal",
      taxMode: "exempt",
      taxRate: 0,
      finalRate: undefined,
      hours: undefined,
      hourlyRate: undefined,
      percentage: undefined,
      totalCost: undefined,
    };

    hooks.beforeEach(function () {
      this.templates = [
        this.server.create("billing-v2-entry-template", {
          ...templateDefaults,
          name: "Flat example template",
          hint: "A hint for the flat rate example",
          calculation: "flat",
          totalCost: 1000.5,
          remark: "My remark",
        }),
        this.server.create("billing-v2-entry-template", {
          ...templateDefaults,
          name: "Percentage example template",
          hint: "A hint for the percentage rate example",
          calculation: "percentage",
          percentage: 10.5,
          totalCost: 1000.5,
          taxMode: "exclusive",
          taxRate: 8.1,
        }),
        this.server.create("billing-v2-entry-template", {
          ...templateDefaults,
          name: "Hourly example template",
          hint: "A hint for the hourly rate example",
          calculation: "hourly",
          hours: 1.5,
          hourlyRate: 150.5,
          taxMode: "inclusive",
          taxRate: 8.1,
        }),
      ];

      this.features.enable(
        "billing.organization",
        "billing.billingType",
        "billing.legalBasis",
        "billing.costCenter",
        "billing.remark",
      );
    });

    test("it can load and display template choices when present", async function (assert) {
      await visit("/billing");
      assert
        .dom("table[data-test-billing-table] tbody tr td")
        .exists({ count: 1 });
      assert
        .dom("table[data-test-billing-table] tbody tr td")
        .hasText(t("global.empty"));

      await click("a[data-test-add]");
      assert.strictEqual(currentURL(), "/billing/new");

      await clickTrigger();
      assert.dom("ul.ember-power-select-options > li").exists({ count: 3 });
      assert
        .dom("ul.ember-power-select-options > li:nth-child(1)")
        .hasText(this.templates[0].name);
      assert
        .dom("ul.ember-power-select-options > li:nth-child(2)")
        .hasText(this.templates[1].name);
      assert
        .dom("ul.ember-power-select-options > li:nth-child(3)")
        .hasText(this.templates[2].name);

      // empty by default
      assert.dom("input[name=text]").hasValue("");
      assert.dom("select[name=organization]").hasValue("");
      assert.dom("select[name=billing-type]").hasValue("by_authority");
      assert.dom("select[name=calculation]").hasValue("flat");
      assert.dom("select[name=tax-mode]").hasValue("exempt:0");
      assert.dom("input[name=total-cost]").hasValue("");
    });

    test("it can handle a template with a flat rate", async function (assert) {
      await visit("/billing");
      await click("a[data-test-add]");
      assert.strictEqual(currentURL(), "/billing/new");

      await selectChoose("[data-test-templates]", this.templates[0].name);
      assert
        .dom("div[data-test-template-hint]")
        .hasText("A hint for the flat rate example");
      await click("button[data-test-apply-template]");

      assert.dom("input[name=text]").hasValue(this.templates[0].text);
      assert.dom("select[name=organization]").hasValue("municipal");
      assert.dom("select[name=billing-type]").hasValue("direct");
      assert.dom("select[name=calculation]").hasValue("flat");
      assert.dom("select[name=tax-mode]").hasValue("exempt:0");
      assert.dom("textarea[name=remark]").hasValue("My remark");
      await click("button[data-test-submit]");
      assert.strictEqual(currentURL(), "/billing");
      assert
        .dom("table[data-test-billing-table] tbody tr")
        .exists({ count: 1 });
    });

    test("it can handle a template with a percentage rate", async function (assert) {
      await visit("/billing");
      await click("a[data-test-add]");
      assert.strictEqual(currentURL(), "/billing/new");
      await selectChoose("[data-test-templates]", this.templates[1].name);
      assert
        .dom("div[data-test-template-hint]")
        .hasText("A hint for the percentage rate example");
      await click("button[data-test-apply-template]");

      assert.dom("input[name=text]").hasValue(this.templates[1].text);
      assert.dom("select[name=organization]").hasValue("municipal");
      assert.dom("select[name=billing-type]").hasValue("direct");
      assert.dom("select[name=calculation]").hasValue("percentage");
      assert.dom("select[name=tax-mode]").hasValue("exclusive:8.1");
      assert.dom("input[name=percentage]").hasValue("10.5");
      assert.dom("input[name=total-cost]").hasValue("1000.5");
      await click("button[data-test-submit]");
      assert.strictEqual(currentURL(), "/billing");
      assert
        .dom("table[data-test-billing-table] tbody tr")
        .exists({ count: 1 });
    });

    test("it can handle a template with an hourly rate", async function (assert) {
      await visit("/billing");
      await click("a[data-test-add]");
      assert.strictEqual(currentURL(), "/billing/new");
      await selectChoose("[data-test-templates]", this.templates[2].name);
      assert
        .dom("div[data-test-template-hint]")
        .hasText("A hint for the hourly rate example");
      await click("button[data-test-apply-template]");

      assert.dom("input[name=text]").hasValue(this.templates[2].text);
      assert.dom("select[name=organization]").hasValue("municipal");
      assert.dom("select[name=billing-type]").hasValue("direct");
      assert.dom("select[name=calculation]").hasValue("hourly");
      assert.dom("select[name=tax-mode]").hasValue("inclusive:8.1");
      assert.dom("input[name=hours]").hasValue("1.5");
      assert.dom("input[name=hourly-rate]").hasValue("150.5");
      await click("button[data-test-submit]");
      assert.strictEqual(currentURL(), "/billing");
      assert
        .dom("table[data-test-billing-table] tbody tr")
        .exists({ count: 1 });
    });

    test("it can not continue on a partial template without filling the hours field", async function (assert) {
      this.templates.push(
        this.server.create("billing-v2-entry-template", {
          ...templateDefaults,
          name: "Hourly example template v2",
          hint: "A hint for the hourly rate example without hours filled",
          calculation: "hourly",
          hourlyRate: 150.5,
          taxMode: "inclusive",
          taxRate: 8.1,
        }),
      );

      await visit("/billing");
      await click("a[data-test-add]");
      assert.strictEqual(currentURL(), "/billing/new");

      await selectChoose("[data-test-templates]", this.templates[3].name);
      assert
        .dom("div[data-test-template-hint]")
        .hasText("A hint for the hourly rate example without hours filled");
      await click("button[data-test-apply-template]");

      assert.dom("input[name=text]").hasValue(this.templates[3].text);
      assert.dom("select[name=organization]").hasValue("municipal");
      assert.dom("select[name=billing-type]").hasValue("direct");
      assert.dom("select[name=calculation]").hasValue("hourly");
      assert.dom("select[name=tax-mode]").hasValue("inclusive:8.1");
      assert.dom("input[name=hours]").hasValue("");
      assert.dom("input[name=hourly-rate]").hasValue("150.5");
      await click("button[data-test-submit]");

      // does not continue, because hours field is not filled.
      assert.strictEqual(currentURL(), "/billing/new");

      await fillIn("input[name=hours]", 5);
      await click("button[data-test-submit]");
      assert.strictEqual(currentURL(), "/billing");
    });
  });
});
