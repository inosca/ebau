import EmberObject from "@ember/object";
import { render } from "@ember/test-helpers";
import { setupRenderingTest } from "ember-qunit";
import hbs from "htmlbars-inline-precompile";
import { module, test } from "qunit";

module("Integration | Component | camac-input-date", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders a date input", async function (assert) {
    assert.expect(2);

    this.set(
      "model",
      EmberObject.create({
        value: "2018-11-12",
      })
    );

    this.set("config", {
      max: "2019-12-31",
      min: "2018-11-01",
    });

    await render(hbs`{{camac-input-date config=config model=model}}`);

    assert.dom("input[type=text]").exists();
    assert.dom("input[type=text]").hasValue("12.11.2018");
  });

  test("it renders in readonly mode", async function (assert) {
    assert.expect(1);

    await render(hbs`{{camac-input-date readonly=true}}`);

    assert.dom("input[type=text]").isDisabled();
  });
});
