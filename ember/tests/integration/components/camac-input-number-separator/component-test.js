import { render, fillIn } from "@ember/test-helpers";
import { tracked } from "@glimmer/tracking";
import { setupRenderingTest } from "ember-qunit";
import hbs from "htmlbars-inline-precompile";
import { module, test } from "qunit";

module("Integration | Component | camac-input-number-separator", function (
  hooks
) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    assert.expect(1);

    await render(hbs`
      <CamacInputNumberSeparator
        @on-change={{fn (mut this.value)}}
      />
    `);

    assert.dom("input[type=text]").exists();
  });

  test("it shows thousand separators", async function (assert) {
    assert.expect(10);

    this.model = new (class {
      @tracked value = 5;
    })();

    await render(hbs`
      <CamacInputNumberSeparator
        @model={{this.model}}
        @on-change={{fn (mut this.model.value)}}
      />`);

    await fillIn("input[type=text]", 5);

    assert.equal(this.model.value, 5);
    assert.dom("input[type=text]").hasValue("5");

    await fillIn("input[type=text]", "");

    assert.equal(this.model.value, "");
    assert.dom("input[type=text]").hasValue("");

    await fillIn("input[type=text]", 5000);

    assert.equal(this.model.value, "5000");
    assert.dom("input[type=text]").hasValue("5’000");

    await fillIn("input[type=text]", "5000,50");

    assert.equal(this.model.value, "5000.50");
    assert.dom("input[type=text]").hasValue("5’000.5");

    await fillIn("input[type=text]", "50'000'000,50");

    assert.equal(this.model.value, "50000000.50");
    assert.dom("input[type=text]").hasValue("50’000’000.5");
  });
});
