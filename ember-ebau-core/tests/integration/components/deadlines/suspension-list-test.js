import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";
import { stub } from "sinon";

import { setupRenderingTest } from "dummy/tests/helpers";
import DeadlinesSuspensionAbility from "ember-ebau-core/abilities/suspension";

module("Integration | Component | deadlines/suspension/list", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(function () {
    this.owner.lookup("service:ebauModules").resolveModuleRoute = (
      _,
      routeName,
    ) => routeName;
    this.instance = this.server.create("instance");
    this.deadline = this.server.create("instance-deadline", {
      instance: this.instance,
    });
    this.owner.lookup("service:ebauModules").instanceId = this.instance.id;
  });

  test("it renders an empty list", async function (assert) {
    await render(
      hbs`<Deadlines::Suspension::List @deadline={{this.deadline}} />`,
    );
    assert.dom("[data-test-suspension-list]").exists();
    assert
      .dom("[data-test-suspension-list]")
      .containsText("Es sind keine Sistierungen vorhanden.");
  });

  [true, false].forEach((readonly) => {
    test(`it renders a non-empty list with readonly=${readonly}`, async function (assert) {
      stub(DeadlinesSuspensionAbility.prototype, "canRead").get(
        () => !readonly,
      );
      stub(DeadlinesSuspensionAbility.prototype, "canCreate").get(
        () => !readonly,
      );
      stub(DeadlinesSuspensionAbility.prototype, "canEdit").get(
        () => !readonly,
      );

      const deadline = this.server.create("instance-deadline");
      this.server.createList("suspension", 2, {
        deadline,
      });
      await render(
        hbs`<Deadlines::Suspension::List @deadline={{this.deadline}} />`,
      );
      assert.dom("[data-test-suspension-list]").exists();
      assert.dom("[data-test-suspension-list-item]").exists({ count: 2 });

      assert
        .dom("[data-test-edit-suspension-button]")
        .exists({ count: readonly ? 0 : 2 });
      assert
        .dom("[data-test-create-suspension-button]")
        .exists({ count: readonly ? 0 : 1 });
    });
  });
});
