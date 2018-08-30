import { module, test } from "qunit";
import { setupRenderingTest } from "ember-qunit";
import { render, fillIn, click } from "@ember/test-helpers";
import hbs from "htmlbars-inline-precompile";

module("Integration | Component | camac-gwr-building", function(hooks) {
  setupRenderingTest(hooks);

  hooks.beforeEach(function() {
    this.set("value", {
      uuid: "testuuid",
      f1: "test f1",
      f2: "2",
      f3: ["3", "2"],
      f4: [
        {
          col1: "test"
        }
      ]
    });
    this.set("columns", [
      {
        name: "f1",
        label: "F1",
        required: true,
        type: "text",
        config: {}
      },
      {
        name: "f2",
        label: "F2",
        required: true,
        type: "number",
        config: { max: 10 }
      },
      {
        name: "f3",
        label: "F3",
        required: false,
        type: "checkbox",
        config: { options: ["1", "2", "3"] }
      },
      {
        name: "f4",
        label: "F4",
        required: true,
        type: "table",
        config: {
          columns: [
            {
              name: "col1",
              label: "Col 1",
              type: "text",
              required: true,
              config: {}
            }
          ]
        }
      }
    ]);
  });

  test("validates input", async function(assert) {
    assert.expect(8);

    await render(hbs`{{camac-gwr-building value=value columns=columns}}`);

    assert.dom(".uk-margin:nth-child(1) input").hasValue("test f1");
    assert.dom(".uk-margin:nth-child(2) input").hasValue("2");
    assert.dom('.uk-margin:nth-child(3) input[value="2"]').isChecked();
    assert.dom('.uk-margin:nth-child(3) input[value="3"]').isChecked();

    await fillIn(".uk-margin:nth-child(1) input", "");
    await fillIn(".uk-margin:nth-child(2) input", "123");
    await click(".uk-margin:nth-child(3) label:nth-child(2)");
    await click(".uk-margin:nth-child(3) label:nth-child(3)");
    await click("table [data-test-delete-row]");

    await click(".uk-button-primary");

    assert.dom(".uk-margin:nth-child(1) ul.uk-text-danger").exists();
    assert.dom(".uk-margin:nth-child(2) ul.uk-text-danger").exists();
    assert.dom(".uk-margin:nth-child(3) ul.uk-text-danger").doesNotExist();
    assert.dom(".uk-margin:nth-child(4) ul.uk-text-danger").exists();
  });

  test("it can delete", async function(assert) {
    assert.expect(2);

    this.set("delete", () => {
      assert.step("delete");
    });

    await render(
      hbs`{{camac-gwr-building value=value columns=columns on-delete=(action delete)}}`
    );

    await click(".uk-card-footer button.uk-button-default");

    assert.verifySteps(["delete"]);
  });

  test("it can save", async function(assert) {
    assert.expect(2);

    this.set("save", () => {
      assert.step("save");
    });

    await render(
      hbs`{{camac-gwr-building value=value columns=columns on-save=(action save)}}`
    );

    await click(".uk-card-footer button.uk-button-primary");

    assert.verifySteps(["save"]);
  });

  test("it can close", async function(assert) {
    assert.expect(2);

    this.set("close", () => {
      assert.step("close");
    });

    await render(
      hbs`{{camac-gwr-building value=value columns=columns on-close=(action close)}}`
    );

    await click("[uk-close]");

    assert.verifySteps(["close"]);
  });
});
