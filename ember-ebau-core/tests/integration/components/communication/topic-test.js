import { render, fillIn, click, waitFor } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | communication/topic", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks, "de");

  hooks.beforeEach(function () {
    this.owner.lookup("service:ebauModules").resolveModuleRoute = (
      _,
      routeName
    ) => routeName;
  });

  test("it renders a topic", async function (assert) {
    assert.expect(7);

    this.topic = this.server.create("communications-topic", {});
    this.server.createList("communications-message", 4, {
      topic: this.topic,
    });

    await render(hbs`<Communication::Topic @topicId={{this.topic.id}}/>`);

    assert.dom("[data-test-subject]").hasText(this.topic.subject);
    assert
      .dom("[data-test-created-by]")
      .hasText(
        `Erstellt von ${this.topic.initiatedByEntity.name} (${this.topic.initiatedBy.name} ${this.topic.initiatedBy.surname})`
      );
    assert.dom("[data-test-message-list]").exists();
    assert.dom("[data-test-message-input]").exists();
    assert.dom("[data-test-no-replies]").doesNotExist();

    assert
      .dom("[data-test-message-list] [data-test-message]")
      .exists({ count: 4 });
    await fillIn("[data-test-message-input] textarea", "New message");
    await click("[data-test-message-input] [data-test-send]");
    // The click awaiter is not waiting for the concurrency task to finish for some reason
    await waitFor('[data-test-message="5"]', { timeout: 200 });
    assert
      .dom("[data-test-message-list] [data-test-message]")
      .exists({ count: 5 });
  });

  test("it renders a read only topic", async function (assert) {
    assert.expect(3);

    this.topic = this.server.create("communications-topic", {
      allowReplies: false,
    });
    this.server.createList("communications-message", 4, {
      topic: this.topic,
    });

    await render(hbs`<Communication::Topic @topicId={{this.topic.id}}/>`);

    assert.dom("[data-test-message-input]").doesNotExist();
    assert.dom("[data-test-no-replies]").exists();

    assert
      .dom("[data-test-message-list] [data-test-message]")
      .exists({ count: 4 });
  });
});
