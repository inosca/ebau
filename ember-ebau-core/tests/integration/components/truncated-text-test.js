import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | truncated-text", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    const content = `
    Lorem Ipsum is simply dummy text of the printing and typesetting industry.
    Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
    when an unknown printer took a galley of type and scrambled it to make a type
    specimen book.
    `;

    this.set("content", content);
    await render(hbs`<TruncatedText @content={{this.content}} />`);
    assert
      .dom("[data-test-content]")
      .hasText(`${content.trim().slice(0, 117)}... (mehr)`);
  });
});
