import { module, test } from "qunit";
import { setupRenderingTest } from "ember-qunit";
import { render } from "@ember/test-helpers";
import hbs from "htmlbars-inline-precompile";
import EmberObject from "@ember/object";

module("Integration | Component | camac-input-date", function(hooks) {
  setupRenderingTest(hooks);

  test("it renders a date input", async function(assert) {
    assert.expect(4);

    this.set(
      "model",
      EmberObject.create({
        value: "2018-11-12"
      })
    );

    this.set("config", {
      max: "2019-12-31",
      min: "2018-11-01"
    });

    await render(hbs`{{camac-input-date config=config model=model}}`);

    assert.dom("input[type=date]").exists();
    assert.dom("input[type=date]").hasAttribute("max", "2019-12-31");
    assert.dom("input[type=date]").hasAttribute("min", "2018-11-01");
    assert.dom("input[type=date]").hasValue("2018-11-12");
  });

  test("it renders in readonly mode", async function(assert) {
    assert.expect(1);

    await render(hbs`{{camac-input-date readonly=true}}`);

    assert.dom("input[type=date]").isDisabled();
  });
});
