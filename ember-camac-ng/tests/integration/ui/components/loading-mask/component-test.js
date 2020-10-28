import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | loading-mask", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    await render(hbs`<LoadingMask />`);

    assert.dom("#dialog-loading").doesNotExist();
    assert.dom(".overlay").doesNotExist();

    await render(hbs`<LoadingMask @visible={{true}} />`);

    assert.dom("#dialog-loading").exists();
    assert.dom("#dialog-loading").hasClass("visible");
    assert.dom(".overlay").exists();
    assert.dom(".overlay").hasClass("visible");
  });
});
