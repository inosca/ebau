import { render, click } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";
import { stub } from "sinon";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | snippets-table/category", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  test("it renders", async function (assert) {
    this.server.createList("notification-template", 2, {
      purpose: "Category",
    });

    this.snippets = this.owner
      .lookup("service:store")
      .findAll("notification-template");

    await render(
      hbs`<SnippetsTable::Category
  @category="Category"
  @snippets={{this.snippets}}
  @editable={{true}}
/>`,
    );

    assert.dom("table[data-test-snippets-table] tbody tr").exists({ count: 3 });
  });

  test("it can collapse and expand", async function (assert) {
    this.server.createList("notification-template", 2, {
      purpose: "Category",
    });

    this.snippets = this.owner
      .lookup("service:store")
      .findAll("notification-template");

    await render(
      hbs`<SnippetsTable::Category
  @category="Category"
  @snippets={{this.snippets}}
  @editable={{true}}
/>`,
    );

    assert.dom("table[data-test-snippets-table]").exists();
    await click("[data-test-toggle-expanded]");
    assert.dom("table[data-test-snippets-table]").doesNotExist();
    await click("[data-test-toggle-expanded]");
    assert.dom("table[data-test-snippets-table]").exists();
  });

  test("it can copy", async function (assert) {
    const clipboardFake = stub(navigator.clipboard, "writeText");

    this.server.create("notification-template", {
      purpose: "Category",
      body: "Test body",
    });

    this.snippets = await this.owner
      .lookup("service:store")
      .findAll("notification-template");

    await render(
      hbs`<SnippetsTable::Category @category="Category" @snippets={{this.snippets}} />`,
    );

    assert.dom("table[data-test-snippets-table] tbody tr").exists({ count: 1 });

    const snippet = this.snippets[0];
    await click(`[data-test-copy-snippet="${snippet.id}"]`);

    assert.strictEqual(clipboardFake.callCount, 1);
    assert.strictEqual(clipboardFake.args[0][0], "Test body");
  });
});
