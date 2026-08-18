import { render, click, waitFor } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";
import { setupConfig, setupPermissions } from "ember-ebau-core/test-support";

module("Integration | Component | corrections/copy-instance", function (hooks) {
  setupRenderingTest(hooks);
  setupConfig(hooks, "be");
  setupPermissions(hooks);

  hooks.beforeEach(function () {
    this.instanceStates = {
      new: this.server.create("instance-state"),
      subm: this.server.create("instance-state"),
      finished: this.server.create("instance-state"),
      archived: this.server.create("instance-state"),
      evaluated: this.server.create("instance-state"),
      finishedInternal: this.server.create("instance-state"),
    };

    this.config.set(
      "instanceStates",
      Object.entries(this.instanceStates).reduce((obj, [key, state]) => {
        return { ...obj, [key]: parseInt(state.id) };
      }, {}),
    );

    this.initialize = async (state, role = "support") => {
      const instance = this.server.create("instance", {
        instanceState:
          this.instanceStates[state] ?? this.server.create("instance-state"),
      });

      this.instance = await this.owner
        .lookup("service:store")
        .findRecord("instance", instance.id);

      const ebauModules = this.owner.lookup("service:ebau-modules");
      ebauModules.baseRole = role;
      ebauModules.instanceId = parseInt(instance.id);
      Object.defineProperty(ebauModules, "isSupportRole", {
        get: () => role === "support",
        configurable: true,
      });
    };
  });

  test.each(
    "it renders",
    [
      // state, role, hasButton
      [null, "support", true],
      ["new", "support", true],
      ["archived", "support", true],
      ["finished", "support", true],
      ["subm", "municipality", false],
      ["finished", "municipality", false],
    ],
    async function (assert, [state, role, hasButton]) {
      await this.initialize(state, role);

      await render(
        hbs`<Corrections::CopyInstance @instance={{this.instance}} />`,
      );

      if (hasButton) {
        assert.dom("button").exists();
      } else {
        assert.dom("button").doesNotExist();
      }
    },
  );

  test("it disables the button without instance-copy permission", async function (assert) {
    await this.initialize("new", "support");

    await render(
      hbs`<Corrections::CopyInstance @instance={{this.instance}} />`,
    );

    assert.dom("button").isDisabled();
  });

  test("it enables the button with instance-copy permission", async function (assert) {
    await this.initialize("archived", "support");
    this.owner.lookup("service:permissions").fullyEnabled = true;
    this.permissions.grant(parseInt(this.instance.id), ["instance-copy"]);

    await render(
      hbs`<Corrections::CopyInstance @instance={{this.instance}} />`,
    );

    assert.dom("button").isNotDisabled();
  });

  test("it redirects after successful copy", async function (assert) {
    await this.initialize("finished");
    this.owner.lookup("service:permissions").fullyEnabled = true;
    this.permissions.grant(parseInt(this.instance.id), ["instance-copy"]);

    this.server.post(
      `/api/v1/instances/${this.instance.id}/copy`,
      () => {
        assert.step("request");
        return { data: { id: 99 } };
      },
      201,
    );

    this.owner.lookup("service:ebau-modules").redirectToInstance = (
      instanceId,
    ) => {
      assert.strictEqual(instanceId, 99);
      assert.step("redirect");
    };

    await render(
      hbs`<Corrections::CopyInstance @instance={{this.instance}} />`,
    );

    await click("button");

    // Confirm dialog
    await waitFor(".uk-modal.uk-open");
    await click(".uk-modal-footer .uk-button-primary");

    await waitFor("button:not([disabled])");

    assert.verifySteps(["request", "redirect"]);
  });
});
