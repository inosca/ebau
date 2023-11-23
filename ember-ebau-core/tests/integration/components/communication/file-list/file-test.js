import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, skip } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module(
  "Integration | Component | communication/file-list/file",
  function (hooks) {
    setupRenderingTest(hooks);

    skip("it renders", async function () {
      await render(hbs`<Communication::FileList::File />`);
    });
  },
);
