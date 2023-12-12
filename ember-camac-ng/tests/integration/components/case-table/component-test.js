import Service from "@ember/service";
import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, skip } from "qunit";

import { setupRenderingTest } from "camac-ng/tests/helpers";

class FakeShoebox extends Service {
  get content() {
    return { role: "municipality" };
  }
}

module("Integration | Component | case-table", function (hooks) {
  setupRenderingTest(hooks);

  hooks.beforeEach(async function () {
    this.owner.register("service:shoebox", FakeShoebox);
  });

  skip("it renders", async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    this.set("filter", {});
    await render(hbs`<CaseTable @filter={{this.filter}}/>`);

    assert.ok(this.element.textContent.trim());
  });
});
