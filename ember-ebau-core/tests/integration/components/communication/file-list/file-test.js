import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, todo } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module(
  "Integration | Component | communication/file-list/file",
  function (hooks) {
    setupRenderingTest(hooks);

    todo("it renders", async function () {
      await render(hbs`<Communication::FileList::File />`);
    });
  },
);
