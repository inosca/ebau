import Service from "@ember/service";
import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "camac-ng/tests/helpers";

module("Integration | Helper | shoebox-value", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    this.owner.register(
      "service:shoebox",
      class ShoeboxStub extends Service {
        content = { foo: { bar: 1 } };
        bar = { baz: 2 };
      }
    );

    await render(hbs`{{shoebox-value "foo.bar"}}`);
    assert.dom(this.element).hasText("1");

    await render(hbs`{{shoebox-value "bar.baz"}}`);
    assert.dom(this.element).hasText("2");
  });
});
