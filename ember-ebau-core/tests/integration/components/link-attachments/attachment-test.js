import { render, click } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { task } from "ember-concurrency";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module(
  "Integration | Component | link-attachments/attachment",
  function (hooks) {
    setupRenderingTest(hooks);

    test("it renders", async function (assert) {
      this.attachment = new (class {
        id = 1;
        thumbnail = { value: "base64-thumbnail" };
        @task
        *download() {
          yield assert.step("download");
        }
      })();

      this.toggle = (id) => {
        assert.strictEqual(id, 1);
        assert.step("toggle");
      };

      await render(hbs`
        <LinkAttachments::Attachment
          @attachment={{this.attachment}}
          @onToggle={{this.toggle}}
        />
      `);

      assert
        .dom(".link-attachments__preview")
        .hasAttribute("style", "background-image: url(base64-thumbnail);");

      await click("button[data-test-download]");
      assert.verifySteps(["download"]);

      await click("button[data-test-toggle]");
      assert.verifySteps(["toggle"]);
    });
  },
);
