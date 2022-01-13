import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | notifications/uikit", function (hooks) {
  setupRenderingTest(hooks);
  setupIntl(hooks);

  test("it renders", async function (assert) {
    this.notification = { message: "Test", type: "error" };
    this.onClick = () => {};

    await render(
      hbs`<Notifications::Uikit
        @notification={{this.notification}}
        @onClick={{this.onClick}}
      />`
    );

    assert.dom(".uk-alert.uk-alert-danger").hasText("t:global.close:() Test");
  });
});
