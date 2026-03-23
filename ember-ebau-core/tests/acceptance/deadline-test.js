import {
  click,
  fillIn,
  find,
  findAll,
  visit,
  waitFor,
  waitUntil,
} from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setFlatpickrDate } from "ember-flatpickr/test-support/helpers";
import { selectChoose } from "ember-power-select/test-support";
import { module, test } from "qunit";
import { stub } from "sinon";

import { setupApplicationTest } from "dummy/tests/helpers";
import DeadlinesDeadlineAbility from "ember-ebau-core/abilities/deadline";
import DeadlinesSuspensionAbility from "ember-ebau-core/abilities/suspension";
import { setupFeatures } from "ember-ebau-core/test-support";

module("Acceptance | deadline", function (hooks) {
  setupApplicationTest(hooks);
  setupFeatures(hooks);
  setupMirage(hooks);

  hooks.beforeEach(function () {
    const service = this.server.create("service");
    const publicService = this.server.create("public-service", {
      id: service.id,
    });

    this.instance = this.server.create("instance", {
      activeService: publicService,
    });
    this.group = this.server.create("group", { service });

    this.owner.lookup("service:ebau-modules").instanceId = this.instance.id;
    this.owner.lookup("service:ebau-modules").serviceId = service.id;

    this.deadlineTypes = this.server.createList("deadline-type", 3, {});
    this.suspensionReasons = this.server.createList("suspension-reason", 3, {});
    this.deadline = this.server.create("instance-deadline", {
      instance: this.instance,
      deadlineType: this.deadlineTypes[1],
    });
    this.server.createList("suspension", 10, {
      deadline: this.deadline,
    });
    stub(DeadlinesSuspensionAbility.prototype, "canRead").get(() => true);
    stub(DeadlinesSuspensionAbility.prototype, "canCreate").get(() => true);
    stub(DeadlinesSuspensionAbility.prototype, "canEdit").get(() => true);
    stub(DeadlinesDeadlineAbility.prototype, "canRead").get(() => true);
    stub(DeadlinesDeadlineAbility.prototype, "canEdit").get(() => true);
  });

  test("it can list deadline suspensions and deadline", async function (assert) {
    await visit(`/deadlines`);

    assert.dom("[data-test-deadlines-overview]").exists();
    assert.dom("[data-test-suspension-list-item]").exists({ count: 10 });
    assert.dom("[data-test-deadline-detail-grid]").exists({ count: 1 });
  });

  [true, false].forEach((withEndDate) => {
    test(`it can add a suspension ${
      withEndDate ? "with" : "without"
    } end date`, async function (assert) {
      this.features.enable("deadlines.manualSuspensionReason");
      await visit(`/deadlines`);
      assert.dom("[data-test-deadlines-overview]").exists();
      assert.dom("[data-test-suspension-list-item]").exists({ count: 10 });

      await click("[data-test-create-suspension-button]");

      const startDate = new Date();
      startDate.setDate(startDate.getDate() - 30);
      const endDate = new Date();

      setFlatpickrDate(
        "[data-test-suspension-start-date-input] input",
        startDate,
        true,
      );
      if (withEndDate) {
        setFlatpickrDate(
          "[data-test-suspension-end-date-input] input",
          endDate,
          true,
        );
      }
      await selectChoose(
        "[data-test-suspension-reason-input]",
        this.suspensionReasons[0].label,
      );
      fillIn("[data-test-suspension-remark-input]", "Test remark");
      await click("[data-test-suspension-submit]");

      // new suspension should be listed
      assert.dom("[data-test-suspension-list-item]").exists({ count: 11 });
    });
  });

  test("it can delete a suspension", async function (assert) {
    await visit(`/deadlines`);
    assert.dom("[data-test-deadlines-overview]").exists();
    assert.dom("[data-test-suspension-list-item]").exists({ count: 10 });
    await click(
      "[data-test-suspension-list-item]:first-child [data-test-edit-suspension-button]",
    );
    assert.dom("[data-test-modal-create-suspension]").exists();
    await click("[data-test-suspension-delete]");
    await waitFor(".uk-modal.uk-open");
    await click(".uk-modal-footer .uk-button-primary");
    await waitUntil(
      () => findAll("[data-test-suspension-list-item]").length === 9,
    );
    await waitUntil(() => !find(".uk-modal.uk-open"));
  });

  test("it can edit the deadline type", async function (assert) {
    await visit(`/deadlines`);
    assert.strictEqual(
      this.deadline.deadlineType.name,
      this.deadlineTypes[1].name,
    );
    assert.dom("[data-test-deadlines-overview]").exists();
    assert.dom("[data-test-deadline-detail-grid]").exists({ count: 1 });
    await click("[data-test-edit-deadline-button]");

    await waitFor(".uk-modal.uk-open");
    await selectChoose(
      "[data-test-deadline-type-input]",
      this.deadlineTypes[0].name.de,
    );
    await click(".uk-modal-footer .uk-button-primary");
    assert.strictEqual(
      this.deadline.deadlineType.name,
      this.deadlineTypes[0].name,
    );
  });
});
