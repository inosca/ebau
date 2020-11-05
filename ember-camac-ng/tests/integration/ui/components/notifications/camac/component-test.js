import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | notifications/camac", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    this.notification = { message: "Test", type: "error" };
    this.onClick = () => {};

    await render(
      hbs`<Notifications::Camac
        @notification={{this.notification}}
        @onClick={{this.onClick}}
      />`
    );

    assert.dom(".alert.hinweisbox.buttonstyle.error").hasText("Test");
  });
});
