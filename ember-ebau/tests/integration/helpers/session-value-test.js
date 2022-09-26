import Service from "@ember/service";
import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "ebau/tests/helpers";

module("Integration | Helper | session-value", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    this.owner.register(
      "service:session",
      class SessionStub extends Service {
        foo = { bar: 1 };
      }
    );

    await render(hbs`{{session-value "foo.bar"}}`);
    assert.dom(this.element).hasText("1");
  });
});
