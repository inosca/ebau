import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Helper | get-options", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    this.plainOptions = [1];
    this.resourceOptions = { value: [2] };
    this.dataResourceOptions = { records: [3] };

    this.optionsKey = "options";

    await render(hbs`{{get-options this this.optionsKey}}`);

    // default value
    assert.dom(this.element).hasText("");

    // options from a getter
    this.set("optionsKey", "plainOptions");
    assert.dom(this.element).hasText("1");

    // options from a resource
    this.set("optionsKey", "resourceOptions");
    assert.dom(this.element).hasText("2");

    // options from a data resource
    this.set("optionsKey", "dataResourceOptions");
    assert.dom(this.element).hasText("3");
  });
});
