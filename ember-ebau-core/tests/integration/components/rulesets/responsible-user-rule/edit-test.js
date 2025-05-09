import { click, render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { t } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module(
  "Integration | Component | rulesets/responsible-user-rule/edit",
  function (hooks) {
    setupRenderingTest(hooks);
    setupMirage(hooks);

    hooks.beforeEach(function () {
      this.store = this.owner.lookup("service:store");
    });

    test("it renders with a new model", async function (assert) {
      this.model = this.store.createRecord("responsible-user-rule");

      await render(
        hbs`<Rulesets::ResponsibleUserRule::Edit @model={{this.model}} />`,
      );

      assert.dom("h3").hasText(t("rulesets.responsible-user.new"));

      await click("[data-test-rule-type=municipalities]");
      assert.dom("#municipalities.ember-power-select-trigger").exists();
      assert.dom("#applicationTypes.ember-power-select-trigger").doesNotExist();
      await click("[data-test-rule-type=application-types]");
      assert.dom("#municipalities.ember-power-select-trigger").doesNotExist();
      assert.dom("#applicationTypes.ember-power-select-trigger").exists();

      assert.dom("#responsibleUser.ember-power-select-trigger").exists();
    });

    test("it renders with an existing model", async function (assert) {
      const model = this.server.create(
        "responsible-user-rule",
        "withMunicipalities",
      );
      this.model = this.store.findRecord("responsible-user-rule", model.id);

      await render(
        hbs`<Rulesets::ResponsibleUserRule::Edit @model={{this.model}} />`,
      );

      assert.dom("h3").hasText(t("rulesets.responsible-user.edit"));

      assert.dom("[data-test-rule-type=municipalities]").doesNotExist();
      assert.dom("[data-test-rule-type=application-types]").doesNotExist();
      assert.dom("#municipalities.ember-power-select-trigger").exists();
      assert.dom("#responsibleUser.ember-power-select-trigger").exists();
    });
  },
);
