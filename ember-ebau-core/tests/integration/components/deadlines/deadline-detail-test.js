import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";
import { stub } from "sinon";

import { setupRenderingTest } from "dummy/tests/helpers";
import DeadlinesDeadlineAbility from "ember-ebau-core/abilities/deadline";

module("Integration | Component | deadlines/deadline/detail", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(function () {
    this.owner.lookup("service:ebauModules").resolveModuleRoute = (
      _,
      routeName,
    ) => routeName;
    this.instance = this.server.create("instance");
    this.owner.lookup("service:ebauModules").instanceId = this.instance.id;
  });

  test("it renders an empty result", async function (assert) {
    await render(
      hbs`<Deadlines::Deadline::Detail @instance={{this.instance}} />`,
    );
    assert.dom("[data-test-deadline-detail]").exists();
    assert.dom("[data-test-deadline-detail-grid]").doesNotExist();
  });

  [true, false].forEach((readonly) => {
    test(`it renders a non-empty result with readonly=${readonly}`, async function (assert) {
      stub(DeadlinesDeadlineAbility.prototype, "canRead").get(() => !readonly);
      stub(DeadlinesDeadlineAbility.prototype, "canEdit").get(() => !readonly);
      this.deadlineTypes = this.server.createList("deadline-type", 3);
      this.deadline = this.server.create("instance-deadline", {
        instance: this.instance,
        deadlineType: this.deadlineTypes[1],
      });
      await render(
        hbs`<Deadlines::Deadline::Detail
  @instance={{this.instance}}
  @deadline={{this.deadline}}
/>`,
      );
      assert.dom("[data-test-deadline-detail]").exists();
      assert.dom("[data-test-deadline-detail-grid]").exists({ count: 1 });
      assert.dom("[data-test-deadline-type]").exists({ count: 1 });
      assert
        .dom("[data-test-deadline-type]")
        .containsText(this.deadlineTypes[1].name);

      assert.dom("[data-test-edit-deadline-button]").exists({
        count: readonly ? 0 : 1,
      });
    });
  });
});
