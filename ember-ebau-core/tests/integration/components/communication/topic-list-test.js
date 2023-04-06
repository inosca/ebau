import { render, click, waitFor } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";
import sinon from "sinon";

module("Integration | Component | communication/topic-list", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks, "de");

  test("it renders topic list", async function (assert) {
    assert.expect(7);
    this.instance = this.server.create("instance", "withTopics");

    await render(
      hbs`<Communication::TopicList @detailRoute="detail" @instanceId={{this.instance.id}} @newRoute="new" />`
    );

    assert.dom("[data-test-new-topic]").exists();
    assert.dom("[data-test-show-all]").hasClass("uk-button-primary");
    assert.dom("[data-test-show-unread]").hasClass("uk-button-default");

    assert.dom("[data-test-topic]").exists({ count: 5 });

    const unreads = this.server.schema.communicationsTopics.where({
      hasUnread: true,
    }).length;
    assert.dom("[data-test-topic].uk-text-bold").exists({ count: unreads });

    const firstTopic = this.server.schema.communicationsTopics.where({
      instanceId: this.instance.id,
    })?.models[0];

    assert.dom("[data-test-subject]").hasText(firstTopic.subject);
    assert
      .dom("[data-test-involved-entities]")
      .hasText(
        firstTopic.involvedEntities.map((entity) => entity.name).join("\n")
      );
  });

  test("it renders global list", async function (assert) {
    assert.expect(4);
    const instance = this.server.create("instance", "withTopics");

    await render(hbs`<Communication::TopicList @detailRoute="application"/>`);

    assert.dom("[data-test-new-topic]").doesNotExist();
    assert.dom("[data-test-instance-header]").exists();
    assert.dom("[data-test-topic]").exists({ count: 5 });

    assert
      .dom("[data-test-dossier-number]")
      .hasText(
        `${this.server.db.communicationsTopics[0].dossierNumber} (${instance.id})`
      );
  });

  test("it toggles between all, read and unread", async function (assert) {
    assert.expect(5);
    const instance = this.server.create("instance");
    this.server.create("communications-topic", {
      hasUnread: true,
      instanceId: instance.id,
    });
    this.server.create("communications-topic", {
      hasUnread: false,
      instanceId: instance.id,
    });

    await render(
      hbs`<Communication::TopicList @detailRoute="detail" @instanceId={{1}} @newRoute="new" />`
    );

    assert.dom("[data-test-topic]").exists({ count: 2 });
    assert.dom("[data-test-topic].uk-text-bold").exists({ count: 1 });

    await click("button[data-test-show-unread]");

    const requests = this.server.pretender.handledRequests;
    assert.deepEqual(requests[requests.length - 1].queryParams, {
      has_unread: "true",
      instance: instance.id,
      include: "instance",
      order: "-created_at",
      "page[number]": "1",
      "page[size]": "20",
    });

    await click("button[data-test-show-read]");
    assert.deepEqual(requests[requests.length - 1].queryParams, {
      has_unread: "false",
      instance: instance.id,
      include: "instance",
      order: "-created_at",
      "page[number]": "1",
      "page[size]": "20",
    });

    await click("button[data-test-show-all]");
    assert.deepEqual(requests[requests.length - 1].queryParams, {
      instance: instance.id,
      include: "instance",
      order: "-created_at",
      "page[number]": "1",
      "page[size]": "20",
    });
  });

  test("it links to detail and new", async function (assert) {
    assert.expect(4);
    this.server.create("communications-topic");

    const router = this.owner.lookup("service:router");
    const routing = this.owner.lookup("service:-routing");

    const detailFake = sinon.replace(
      router,
      "transitionTo",
      sinon.fake.returns("transisioned")
    );
    const newFake = sinon.replace(
      routing,
      "transitionTo",
      sinon.fake.returns("transisioned")
    );

    await render(
      hbs`<Communication::TopicList @detailRoute="detail" @instanceId={{1}} @newRoute="new" />`
    );

    await click("[data-test-new-topic]");
    await click("[data-test-topic]");

    assert.strictEqual(detailFake.callCount, 1);
    assert.strictEqual(detailFake.args[0][0], "detail");
    assert.strictEqual(newFake.callCount, 1);
    assert.strictEqual(newFake.args[0][0], "new");
  });

  test("it has infinite loading and resets page on query change", async function (assert) {
    assert.expect(5);
    this.server.createList("communications-topic", 40);

    await render(
      hbs`<Communication::TopicList @detailRoute="detail" @instanceId={{1}} @newRoute="new" />`
    );

    assert.dom("[data-test-topic]").exists({ count: 20 });

    // I could`t get the scrollTo helper to work here and this works perfect.
    this.element.querySelector("tbody>tr:last-child").scrollIntoView();
    await waitFor("[data-test-topic]", { count: 40 });

    assert.dom("[data-test-topic]").exists({ count: 40 });

    let requests = this.server.pretender.handledRequests;
    assert.deepEqual(requests[requests.length - 1].queryParams, {
      instance: "1",
      include: "instance",
      order: "-created_at",
      "page[number]": "2",
      "page[size]": "20",
    });

    await click("button[data-test-show-unread]");
    assert.dom("[data-test-topic]").exists({ count: 20 });

    requests = this.server.pretender.handledRequests;
    assert.deepEqual(requests[requests.length - 1].queryParams, {
      has_unread: "true",
      instance: "1",
      include: "instance",
      order: "-created_at",
      "page[number]": "1",
      "page[size]": "20",
    });
  });

  test("it has scroll to top button", async function (assert) {
    assert.expect(3);
    this.server.createList("communications-topic", 20);

    await render(
      hbs`<Communication::TopicList @detailRoute="detail" @instanceId={{1}} @newRoute="new" />`
    );

    assert.dom("[data-test-topic]").exists({ count: 20 });
    // I could`t get the scrollTo helper to work here and this works perfect.
    this.element.querySelector("tbody>tr:last-child").scrollIntoView();
    const scrollIntoViewFake = sinon.replace(
      this.element.querySelector("tbody>tr:first-child"),
      "scrollIntoView",
      sinon.fake()
    );
    assert.strictEqual(scrollIntoViewFake.callCount, 0);
    await click("[data-test-back-to-first]");
    assert.strictEqual(scrollIntoViewFake.callCount, 1);
  });
});
