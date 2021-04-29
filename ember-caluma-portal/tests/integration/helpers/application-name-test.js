import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupRenderingTest } from "ember-qunit";
import { module } from "qunit";

import testIf from "caluma-portal/tests/helpers/test-if";

module("Integration | Helper | application-name", function (hooks) {
  setupRenderingTest(hooks);

  testIf("be")("it works", async function (assert) {
    await render(hbs`{{application-name}}`);

    assert.equal(this.element.textContent.trim(), "be");
  });
});
