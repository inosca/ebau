import Service from "@ember/service";
import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";
import { v4 } from "uuid";

module("Integration | Component | qr-code", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    this.owner.register(
      "service:shoebox",
      class extends Service {
        content = { config: { portalURL: location.origin } };
      }
    );

    const uuid = v4();

    this.field = { document: { uuid } };
    this.context = { instanceId: 1 };

    await render(hbs`
      <QrCode
        @field={{this.field}}
        @context={{this.context}}
      />
    `);

    assert.dom("img").exists();
    assert.dom("img").hasAttribute("src", /^data:image\/png/);
    assert
      .dom("img")
      .hasAttribute(
        "alt",
        `${location.origin}/public-instances/1?key=${uuid.substr(0, 7)}`
      );
  });
});
