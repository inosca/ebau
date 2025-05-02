import { visit, currentURL, click, waitFor } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { selectChoose } from "ember-power-select/test-support";
import { module, test } from "qunit";

import { setupApplicationTest } from "dummy/tests/helpers";

module("Acceptance | rulesets/responsible user", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(function () {
    this.server.create("user", { name: "John", surname: "Doe" });
    this.server.create("public-service", { name: "Gemeinde A" });
    this.server.create("public-service", { name: "Gemeinde B" });
    this.server.create("public-service", { name: "Gemeinde C" });
    this.server.create("application-type", { name: "Baugesuch" });
    this.server.create("application-type", { name: "Baugesuch mit UVP" });
  });

  test("add responsible user rule", async function (assert) {
    await visit("/rulesets/responsible-user");

    await click("[data-test-add-rule]");
    assert.strictEqual(currentURL(), "/rulesets/responsible-user/new");

    await click("[data-test-rule-type=municipalities]");
    await selectChoose("#municipalities", "Gemeinde A");
    await selectChoose("#municipalities", "Gemeinde B");
    await selectChoose("#responsibleUser", "John Doe");

    await click("[data-test-save]");

    assert.strictEqual(currentURL(), "/rulesets/responsible-user");

    assert.dom("ul.uk-list > li").exists({ count: 1 });
    assert
      .dom("ul.uk-list > li:nth-of-type(1) > div > div:nth-of-type(1)")
      .hasText("Gemeinde A, Gemeinde B");
    assert
      .dom("ul.uk-list > li:nth-of-type(1) > div > div:nth-of-type(3)")
      .hasText("John Doe");

    await click("[data-test-add-rule]");
    assert.strictEqual(currentURL(), "/rulesets/responsible-user/new");

    await click("[data-test-rule-type=application-types]");
    await selectChoose("#applicationTypes", "Baugesuch mit UVP");
    await selectChoose("#responsibleUser", "John Doe");

    await click("[data-test-save]");

    assert.strictEqual(currentURL(), "/rulesets/responsible-user");

    assert.dom("ul.uk-list > li").exists({ count: 2 });
    assert
      .dom("ul.uk-list > li:nth-of-type(2) > div > div:nth-of-type(1)")
      .hasText("Baugesuch mit UVP");
    assert
      .dom("ul.uk-list > li:nth-of-type(2) > div > div:nth-of-type(3)")
      .hasText("John Doe");
  });

  test("edit responsible user rule", async function (assert) {
    const rule = this.server.create(
      "responsible-user-rule",
      "withMunicipalities",
    );

    await visit("/rulesets/responsible-user");

    await click(`li[data-rule-id="${rule.id}"] [data-test-edit-rule]`);
    assert.strictEqual(currentURL(), `/rulesets/responsible-user/${rule.id}`);

    await selectChoose("#municipalities", "Gemeinde C");
    await selectChoose("#responsibleUser", "John Doe");

    await click("[data-test-save]");

    assert.strictEqual(currentURL(), "/rulesets/responsible-user");

    assert
      .dom(`li[data-rule-id="${rule.id}"] > div > div:nth-of-type(1)`)
      .containsText("Gemeinde C");
    assert
      .dom(`li[data-rule-id="${rule.id}"] > div > div:nth-of-type(3)`)
      .hasText("John Doe");
  });

  test("edit responsible user rule", async function (assert) {
    const rules = this.server.createList(
      "responsible-user-rule",
      2,
      "withMunicipalities",
    );

    await visit("/rulesets/responsible-user");
    await click(`li[data-rule-id="${rules[0].id}"] [data-test-delete-rule]`);

    // Confirm dialog
    await waitFor(".uk-modal.uk-open");
    await click(".uk-modal-footer .uk-button-primary");

    assert.dom(`li[data-rule-id="${rules[0].id}"]`).doesNotExist();
    assert.dom(`li[data-rule-id="${rules[1].id}"]`).exists();
  });
});
