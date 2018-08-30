import { module, test } from "qunit";
import { setupRenderingTest } from "ember-qunit";
import { render, click } from "@ember/test-helpers";
import hbs from "htmlbars-inline-precompile";
import EmberObject from "@ember/object";

module("Integration | Component | camac-input-radio", function(hooks) {
  setupRenderingTest(hooks);

  test("it renders radio inputs", async function(assert) {
    assert.expect(2);

    this.set(
      "model",
      EmberObject.create({
        value: "option 1"
      })
    );

    this.set("config", {
      options: ["option 1", "option 2", "option 3"]
    });

    await render(hbs`{{camac-input-radio config=config model=model}}`);

    assert.dom("input[type=radio]").exists({ count: 3 });
    assert.dom("input[type=radio]:checked").exists({ count: 1 });
  });

  test("it can be rendered in readonly mode", async function(assert) {
    assert.expect(2);

    this.set(
      "model",
      EmberObject.create({
        value: "option 1"
      })
    );

    this.set("config", {
      options: ["option 1", "option 2", "option 3"]
    });

    await render(
      hbs`{{camac-input-radio config=config model=model readonly=true}}`
    );

    assert.dom("input[type=radio]").exists({ count: 3 });
    assert.dom("input[type=radio]").isDisabled();
  });

  test("it can change the value", async function(assert) {
    assert.expect(1);

    this.set(
      "model",
      EmberObject.create({
        value: "option 1"
      })
    );

    this.set("config", {
      options: ["option 1", "option 2", "option 3"]
    });

    await render(
      hbs`{{camac-input-radio config=config model=model on-change=(action (mut model.value))}}`
    );

    await click('input[type=radio][value="option 3"]');

    assert.equal(this.get("model.value"), "option 3");
  });
});
