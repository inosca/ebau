import { render } from "@ember/test-helpers";
import loadQuestions from "citizen-portal/tests/helpers/load-questions";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupRenderingTest } from "ember-qunit";
import hbs from "htmlbars-inline-precompile";
import { module, test } from "qunit";

module("Integration | Component | camac-form", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(async function () {
    const instance = this.server.create("instance");

    this.set("id", instance.id);

    this.server.create("form-field", {
      name: "test-input",
      instance,
      value: "test",
    });

    this.server.create("form-field", {
      name: "test-table",
      instance,
      value: [{ "test-input-in-table": 1 }],
    });

    this.server.get("/api/v1/form-config", () => ({
      questions: {
        "test-input": {
          label: "Test input",
          required: true,
          type: "text",
          config: {},
        },
        "test-table": {
          label: "Test table",
          required: true,
          type: "table",
          config: {
            columns: [
              {
                name: "test-input-in-table",
                title: "Test input in a table",
                type: "number",
                required: true,
                config: {},
              },
            ],
          },
        },
      },
    }));

    await loadQuestions(["test-input", "test-table"], instance.id);
  });

  test("it renders", async function (assert) {
    assert.expect(4);

    await render(hbs`
      <CamacForm @instance={{hash id=id}} @meta={{hash editable=(array 'form' 'document')}} as |form|>
        <form.input @identifier='test-input'/>
        <form.table @identifier='test-table'/>
      </CamacForm>
    `);

    assert.dom("form").exists();
    assert.dom("input").exists();
    assert.dom("table").exists();
    assert.dom("tfoot").exists();
  });

  test("it renders in readonly mode", async function (assert) {
    assert.expect(4);

    await render(hbs`
      <CamacForm @instance={{hash id=id}} @meta={{hash editable=(array)}} as |form|>
        <form.input @identifier='test-input'/>
        <form.table @identifier='test-table'/>
      </CamacForm>
    `);

    assert.dom("form").exists();
    assert.dom("input").isDisabled();
    assert.dom("table").exists();
    assert.dom("tfoot").doesNotExist();
  });
});
