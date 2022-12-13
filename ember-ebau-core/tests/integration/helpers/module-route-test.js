import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Helper | module-route", function (hooks) {
  setupRenderingTest(hooks);

  test("it resolves to the correct route", async function (assert) {
    this.owner.lookup("service:ebau-modules").registeredModules = {
      "my-module": { path: "test.testy" },
    };

    await render(hbs`{{module-route "my-module" "foo.bar"}}`);

    assert.dom(this.element).hasText("test.testy.my-module.foo.bar");

    await render(hbs`{{module-route "my-module" "my-module.foo.bar"}}`);

    assert.dom(this.element).hasText("test.testy.my-module.foo.bar");
  });
});
