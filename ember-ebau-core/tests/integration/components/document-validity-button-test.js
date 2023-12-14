import { click, render, settled } from "@ember/test-helpers";
import { tracked } from "@glimmer/tracking";
import { hbs } from "ember-cli-htmlbars";
import { task } from "ember-concurrency";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

class MockField {
  constructor(slug, valid, hidden) {
    this.question = { raw: { slug, label: slug } };

    this._valid = valid;
    this.hidden = hidden;
  }

  @tracked isInvalid = false;
  @tracked hidden = false;

  get isValid() {
    return !this.isInvalid;
  }

  @task
  *validate() {
    yield Promise.resolve();

    this.isInvalid = !this._valid;
  }
}

module("Integration | Component | document-validity-button", function (hooks) {
  setupRenderingTest(hooks);

  hooks.beforeEach(function () {
    const fields = [
      ["test-1", false, false],
      ["test-2", false, true],
      ["test-3", true, false],
    ].map((config) => new MockField(...config));

    this.field = { ...fields[0], document: { fields } };
  });

  test("it renders", async function (assert) {
    await render(hbs`<DocumentValidityButton @field={{this.field}} />`);

    assert.dom("button.uk-button.uk-button-primary").exists();
    assert
      .dom("button.uk-button.uk-button-primary")
      .hasAttribute("type", "button");

    await click("button");

    assert.dom(".uk-alert.uk-alert-danger").exists();
    assert.dom("ul > li").exists({ count: 1 });
    assert.dom("ul > li").hasText("test-1");

    this.field.document.fields[0].isInvalid = false;
    await settled();

    assert.dom(".uk-alert.uk-alert-danger").doesNotExist();
    assert.dom(".uk-alert.uk-alert-success").exists();
  });

  test("it can be disabled", async function (assert) {
    await render(
      hbs`<DocumentValidityButton @disabled={{true}} @field={{this.field}} />`,
    );

    assert.dom("button").isDisabled();
  });
});
