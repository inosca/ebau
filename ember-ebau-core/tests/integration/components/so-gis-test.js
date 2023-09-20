import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | so-gis", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    this.field = {
      document: {
        findAnswer() {
          return null;
        },
      },
    };

    await render(hbs`<SoGis @field={{this.field}} />`);

    assert.dom("[data-test-search]").exists();
    assert.dom("[data-test-map]").exists();
  });
});
