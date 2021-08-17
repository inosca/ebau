import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

import config from "caluma-portal/config/environment";

module("Integration | Helper | has-feature", function (hooks) {
  setupRenderingTest(hooks);

  test("it returns whether a feature is enabled or not", async function (assert) {
    await render(hbs`{{#if (has-feature "foo.bar")}}<button></button>{{/if}}`);

    assert.dom("button").doesNotExist();

    config.APPLICATION.features.foo = { bar: true };
    await render(hbs`{{#if (has-feature "foo.bar")}}<button></button>{{/if}}`);

    assert.dom("button").exists();
  });
});
