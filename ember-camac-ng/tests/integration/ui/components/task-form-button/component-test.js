import { render, click } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import setupMirage from "ember-cli-mirage/test-support/setup-mirage";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | task-form-button", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  test("it renders", async function (assert) {
    const controller = this.owner.lookup("controller:task-form");

    controller.fetchWorkItem = {
      perform() {
        assert.step("refresh");
      },
    };

    this.workItem = this.server.create("work-item");

    this.field = {
      document: {
        fields: [
          {
            isValid: true,
            validate: { perform: () => true },
          },
        ],
      },
      question: {
        label: "Do it!",
        staticContent: "Sure?",
        meta: {
          mutation: "complete",
        },
      },
    };

    await render(hbs`
      <TaskFormButton
        @context={{hash workItemId=this.workItem.id instanceId=1}}
        @field={{this.field}}
      />
    `);

    assert.dom("button").exists();
    assert.dom("button").hasText(this.field.question.label);

    await click("button");

    assert.dom(".uk-modal-body").hasText(this.field.question.staticContent);

    await click(".uk-modal-footer button.uk-button-primary");

    assert.verifySteps(["refresh"]);
  });

  test("it does not render when disabled", async function (assert) {
    assert.expect(1);

    await render(hbs`<TaskFormButton @disabled={{true}} />`);

    assert.dom("button").doesNotExist();
  });
});
