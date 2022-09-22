import { render, triggerEvent, settled } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | thumbnail", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  test("it renders", async function (assert) {
    await render(hbs`<Thumbnail />`);
    await triggerEvent("[uk-dropdown]", "beforeshow");
    // eslint-disable-next-line ember/no-settled-after-test-helper
    await settled();

    assert.dom("img").exists();
  });
});
