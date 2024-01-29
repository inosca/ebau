import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";
import setupPermissions from "dummy/tests/helpers/permissions";

module("Integration | Helper | has-any-permission", function (hooks) {
  setupRenderingTest(hooks);
  setupPermissions(hooks, 1, []);

  test("it works", async function (assert) {
    this.required = ["form-read", "form-write"];

    await render(hbs`{{has-any-permission 1 this.required reload=true}}`);

    assert.dom(this.element).hasText("false");
    this.permissions.grant(1, ["form-read"]);

    await render(hbs`{{has-any-permission 1 this.required reload=true}}`);

    assert.dom(this.element).hasText("true");
  });

  test("it works with positional params", async function (assert) {
    this.permissions.grant(1, ["form-read"]);
    await render(
      hbs`{{has-any-permission 1 "form-read" "form-write" reload=true}}`,
    );
    assert.dom(this.element).hasText("true");
  });
});
