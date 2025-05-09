import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module(
  "Integration | Component | rulesets/responsible-user-rule/list/item",
  function (hooks) {
    setupRenderingTest(hooks);
    setupMirage(hooks);

    test("it renders a sortable handle and action buttons", async function (assert) {
      const store = this.owner.lookup("service:store");
      const rule = this.server.create("responsible-user-rule");

      this.rule = await store.findRecord("responsible-user-rule", rule.id, {
        include: "responsible_user,municipalities,application_types",
      });

      await render(
        hbs`<Rulesets::ResponsibleUserRule::List::Item @rule={{this.rule}} />`,
      );

      assert.dom("li").exists({ count: 1 });
      assert
        .dom("li > div > span.uk-sortable-handle")
        .hasAttribute("icon", "menu");
      assert
        .dom("li > div > div:nth-of-type(4) > a[data-test-edit-rule]")
        .exists();
      assert
        .dom("li > div > div:nth-of-type(4) > button[data-test-delete-rule]")
        .exists();
    });

    test("it renders with application types", async function (assert) {
      const store = this.owner.lookup("service:store");
      const rule = this.server.create(
        "responsible-user-rule",
        "withApplicationTypes",
      );

      this.rule = await store.findRecord("responsible-user-rule", rule.id, {
        include: "responsible_user,municipalities,application_types",
      });

      await render(
        hbs`<Rulesets::ResponsibleUserRule::List::Item @rule={{this.rule}} />`,
      );

      assert.dom("li").exists({ count: 1 });
      assert.dom("li > div > div").exists({ count: 4 });
      assert
        .dom("li > div > div:nth-of-type(1)")
        .hasText(
          (await this.rule.applicationTypes).map((t) => t.name).join(", "),
        );
      assert
        .dom("li > div > div:nth-of-type(3)")
        .hasText((await this.rule.responsibleUser).fullName);
    });

    test("it renders with municipalities", async function (assert) {
      const store = this.owner.lookup("service:store");
      const rule = this.server.create(
        "responsible-user-rule",
        "withMunicipalities",
      );

      this.rule = await store.findRecord("responsible-user-rule", rule.id, {
        include: "responsible_user,municipalities,application_types",
      });

      await render(
        hbs`<Rulesets::ResponsibleUserRule::List::Item @rule={{this.rule}} />`,
      );

      assert.dom("li").exists({ count: 1 });
      assert.dom("li > div > div").exists({ count: 4 });
      assert
        .dom("li > div > div:nth-of-type(1)")
        .hasText(
          (await this.rule.municipalities).map((t) => t.name).join(", "),
        );
      assert
        .dom("li > div > div:nth-of-type(3)")
        .hasText((await this.rule.responsibleUser).fullName);
    });
  },
);
