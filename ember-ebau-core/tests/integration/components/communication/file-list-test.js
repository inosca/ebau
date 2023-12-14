import { render, click } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { task } from "ember-concurrency";
import { module, test } from "qunit";
import { fake, stub } from "sinon";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | communication/file-list", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders with delete", async function (assert) {
    this.files = [
      {
        name: "File A",
      },
      {
        name: "File B",
      },
    ];
    this.removeFile = fake(() => {});

    await render(
      hbs`<Communication::FileList @files={{this.files}} @removeFile={{this.removeFile}}/>`,
    );

    assert.dom("[data-test-attachment]").exists({ count: 2 });
    assert.dom("[data-test-attachment]:nth-child(1) span").hasText("File A");
    await click("[data-test-remove-attachment]");
    assert.strictEqual(this.removeFile.args[0][0].name, "File A");
  });

  test("it renders with download", async function (assert) {
    const File = class {
      id = 1;
      name = "File A";
      downloadUrl = "test";
      documentAttachment = {
        content: {
          context: {
            displayName: "New Name File A",
            isReplaced: true,
          },
        },
      };
      @task download() {}
    };

    this.files = [new File()];
    const performFake = stub(this.files[0].download, "perform");

    await render(hbs`<Communication::FileList @files={{this.files}} />`);

    await click("[data-test-attachment]:nth-child(1) a");
    assert.strictEqual(performFake.callCount, 1);
  });
});
