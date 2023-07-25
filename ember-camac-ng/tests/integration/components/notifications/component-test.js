import { render, settled, click } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "camac-ng/tests/helpers";

module("Integration | Component | notification", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders different types", async function (assert) {
    const service = this.owner.lookup("service:notification");

    await render(hbs`<Notifications />`);

    assert.dom(".uk-alert").doesNotExist();

    const types = ["default", "primary", "success", "warning", "danger"];

    await Promise.all(
      types.map(async (type) => {
        service[type](`Test: ${type}`);

        await settled();

        assert.dom(`.uk-alert.uk-alert-${type}`).exists();
        assert.dom(`.uk-alert.uk-alert-${type}`).containsText(`Test: ${type}`);
      }),
    );
  });

  test("it can remove a notification", async function (assert) {
    const service = this.owner.lookup("service:notification");

    await render(hbs`<Notifications />`);

    assert.dom(".uk-alert").doesNotExist();
    service.danger("Test");
    await settled();
    assert.dom(".uk-alert").exists({ count: 1 });
    assert.strictEqual(service.all.length, 1);

    await click(".uk-alert:first-of-type .uk-close");

    assert.strictEqual(service.all.length, 0);
    assert.dom(".uk-alert").doesNotExist();
  });
});
