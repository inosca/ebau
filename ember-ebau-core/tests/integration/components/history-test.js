import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | history", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  test("it renders", async function (assert) {
    const entry = this.server.create("history-entry");
    await render(hbs`<History @instanceId={{2}} />`);

    assert.dom(this.element).containsText(entry.title);
  });
});
