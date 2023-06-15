import { getOwner } from "@ember/application";
import { render, fillIn, click, waitUntil } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { selectChoose } from "ember-power-select/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";
import sinon from "sinon";

module("Integration | Component | communication/new-topic", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks, "de");

  hooks.beforeEach(function () {
    this.ebauModules = getOwner(this).lookup("service:ebauModules");
    this.resolveModuleRoute = this.ebauModules.resolveModuleRoute;
    this.ebauModules.resolveModuleRoute = (_, routeName) => routeName;

    this.store = getOwner(this).lookup("service:store");

    this.router = getOwner(this).lookup("service:router");
    this.transitionTo = this.router.transitionTo;
    this.transitionToFake = sinon.replace(
      this.router,
      "transitionTo",
      sinon.fake(() => {})
    );
  });

  hooks.afterEach(function () {
    this.router.transitionTo = this.transitionTo;
    this.transitionTo = null;
    this.transitionToFake = null;
    this.ebauModules.resolveModuleRoute = this.resolveModuleRoute;
    this.ebauModules.reset();
  });

  test("it renders the form for applicant", async function (assert) {
    assert.expect(13);

    this.ebauModules.isApplicant = true;
    this.instance = this.server.create("instance");

    await render(
      hbs`<Communication::NewTopic @instanceId={{this.instance.id}} />`
    );

    assert.dom("[data-test-involved-entities]").doesNotExist();
    assert.dom("[data-test-subject]").exists();
    assert.dom("[data-test-allow-answers]").doesNotExist();
    assert.dom("[data-test-message]").exists();
    assert.dom("[data-test-save]").exists();
    assert.dom("[data-test-save]").isDisabled();
    assert.dom("[data-test-discard]").exists();

    const subject = "Test subject";
    await fillIn("[data-test-subject]", subject);
    await fillIn("[data-test-message] textarea", "Test subject");
    assert.dom("[data-test-save]").isNotDisabled();

    await click("[data-test-save]");
    // Same as in the message-input test, the click helper is not waiting for
    // the concurrency task to finish.
    await waitUntil(() => this.transitionToFake.callCount === 1);

    const requests = this.server.pretender.handledRequests;

    const topicRequest = requests[requests.length - 2];
    assert.strictEqual(topicRequest.url, "/api/v1/communications-topics");
    assert.deepEqual(JSON.parse(topicRequest.requestBody), {
      data: {
        attributes: {
          "allow-replies": true,
          created: null,
          "involved-entities": [
            {
              id: "1",
              name: this.instance.activeService.name,
            },
          ],
          subject,
        },
        relationships: {
          instance: {
            data: {
              id: "1",
              type: "instances",
            },
          },
        },
        type: "communications-topics",
      },
    });

    const messageRequest = requests[requests.length - 1];
    assert.strictEqual(messageRequest.url, "/api/v1/communications-messages");
    assert.strictEqual(this.transitionToFake.callCount, 1);
    assert.strictEqual(this.transitionToFake.lastCall.args[0], "detail");
  });

  test("it renders the form for internal", async function (assert) {
    assert.expect(9);

    const involvedServices = this.server.createList("service", 2);
    this.instance = this.server.create("instance");
    this.instance.update({
      involvedServices,
    });

    await render(
      hbs`<Communication::NewTopic @instanceId={{this.instance.id}} />`
    );

    assert.dom("[data-test-allow-answers]").doesNotExist();

    try {
      // Check applicant is not selectable
      await selectChoose(
        "[data-test-involved-entities]",
        this.intl.t("communications.new.applicant")
      );
    } catch (error) {
      assert.ok(error);
    }

    await selectChoose(
      "[data-test-involved-entities]",
      involvedServices[0].name
    );

    assert
      .dom("[data-test-involved-entities]")
      .hasText(`× ${involvedServices[0].name}`);

    const subject = "Test subject";
    await fillIn("[data-test-subject]", subject);
    await fillIn("[data-test-message] textarea", "Test subject");
    assert.dom("[data-test-save]").isNotDisabled();

    await click("[data-test-save]");
    // Same as in the message-input test, the click helper is not waiting for
    // the concurrency task to finish.
    await waitUntil(() => this.transitionToFake.callCount === 1);

    const requests = this.server.pretender.handledRequests;

    const topicRequest = requests[requests.length - 2];
    assert.strictEqual(topicRequest.url, "/api/v1/communications-topics");
    assert.deepEqual(JSON.parse(topicRequest.requestBody), {
      data: {
        attributes: {
          "allow-replies": true,
          created: null,
          "involved-entities": [
            {
              id: "1",
              name: involvedServices[0].name,
            },
          ],
          subject,
        },
        relationships: {
          instance: {
            data: {
              id: "1",
              type: "instances",
            },
          },
        },
        type: "communications-topics",
      },
    });

    const messageRequest = requests[requests.length - 1];
    assert.strictEqual(messageRequest.url, "/api/v1/communications-messages");
    assert.strictEqual(this.transitionToFake.callCount, 1);
    assert.strictEqual(this.transitionToFake.lastCall.args[0], "detail");
  });

  test("it renders the form for active instance service", async function (assert) {
    assert.expect(8);

    const group = this.server.create("public-group", {
      service: this.server.create("public-service", { name: "test-service" }),
    });
    this.ebauModules.serviceId = group.service.id;
    this.instance = this.server.create("instance", {
      activeService: group.service,
    });

    await render(
      hbs`<Communication::NewTopic @instanceId={{this.instance.id}} />`
    );

    assert.dom("[data-test-allow-answers]").exists();

    const applicant = this.intl.t("communications.new.applicant");
    await selectChoose("[data-test-involved-entities]", applicant);

    assert.dom("[data-test-involved-entities]").hasText(`× ${applicant}`);

    const subject = "Test subject";
    await fillIn("[data-test-subject]", subject);

    await click("[data-test-allow-answers] input[type=checkbox]");

    await fillIn("[data-test-message] textarea", "Test subject");
    assert.dom("[data-test-save]").isNotDisabled();

    await click("[data-test-save]");
    // Same as in the message-input test, the click helper is not waiting for
    // the concurrency task to finish.
    await waitUntil(() => this.transitionToFake.callCount === 1);

    const requests = this.server.pretender.handledRequests;

    const topicRequest = requests[requests.length - 2];
    assert.strictEqual(topicRequest.url, "/api/v1/communications-topics");
    assert.deepEqual(JSON.parse(topicRequest.requestBody), {
      data: {
        attributes: {
          "allow-replies": false,
          created: null,
          "involved-entities": [
            {
              id: "APPLICANT",
              name: applicant,
            },
          ],
          subject,
        },
        relationships: {
          instance: {
            data: {
              id: "1",
              type: "instances",
            },
          },
        },
        type: "communications-topics",
      },
    });

    const messageRequest = requests[requests.length - 1];
    assert.strictEqual(messageRequest.url, "/api/v1/communications-messages");
    assert.strictEqual(this.transitionToFake.callCount, 1);
    assert.strictEqual(this.transitionToFake.lastCall.args[0], "detail");
  });

  test("it redirects to index route on discard", async function (assert) {
    assert.expect(2);

    this._routing = getOwner(this).lookup("service:-routing");
    this._transitionTo = this._routing.transitionTo;
    this._transitionToFake = sinon.replace(
      this._routing,
      "transitionTo",
      sinon.fake(() => {})
    );

    this.instance = this.server.create("instance");

    await render(
      hbs`<Communication::NewTopic @instanceId={{this.instance.id}} />`
    );

    await click("[data-test-discard]");
    assert.strictEqual(this._transitionToFake.callCount, 1);
    assert.strictEqual(this._transitionToFake.lastCall.args[0], "index");
  });
});
