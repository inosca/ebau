import { module, test } from "qunit";
import { setupRenderingTest } from "ember-qunit";
import { render } from "@ember/test-helpers";
import hbs from "htmlbars-inline-precompile";

module("Integration | Helper | count-keys", function(hooks) {
  setupRenderingTest(hooks);

  test("it works", async function(assert) {
    this.set("obj", { foo: 1, bar: 2 });

    await render(hbs`{{count-keys obj}}`);

    assert.dom(this.element).hasText("2");
  });

  test("it handles invalid arguments", async function(assert) {
    this.set("obj", null);

    await render(hbs`{{count-keys obj}}`);

    assert.dom(this.element).hasText("0");
  });
});
