import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "caluma-portal/tests/helpers";

module("Integration | Component | be-disabled-input", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    await render(hbs`<BeDisabledInput />`);

    assert.dom("input").hasAttribute("readonly");
    assert.dom("input").hasClass("uk-disabled");
  });
});
