import { render, click, fillIn } from "@ember/test-helpers";
import { setupRenderingTest } from "ember-qunit";
import hbs from "htmlbars-inline-precompile";
import { module, test } from "qunit";

module("Integration | Component | camac-gwr-building-table", function (hooks) {
  setupRenderingTest(hooks);

  hooks.beforeEach(function () {
    this.set("value", [{ f1: "test" }]);
    this.set("config", {
      columns: [
        { name: "f1", label: "f1", type: "text", required: true, config: {} },
      ],
    });
  });

  test("it renders", async function (assert) {
    assert.expect(2);

    await render(
      hbs`<CamacGwrBuildingTable @value={{this.value}} @config={{this.config}} @onChange={{fn (mut this.value)}}/>`
    );

    assert.dom("table").exists();
    assert.dom("tbody > tr > td:first-child").hasText("test");
  });

  test("it can delete a row", async function (assert) {
    assert.expect(2);

    await render(
      hbs`<CamacGwrBuildingTable @value={{this.value}} @config={{this.config}} @onChange={{fn (mut this.value)}}/>`
    );

    assert.dom("tbody > tr > td:first-child").hasText("test");

    await click("button[data-test-delete-row]");

    assert
      .dom("tbody > tr > td:first-child")
      .hasText("Noch keine Einträge erfasst");
  });

  test("it can edit a row", async function (assert) {
    assert.expect(2);

    await render(
      hbs`<CamacGwrBuildingTable @value={{this.value}} @config={{this.config}} @onChange={{fn (mut this.value)}}/>`
    );

    assert.dom("tbody > tr > td:first-child").hasText("test");

    await click("button[data-test-edit-row]");
    await fillIn("input", "shimmyshimmyya");
    await click(".uk-button-primary");

    assert.dom("tbody > tr > td:first-child").hasText("shimmyshimmyya");
  });

  test("it can add a row", async function (assert) {
    assert.expect(2);

    await render(
      hbs`<CamacGwrBuildingTable @value={{this.value}} @config={{this.config}} @onChange={{fn (mut this.value)}}/>`
    );

    assert.dom("tbody > tr").exists({ count: 1 });

    await click("tfoot > tr > td:first-child > button");
    await fillIn("input", "test");
    await click(".uk-button-primary");

    assert.dom("tbody > tr").exists({ count: 2 });
  });
});
