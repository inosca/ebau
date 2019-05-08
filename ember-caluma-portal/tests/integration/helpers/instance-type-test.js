import { module, test } from "qunit";
import { setupRenderingTest } from "ember-qunit";
import { render } from "@ember/test-helpers";
import hbs from "htmlbars-inline-precompile";

module("Integration | Helper | instance-type", function(hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function(assert) {
    this.set("inputValue", { form: { name: "foo" } });

    await render(hbs`{{instance-type inputValue}}`);

    assert.equal(this.element.textContent.trim(), "foo");
  });
});
