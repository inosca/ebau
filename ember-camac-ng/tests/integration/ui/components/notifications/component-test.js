import { render, settled, click } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | notifications", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    const service = this.owner.lookup("service:notifications");

    await render(hbs`<Notifications />`);

    assert.dom(".uk-alert").doesNotExist();

    service.error("Test");
    await settled();

    assert.dom(".uk-alert.uk-alert-danger").exists();
    assert.dom(".uk-alert.uk-alert-danger").containsText("Test");

    service.success("Test");
    await settled();

    assert.dom(".uk-alert.uk-alert-success").exists();
    assert.dom(".uk-alert.uk-alert-danger").containsText("Test");

    assert.dom(".uk-alert").exists({ count: 2 });

    assert.strictEqual(service.all.length, 2);
    await click(".uk-alert:first-of-type .uk-close");
    assert.strictEqual(service.all.length, 1);

    assert.dom(".uk-alert").exists({ count: 1 });
  });
});
