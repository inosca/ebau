import { render } from "@ember/test-helpers";
import { getOwnConfig } from "@embroider/macros";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";
import { v4 } from "uuid";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | qr-code", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    const portalUrl = getOwnConfig().portalUrl;
    const uuid = v4();

    this.field = { document: { uuid } };
    this.context = { instanceId: 1 };

    await render(
      hbs`<QrCode @field={{this.field}} @context={{this.context}} />`,
    );

    assert.dom("img").exists();
    assert.dom("img").hasAttribute("src", /^data:image\/png/);
    assert
      .dom("img")
      .hasAttribute(
        "alt",
        `${portalUrl}/public-instances/1?key=${uuid.substring(0, 7)}`,
      );
  });
});
