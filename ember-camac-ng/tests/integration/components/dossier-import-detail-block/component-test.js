import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "camac-ng/tests/helpers";

module(
  "Integration | Component | dossier-import-detail-block",
  function (hooks) {
    setupRenderingTest(hooks);

    test("it renders", async function (assert) {
      // Set any properties with this.set('myProperty', 'value');
      // Handle any actions with this.set('myAction', function(val) { ... });

      await render(hbs`<DossierImportDetailBlock />`);

      assert.strictEqual(this.element.textContent.trim(), "");

      // Template block usage:
      await render(hbs`
      <DossierImportDetailBlock>
        template block text
      </DossierImportDetailBlock>
    `);

      assert.strictEqual(
        this.element.textContent.trim(),
        "template block text",
      );
    });
  },
);
