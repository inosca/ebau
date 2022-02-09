import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Helper | is-embedded", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    await render(hbs`{{is-embedded}}`);

    assert.dom(this.element).hasText("false");
  });
});
