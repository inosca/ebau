import { module, test } from "qunit";
import { setupRenderingTest } from "ember-qunit";
import { render } from "@ember/test-helpers";
import hbs from "htmlbars-inline-precompile";
import setupMirage from "ember-cli-mirage/test-support/setup-mirage";
import loadQuestions from "citizen-portal/tests/helpers/load-questions";

module("Integration | Component | camac-input", function(hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(async function() {
    let instance = this.server.create("instance");

    this.set("instance", instance);

    this.server.create("form-field", {
      name: "test-input",
      instance
    });

    this.server.get("/api/v1/form-config", () => {
      return {
        questions: {
          "test-input": {
            label: "Test Input",
            hint: "Hint hint hint",
            type: "text",
            required: true,
            config: {}
          }
        }
      };
    });

    await loadQuestions(["test-input"], instance.id);
  });

  test("it renders", async function(assert) {
    await render(hbs`{{camac-input 'test-input' instance=instance}}`);

    assert.dom("input").exists();
  });
});
