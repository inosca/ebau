import { module, test } from "qunit";
import { setupRenderingTest } from "ember-qunit";
import { render, fillIn } from "@ember/test-helpers";
import hbs from "htmlbars-inline-precompile";
import EmberObject from "@ember/object";

module("Integration | Component | camac-input-textarea", function(hooks) {
  setupRenderingTest(hooks);

  test("it renders a textarea", async function(assert) {
    assert.expect(6);

    this.set(
      "model",
      EmberObject.create({
        value: "foo bar"
      })
    );

    this.set("config", {
      cols: 20,
      rows: 5,
      minlength: 0,
      maxlength: 500
    });

    await render(hbs`{{camac-input-textarea config=config model=model}}`);

    assert.dom("textarea").exists();

    assert.dom("textarea").hasAttribute("cols", "20");
    assert.dom("textarea").hasAttribute("rows", "5");
    assert.dom("textarea").hasAttribute("minlength", "0");
    assert.dom("textarea").hasAttribute("maxlength", "500");

    assert.dom("textarea").hasText("foo bar");
  });

  test("it renders in readonly mode", async function(assert) {
    assert.expect(1);

    this.set(
      "model",
      EmberObject.create({
        value: "foo bar"
      })
    );

    this.set("config", {});

    await render(
      hbs`{{camac-input-textarea config=config model=model readonly=true}}`
    );

    assert.dom("textarea").isDisabled();
  });

  test("it can change the value", async function(assert) {
    assert.expect(1);

    this.set(
      "model",
      EmberObject.create({
        value: "foo bar"
      })
    );

    this.set("config", {});

    await render(
      hbs`{{camac-input-textarea config=config model=model on-change=(action (mut model.value))}}`
    );

    await fillIn("textarea", "foo bar to foobar");

    assert.equal(this.get("model.value"), "foo bar to foobar");
  });
});
