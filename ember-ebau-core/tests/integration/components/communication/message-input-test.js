import { getOwner } from "@ember/application";
import { render, fillIn, click } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupRenderingTest } from "ember-qunit";
import { module, test, todo } from "qunit";

module(
  "Integration | Component | communication/message-input",
  function (hooks) {
    setupRenderingTest(hooks);

    hooks.beforeEach(function () {
      this.owner.lookup("service:ebauModules").resolveModuleRoute = (
        _,
        routeName,
      ) => routeName;
    });

    test("it renders without a send button", async function (assert) {
      await render(hbs`<Communication::MessageInput />`);

      assert.dom(".communications-message-input").exists();
      assert.dom("textarea").exists();
      assert.dom("input").exists();
      assert.dom("[data-test-select-files]").exists();
      assert.dom("[data-test-send]").doesNotExist();
    });

    test("it renders with a send button", async function (assert) {
      this.sendMessage = () => {};

      await render(hbs`
      <Communication::MessageInput @sendMessage={{this.sendMessage}} />`);

      assert.dom(".communications-message-input").exists();
      assert.dom("textarea").exists();
      assert.dom("input").exists();
      assert.dom("[data-test-select-files]").exists();
      assert.dom("[data-test-send]").exists();
    });

    test("it renders, updates and sends a message", async function (assert) {
      const store = getOwner(this).lookup("service:store");
      this.message = store.createRecord("communications-message");

      const testInput = "Test input";

      this.updateMessage = (value) => {
        assert.step("update");
        assert.strictEqual(value, testInput);
        this.message.body = value;
      };

      this.sendMessage = () => {
        assert.step("send");
      };

      await render(hbs`
      <Communication::MessageInput
        @message={{this.message}}
        @updateMessage={{this.updateMessage}}
        @sendMessage={{this.sendMessage}}
      />`);

      await fillIn("textarea", testInput);
      await click("[data-test-send]");
      assert.verifySteps(["update", "send"]);
    });

    test("it is disabled if @disabled or @loading is passed", async function (assert) {
      this.sendMessage = () => {};
      this.set("disabled", false);
      this.set("loading", false);
      this.message = { body: "test" };

      await render(hbs`
      <Communication::MessageInput
        @message={{this.message}}
        @disabled={{this.disabled}}
        @loading={{this.loading}}
        @sendMessage={{this.sendMessage}}
      />`);

      assert.dom("[data-test-select-files]").exists();
      assert.dom("[data-test-send]").isNotDisabled();

      this.set("disabled", true);
      assert.dom("[data-test-select-files]").doesNotExist();
      assert.dom("[data-test-send]").isDisabled();

      this.set("disabled", false);
      this.set("loading", true);
      assert.dom("[data-test-select-files]").doesNotExist();
      assert.dom("[data-test-send]").isDisabled();

      this.set("disabled", true);
      this.set("loading", true);
      assert.dom("[data-test-select-files]").doesNotExist();
      assert.dom("[data-test-send]").isDisabled();
    });

    test("it show loading state if @loading", async function (assert) {
      this.sendMessage = () => {};
      this.set("loading", false);

      await render(hbs`
      <Communication::MessageInput
        @disabled={{this.disabled}}
        @loading={{this.loading}}
        @sendMessage={{this.sendMessage}}
      />`);

      assert.dom("[data-test-loading]").doesNotExist();
      this.set("loading", true);
      assert.dom("[data-test-loading]").exists();
    });

    todo("it selects files", async function () {
      await render(hbs`
      <Communication::MessageInput
        @message={{this.message.value}}
        @updateMessage={{this.updateMessage}}
        @updateFiles={{this.updateFiles}}
      />`);
    });
  },
);
