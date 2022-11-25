import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | communication/topic-list", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<Communication::TopicList />`);

    assert.dom(this.element).hasText("");

    // Template block usage:
    await render(hbs`
      <Communication::TopicList>
        template block text
      </Communication::TopicList>
    `);

    assert.dom(this.element).hasText("template block text");
  });
});
