import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Helper | format-coordinate", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    this.centerCoordinate = {
      x: 2759647.420698834,
      y: 1191526.7969428787,
    };

    await render(hbs`{{format-coordinate this.centerCoordinate}}`);

    assert.dom(this.element).hasText("2'759'647 / 1'191'527");
  });
});
