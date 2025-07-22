import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | markdown-to-html", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders safe html", async function (assert) {
    this.set(
      "value",
      `# Title
<script type="text/javascript">alert("XSS");</script>
text`,
    );

    await render(
      hbs`<MarkdownToHtml @markdown={{this.value}} @extensions="DOMPurify" />`,
    );

    assert.dom("h1").exists();
    assert.dom("script").doesNotExist();
  });
});
