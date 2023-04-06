import { getOwner } from "@ember/application";
import { render, click } from "@ember/test-helpers";
import { faker } from "@faker-js/faker";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import { DateTime } from "luxon";
import { module, test } from "qunit";
import sinon from "sinon";

module("Integration | Component | communication/message", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks, "de");

  hooks.beforeEach(async function () {
    this.mirageMessage = this.server.create("communications-message", {
      topic: this.server.create("communications-topic"),
    });
    this.store = getOwner(this).lookup("service:store");
    await this.store.findRecord(
      "communications-topic",
      this.mirageMessage.topicId
    );
    this.message = await this.store.findRecord(
      "communications-message",
      this.mirageMessage.id
    );
    this.refresh = sinon.fake(() => {});
  });

  hooks.afterEach(async function () {
    this.mirageMessage = undefined;
    this.store = undefined;
    this.message = undefined;
    this.refresh = undefined;
  });

  test("it renders a read message", async function (assert) {
    assert.expect(9);

    this.mirageMessage.update({
      body: "Hello there, Im a test message, so you you should probably not respond.",
      createdAt: DateTime.fromISO("2020-02-12T08:12:21").toISO(),
    });
    await this.message.reload();

    await render(
      hbs`<Communication::Message @message={{this.message}} @refresh={{this.refresh}} />`
    );

    assert
      .dom("[data-test-created-by]")
      .hasText(
        `${this.message.createdBy.name} (${this.message.get(
          "createdByUser.fullName"
        )})`
      );
    assert.dom("[data-test-sent-date]").hasText("am 12.2.2020 um 08:12");
    assert.dom("[data-test-read-details-trigger]").exists();
    // Not testing the uikit dropdown visibility here since it's very flaky
    assert.dom("[data-test-mark-unread]").exists();
    assert.dom("[data-test-mark-read]").doesNotExist();
    assert.dom("[data-test-expand]").hasClass("collapsed");
    assert.dom("[data-test-expand]").doesNotHaveClass("expandable");
    assert.dom("[data-test-collapse]").doesNotExist();

    assert.strictEqual(this.refresh.callCount, 0);
  });

  test("it renders a unread message", async function (assert) {
    assert.expect(7);

    this.mirageMessage.update({
      readAt: null,
    });
    await this.message.reload();

    await render(
      hbs`<Communication::Message @message={{this.message}} @refresh={{this.refresh}} />`
    );

    assert.dom("[data-test-read-details-trigger]").doesNotExist();
    assert.dom("[data-test-read-details]").doesNotExist();
    assert.dom("[data-test-mark-unread]").doesNotExist();
    assert.dom("[data-test-mark-read]").exists();

    await click("[data-test-mark-read]");

    const requests = this.server.pretender.handledRequests;
    const { url, response } = requests[requests.length - 1];

    assert.deepEqual(
      url,
      `/api/v1/communications-messages/${this.message.id}/read`
    );
    assert.ok(JSON.parse(response)?.data?.attributes?.["read-at"]);
    assert.strictEqual(this.refresh.callCount, 0);
  });

  test("it marks a message as unread", async function (assert) {
    assert.expect(7);

    await render(
      hbs`<Communication::Message @message={{this.message}} @refresh={{this.refresh}} />`
    );

    assert.dom("[data-test-read-details-trigger]").exists();
    assert.dom("[data-test-read-details]").exists();
    assert.dom("[data-test-mark-unread]").exists();
    assert.dom("[data-test-mark-read]").doesNotExist();

    await click("[data-test-mark-unread]");

    const requests = this.server.pretender.handledRequests;
    const { url, response } = requests[requests.length - 1];

    assert.deepEqual(
      url,
      `/api/v1/communications-messages/${this.message.id}/unread`
    );
    assert.notOk(JSON.parse(response)?.data?.attributes?.["read-at"]);
    assert.strictEqual(this.refresh.callCount, 0);
  });

  test("it renders collapsed message", async function (assert) {
    assert.expect(10);

    this.mirageMessage.update({
      body: faker.lorem.paragraphs(3),
    });
    await this.message.reload();

    await render(
      hbs`<Communication::Message @message={{this.message}} @refresh={{this.refresh}} />`
    );

    assert.dom("[data-test-expand]").hasClass("collapsed");
    assert.dom("[data-test-expand]").hasClass("expandable");
    assert.dom("[data-test-collapse]").doesNotExist();

    await click("[data-test-expand]");
    assert.dom("[data-test-expand]").doesNotHaveClass("collapsed");
    assert.dom("[data-test-expand]").hasClass("expandable");
    assert.dom("[data-test-collapse]").exists();

    await click("[data-test-collapse]");
    assert.dom("[data-test-expand]").hasClass("collapsed");
    assert.dom("[data-test-expand]").hasClass("expandable");
    assert.dom("[data-test-collapse]").doesNotExist();
    assert.strictEqual(this.refresh.callCount, 0);
  });
});
