import { click, render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | case-table/header", function (hooks) {
  setupRenderingTest(hooks);
  setupIntl(hooks);

  test("it renders", async function (assert) {
    this.column = { name: "test" };
    this.order = "foo";

    await render(hbs`
      <CaseTable::Header
        @column={{this.column}}
        @currentOrder={{this.order}}
        @onSetOrder={{fn (mut this.order)}}
      />
    `);

    assert.dom("th").hasText("t:cases.tableHeaders.test:()");
    assert.dom("th > a").doesNotExist();

    this.set("column.order", "test");

    assert.dom("th").hasText("t:cases.tableHeaders.test:()");
    assert.dom("th > a").exists();
    assert.dom("th > a").doesNotHaveClass("uk-text-bold");
    assert.dom("th > a > span").hasAttribute("icon", "arrow-down");

    await click("a");

    assert.strictEqual(this.order, "test");
    assert.dom("th > a").hasClass("uk-text-bold");
    assert.dom("th > a > span").hasAttribute("icon", "arrow-down");

    await click("a");

    assert.strictEqual(this.order, "-test");
    assert.dom("th > a").hasClass("uk-text-bold");
    assert.dom("th > a > span").hasAttribute("icon", "arrow-up");
  });
});
