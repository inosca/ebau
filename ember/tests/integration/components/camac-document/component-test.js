import { render, triggerEvent, click } from "@ember/test-helpers";
import loadQuestions from "citizen-portal/tests/helpers/load-questions";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupRenderingTest } from "ember-qunit";
import hbs from "htmlbars-inline-precompile";
import { module, test } from "qunit";

module("Integration | Component | camac-document", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(async function () {
    const instance = this.server.create("instance", "unsubmitted", {
      instanceState: this.server.create("instance-state", {
        name: "new",
      }),
    });

    this.set("instance", instance);

    this.server.createList("attachment", 2, {
      name: "foo",
      question: "test-document",
      instance,
    });

    this.server.create("attachment", {
      name: "bar",
      question: "test-document",
      instance,
    });

    this.server.get("/api/v1/form-config", () => {
      return {
        questions: {
          "test-document": {
            label: "Test Doc",
            hint: "Hint hint hint",
            type: "document",
            required: true,
            config: {},
          },
        },
      };
    });

    await loadQuestions(["test-document"], instance.id);
  });

  test("it renders", async function (assert) {
    assert.expect(1);

    await render(hbs`{{camac-document 'test-document' instance=instance}}`);

    assert.dom(".uk-card-header").hasText("Test Doc *");
  });

  test("it can upload a document", async function (assert) {
    assert.expect(2);

    this.server.post("/api/v1/attachments", ({ attachments }) => {
      assert.step("upload-document");

      return attachments.first();
    });

    await render(hbs`{{camac-document 'test-document'instance=instance}}`);

    const files = {
      files: [new File([new Blob()], "testfile.png", { type: "image/png" })],
    };

    await triggerEvent(
      "[data-test-upload-document] + input[type=file]",
      "change",
      files
    );

    assert.verifySteps(["upload-document"]);
  });

  test("it can replace a document", async function (assert) {
    assert.expect(3);

    this.server.patch(
      "/api/v1/attachments/:id",
      ({ attachments }, { requestBody }) => {
        assert.step("upload-document");

        assert.equal(requestBody.get("path").name, "bar");

        return attachments.first();
      }
    );

    await render(hbs`{{camac-document 'test-document' instance=instance}}`);

    const files = {
      files: [new File([new Blob()], "testfile.png", { type: "image/png" })],
    };

    await triggerEvent(
      "[data-test-replace-document] + input[type=file]",
      "change",
      files
    );

    assert.verifySteps(["upload-document"]);
  });

  test("it can download a document", async function (assert) {
    assert.expect(2);

    this.server.get("/api/v1/attachments/:id/files/:name", () => {
      assert.step("download-document");

      return new Blob();
    });

    await render(hbs`{{camac-document 'test-document'instance=instance}}`);

    await click("[data-test-download-document]");

    assert.verifySteps(["download-document"]);
  });

  test("it can delete a document", async function (assert) {
    assert.expect(2);

    this.server.delete(
      "/api/v1/attachments/:id",
      () => {
        assert.step("delete-document");

        return "";
      },
      204
    );

    await render(hbs`{{camac-document 'test-document' instance=instance}}`);

    await click("[data-test-delete-document]");
    await click("[data-test-delete-document-confirm]");

    assert.verifySteps(["delete-document"]);
  });

  // If instance has never been submitted delete button is displayed
  test("delete document button is not visible", async function (assert) {
    const instanceState = this.server.create("instance-state", { name: "new" });

    const n = String(this.instance.location.communalFederalNumber).substr(2, 4);
    const y = String(new Date().getFullYear()).substr(2, 4);
    const i = String(this.instance.id).padStart(3, 0);

    // Set instance to submitted
    this.set("instance.identifier", `${n}-${y}-${i}`);
    this.set("instance.instanceState", instanceState);

    await loadQuestions(["test-document"], this.instance.id);

    await render(hbs`{{camac-document 'test-document' instance=instance}}`);

    assert.notOk(await find("[data-test-delete-document]"));
  });
});
