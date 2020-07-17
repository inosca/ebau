import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupRenderingTest } from "ember-qunit";
import { module, skip } from "qunit";

module("Integration | Component | be-gis", function (hooks) {
  setupRenderingTest(hooks);

  skip("it renders", async function (assert) {
    await render(hbs`{{be-gis}}`);
    assert.ok(this.element);
  });
});
