import EmberObject from "@ember/object";
import { render, fillIn, focus, blur } from "@ember/test-helpers";
import { setupRenderingTest } from "ember-qunit";
import hbs from "htmlbars-inline-precompile";
import { module, test } from "qunit";

module("Integration | Component | camac-input-number-separator", function(
  hooks
) {
  setupRenderingTest(hooks);

  test("it renders", async function(assert) {
    await render(hbs`{{camac-input-number-separator}}`);

    assert.dom("input[type=text]").exists();
  });

  test("it shows thousand separators", async function(assert) {
    this.set(
      "model",
      EmberObject.create({
        value: 2
      })
    );

    await render(
      hbs`{{camac-input-number-separator model=model on-change=(action (mut model.value))}}`
    );

    await focus("input[type=text]");
    await fillIn("input[type=text]", 5);
    await blur("input[type=text]");

    assert.equal(this.get("model.value"), 5);
    assert.dom("input[type=text]").hasValue("5");

    await focus("input[type=text]");
    await fillIn("input[type=text]", "");
    await blur("input[type=text]");

    assert.equal(this.get("model.value"), 0);
    assert.dom("input[type=text]").hasValue("0");

    await focus("input[type=text]");
    await fillIn("input[type=text]", 5000);
    await blur("input[type=text]");

    assert.equal(this.get("model.value"), "5000");
    assert.dom("input[type=text]").hasValue("5’000");

    await focus("input[type=text]");
    await fillIn("input[type=text]", "5000.50");
    await blur("input[type=text]");

    assert.equal(this.get("model.value"), "5000.50");
    assert.dom("input[type=text]").hasValue("5’000.5");

    await focus("input[type=text]");
    assert.dom("input[type=text]").hasValue("5000.5");
  });
});
