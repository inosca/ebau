import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | gr-gis", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    this.field = {
      answer: {
        value: null,
      },
    };

    await render(hbs`<GrGis @field={{this.field}} />`);

    assert.dom("[data-test-search]").exists();
    assert.dom("[data-test-map]").exists();
  });
});
