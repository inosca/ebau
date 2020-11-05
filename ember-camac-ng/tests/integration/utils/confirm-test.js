import { click } from "@ember/test-helpers";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

import confirm from "camac-ng/utils/confirm";

module("Integration | Utility | confirm", function (hooks) {
  setupRenderingTest(hooks);
  setupIntl(hooks);

  test("it works", async function (assert) {
    assert.expect(4);

    const okResult = confirm("Test");
    okResult.then((result) => assert.ok(result));

    assert.dom(".uk-modal-footer .uk-button-primary").hasText("t:global.ok:()");
    assert
      .dom(".uk-modal-footer .uk-button-default")
      .hasText("t:global.cancel:()");
    assert.dom(".uk-modal-body").hasText("Test");

    await click(".uk-modal-footer .uk-button-primary");
  });
});
