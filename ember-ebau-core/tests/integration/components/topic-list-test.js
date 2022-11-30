import { render, click } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";
import { setupMirage } from "ember-cli-mirage/test-support";

module("Integration | Component | communication/topic-list", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks, "de");

  test("it renders instance list", async function (assert) {
    this.instance = this.server.create("instance", "withTopics");

    await render(
      hbs`<Communication::TopicList @detailRoute="detail" @instance={{this.instance.id}} @newRoute="new" />`
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
        firstTopic.involvedEntities.models
          .map((entity) => entity.service.name)
          .join("\n")
      );
  });

  test("it renders global list", async function (assert) {
    const instance = this.server.create("instance", "withTopics");

    await render(hbs`<Communication::TopicList @detailRoute="application"/>`);

    assert.dom("[data-test-new-topic]").doesNotExist();
    assert.dom("[data-test-instance-header]").exists();
    assert.dom("[data-test-topic]").exists({ count: 5 });

    assert
      .dom("[data-test-dossier-number]")
      .hasText(`${instance.dossierNumber} (${instance.id})`);
  });

  test("it toggles between read and unread", async function (assert) {
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
      hbs`<Communication::TopicList @detailRoute="detail" @instance={{1}} @newRoute="new" />`
    );

    assert.dom("[data-test-topic]").exists({ count: 2 });
    assert.dom("[data-test-topic].uk-text-bold").exists({ count: 1 });

    await click("button[data-test-show-unread]");

    const requests = this.server.pretender.handledRequests;
    assert.deepEqual(requests[requests.length - 1].queryParams, {
      has_unread: "true",
      instance: instance.id,
      include: "instance,involved_entities",
    });
  });
});
