import { module, test } from "qunit";
import { setupRenderingTest } from "ember-qunit";
import { render } from "@ember/test-helpers";
import hbs from "htmlbars-inline-precompile";
import EmberObject from "@ember/object";

module("Integration | Component | new-form-grid-entry", function(hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function(assert) {
    assert.expect(2);

    this.set(
      "form",
      EmberObject.create({
        id: 1,
        name: "baubewilligung",
        description: "Baubewilligung"
      })
    );

    await render(hbs`{{new-form-grid-entry form=form}}`);

    assert.dom("div.uk-width-1-1 button").hasClass("uk-button-default");

    assert.equal(this.element.textContent.trim(), "Baubewilligung");
  });

  test("it renders active", async function(assert) {
    assert.expect(2);

    this.set(
      "form",
      EmberObject.create({
        id: 1,
        name: "baubewilligung",
        description: "Baubewilligung"
      })
    );

    await render(hbs`{{new-form-grid-entry form=form selectedForm=form}}`);

    assert.dom("div.uk-width-1-1 button").hasClass("uk-button-secondary");

    assert.equal(this.element.textContent.trim(), "Baubewilligung");
  });
});
