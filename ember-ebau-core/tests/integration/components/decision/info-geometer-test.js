import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | decision/info-geometer", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  test("it renders", async function (assert) {
    const instance = this.server.create("instance");
    const municipalityId = instance.activeService.id;
    this.set("context", { instanceId: instance.id });

    this.set("field", {
      raw: {
        question: {
          staticContent: "some <b>rich</b> text",
        },
      },
    });

    this.server.get("/api/v1/public-services", (_, request) => {
      assert.deepEqual(request.queryParams, {
        provider_for: `geometer;${municipalityId}`,
      });

      return {
        data: [
          {
            type: "public-services",
            id: "123456",
            attributes: {
              name: "Test Geometer",
              website: null,
            },
          },
        ],
      };
    });

    await render(
      hbs`<Decision::InfoGeometer @context={{this.context}} @field={{this.field}} />`,
    );

    assert.dom(this.element).includesText("some rich text");
    assert.dom(this.element).includesText("Test Geometer");
  });
});
