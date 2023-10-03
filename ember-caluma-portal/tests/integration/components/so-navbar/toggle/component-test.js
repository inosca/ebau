import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "caluma-portal/tests/helpers";

module("Integration | Component | so-navbar/toggle", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    await render(hbs`<SoNavbar::Toggle />`);

    assert.dom("button").exists();
    assert.dom("button > span").exists({ count: 3 });
  });
});
