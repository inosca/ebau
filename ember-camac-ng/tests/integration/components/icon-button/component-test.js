import { render, click } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | icon-button", function (hooks) {
  setupRenderingTest(hooks);

  hooks.beforeEach(function (assert) {
    this.noop = () => assert.step("noop");
  });

  test("it renders", async function (assert) {
    await render(hbs`<IconButton @icon="plus" @onClick={{this.noop}} />`);

    assert.dom("button.uk-icon-button span[icon=plus]").exists();
  });

  test("it renders a loading state", async function (assert) {
    await render(hbs`
      <IconButton
        @icon="plus"
        @loading={{true}}
        @onClick={{this.noop}}
        title="foo"
      />
    `);

    assert.dom("button.uk-icon-button div[uk-spinner]").exists();
    assert.dom("button.uk-icon-button").hasAttribute("title", "foo");
  });

  test("it renders a disabled state", async function (assert) {
    await render(hbs`
      <IconButton
        @icon="plus"
        @disabled={{true}}
        @onClick={{this.noop}}
      />
    `);

    assert.dom("button.uk-icon-button.uk-disabled").exists();
    assert.dom("button.uk-icon-button").hasAttribute("disabled");
  });

  test("it trigers the onClick action on click", async function (assert) {
    await render(hbs`
      <IconButton
        @icon="plus"
        @onClick={{this.noop}}
      />
    `);

    await click("button");

    assert.verifySteps(["noop"]);
  });
});
