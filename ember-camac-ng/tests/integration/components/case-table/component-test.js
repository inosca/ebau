import Service from "@ember/service";
import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, skip } from "qunit";

class FakeShoebox extends Service {
  get content() {
    return { role: "municipality" };
  }
}

module("Integration | Component | case-table", function (hooks) {
  setupRenderingTest(hooks);
  setupIntl(hooks);

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
