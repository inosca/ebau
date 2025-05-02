import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module(
  "Integration | Component | rulesets/responsible-user-rule/list",
  function (hooks) {
    setupRenderingTest(hooks);
    setupMirage(hooks);

    test("it renders empty", async function (assert) {
      await render(hbs`<Rulesets::ResponsibleUserRule::List />`);

      assert.dom("ul").doesNotExist();
      assert
        .dom("[data-test-empty]")
        .hasText("Es wurden noch keine Zuständigkeitsregeln definiert");
    });

    test("it renders a list of rules", async function (assert) {
      this.server.createList(
        "responsible-user-rule",
        4,
        "withApplicationTypes",
      );
      this.server.createList("responsible-user-rule", 3, "withMunicipalities");

      await render(hbs`<Rulesets::ResponsibleUserRule::List />`);

      assert.dom("ul").exists();
      assert.dom("ul > li").exists({ count: 7 });
    });
  },
);
