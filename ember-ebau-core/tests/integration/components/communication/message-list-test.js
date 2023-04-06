import { getOwner } from "@ember/application";
import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";
import sinon from "sinon";

module(
  "Integration | Component | communication/message-list",
  function (hooks) {
    setupRenderingTest(hooks);
    setupMirage(hooks);

    hooks.beforeEach(async function () {
      this._scrollIntoView = Element.prototype.scrollIntoView;
      this.scrollIntoViewFake = sinon.replace(
        Element.prototype,
        "scrollIntoView",
        sinon.fake(Element.prototype.scrollIntoView)
      );
    });

    hooks.afterEach(async function () {
      Element.prototype.scrollIntoView = this._scrollIntoView;
      this._scrollIntoView = null;
    });

    test("it renders and scrolls to last element", async function (assert) {
      assert.expect(5);

      const topic = this.server.create("communications-topic");
      this.server.createList("communications-message", 10, {
        topic,
      });
      const store = getOwner(this).lookup("service:store");
      await store.findRecord("communications-topic", topic.id);
      this.set("messages", []);
      this.refresh = () => {};

      await render(
        hbs`<Communication::MessageList @messages={{this.messages}} @refresh={{this.refresh}}/>`
      );

      assert.dom("[data-test-empty]").exists();

      this.set("messages", await store.findAll("communications-message"));
      assert.dom("[data-test-empty]").doesNotExist();
      assert.dom("[data-test-message]").exists({ count: 10 });
      assert.strictEqual(this.scrollIntoViewFake.callCount, 1);
      assert.strictEqual(
        this.scrollIntoViewFake.lastCall.thisValue.dataset.testMessage,
        this.messages.lastObject.id
      );
    });
  }
);
