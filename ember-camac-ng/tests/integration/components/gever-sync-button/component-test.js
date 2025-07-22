import { getOwner } from "@ember/application";
import { click, render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "camac-ng/tests/helpers";

module("Integration | Component | gever-sync-button", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    this.context = { instanceId: 1 };
    const fetch = getOwner(this).lookup("service:fetch");
    fetch.fetch = (url, options) => {
      assert.strictEqual(url, "/api/v1/instances/1/sync-gever");
      assert.strictEqual(options.method, "POST");
      assert.step("fetch");
    };

    await render(hbs`<GeverSyncButton @context={{this.context}} />`);

    await click("button[data-test-gever-button]");

    assert.verifySteps(["fetch"]);
  });
});
