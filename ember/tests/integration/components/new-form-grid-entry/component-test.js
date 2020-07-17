import EmberObject from "@ember/object";
import { render } from "@ember/test-helpers";
import { setupRenderingTest } from "ember-qunit";
import hbs from "htmlbars-inline-precompile";
import { module, test } from "qunit";

module("Integration | Component | new-form-grid-entry", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    assert.expect(2);

    this.set(
      "form",
      EmberObject.create({
        id: 1,
        name: "baubewilligung",
        description: "Baubewilligung",
      })
    );

    await render(hbs`<NewFormGridEntry @form={{this.form}}/>`);

    assert.dom("div.uk-width-1-1 button").hasClass("uk-button-default");

    assert.dom("button").hasText("Baubewilligung");
  });

  test("it renders active", async function (assert) {
    assert.expect(2);

    this.set(
      "form",
      EmberObject.create({
        id: 1,
        name: "baubewilligung",
        description: "Baubewilligung",
      })
    );

    await render(
      hbs`<NewFormGridEntry @form={{this.form}} @selectedForm={{this.form}}/>`
    );

    assert.dom("div.uk-width-1-1 button").hasClass("uk-button-secondary");

    assert.dom("button").hasText("Baubewilligung");
  });
});
