import { module, test } from "qunit";
import { setupRenderingTest } from "ember-qunit";
import { render, fillIn, focus, blur } from "@ember/test-helpers";
import hbs from "htmlbars-inline-precompile";
import EmberObject from "@ember/object";

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

  test("it validates input", async function(assert) {
    this.set(
      "model",
      EmberObject.create({
        value: 2
      })
    );

    this.set("config", { min: 10, max: 20 });

    await render(
      hbs`{{camac-input-number-separator config=config model=model on-change=(action (mut model.value))}}`
    );

    await fillIn("input[type=text]", "5");
    assert.dom("input[type=text]").hasClass("uk-form-danger");
    assert
      .dom("input[type=text]")
      .hasAttribute("title", "Eingabe ist zu klein");

    await fillIn("input[type=text]", "25");
    assert.dom("input[type=text]").hasClass("uk-form-danger");
    assert
      .dom("input[type=text]")
      .hasAttribute("title", "Eingabe ist zu gross");

    await fillIn("input[type=text]", "abc");
    assert.dom("input[type=text]").hasClass("uk-form-danger");
    assert
      .dom("input[type=text]")
      .hasAttribute("title", "Eingabe ist keine Zahl");

    await fillIn("input[type=text]", "127.0.0.1");
    assert.dom("input[type=text]").hasClass("uk-form-danger");
    assert
      .dom("input[type=text]")
      .hasAttribute("title", "Eingabe ist keine Zahl");
  });
});
