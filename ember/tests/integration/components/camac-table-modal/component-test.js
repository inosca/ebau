import { module, test } from "qunit";
import { setupRenderingTest } from "ember-qunit";
import { render, waitFor, click, fillIn } from "@ember/test-helpers";
import hbs from "htmlbars-inline-precompile";

module("Integration | Component | camac-table-modal", function(hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function(assert) {
    this.set("columns", [{ name: "f1", type: "text", config: {} }]);
    this.set("value", { f1: "test" });
    this.set("visible", false);

    await render(
      hbs`{{camac-table-modal visible=visible columns=columns value=value}}`
    );

    assert.dom(".uk-modal.uk-open").doesNotExist();

    this.set("visible", true);

    await waitFor(".uk-modal.uk-open");

    assert.dom(".uk-modal.uk-open").exists();

    assert.dom(".uk-modal input[type=text]").exists();
    assert.dom(".uk-modal input[type=text]").hasValue("test");
  });

  test("it can handle changes", async function(assert) {
    this.set("columns", [{ name: "f1", type: "text", config: {} }]);
    this.set("value", { f1: "test" });

    await render(
      hbs`{{camac-table-modal visible=true columns=columns value=value on-save=(action (mut value))}}`
    );

    await fillIn(".uk-modal input[type=text]", "foobar");
    await click("button[type=submit]");

    assert.equal(this.get("value.f1"), "foobar");
  });

  test("it rollbacks changes on close", async function(assert) {
    this.set("columns", [{ name: "f1", type: "text", config: {} }]);
    this.set("value", { f1: "test" });
    this.set("visible", true);

    await render(
      hbs`{{camac-table-modal visible=visible columns=columns value=value}}`
    );

    await fillIn(".uk-modal input[type=text]", "foobar");
    assert.dom(".uk-modal input[type=text]").hasValue("foobar");

    await click("[uk-close]");

    assert.dom(".uk-modal input[type=text]").hasValue("test");
  });

  test("it validates changes", async function(assert) {
    this.set("columns", [
      { name: "f1", type: "text", required: true, config: {} }
    ]);
    this.set("value", { f1: "test" });
    this.set("visible", true);

    await render(
      hbs`{{camac-table-modal name='testy' visible=visible columns=columns value=value on-save=(action (mut foo))}}`
    );

    await fillIn(".uk-modal input[type=text]", "");

    await click("button[type=submit]");

    assert.dom(".uk-modal ul li:first-child").includesText("darf nicht leer");

    await fillIn(".uk-modal input[type=text]", "test");

    await click("button[type=submit]");

    assert.dom(".uk-modal ul li:first-child").doesNotExist();
  });
});
