import { settled } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";
import { spy, restore } from "sinon";

import { setupTest } from "dummy/tests/helpers";

module("Unit | Model | applicant confirmation round", function (hooks) {
  setupTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(async function () {
    this.store = this.owner.lookup("service:store");
    this.mirageModel = this.server.create("applicant-confirmation-round");
    this.model = await this.store.findRecord(
      "applicant-confirmation-round",
      this.mirageModel.id,
    );

    this.pushPayloadSpy = spy(this.store, "pushPayload");
  });

  hooks.afterEach(function () {
    restore();
  });

  test("it can cancel", async function (assert) {
    this.server.post(
      "/api/v1/applicant-confirmation-rounds/:id/cancel",
      ({ applicantConfirmationRounds }, request) => {
        assert.strictEqual(request.params.id, this.model.id);
        assert.strictEqual(request.queryParams.include, "confirmations");
        assert.step("cancel-api-call");

        return applicantConfirmationRounds.find(request.params.id);
      },
    );

    await this.model.cancel();

    assert.verifySteps(["cancel-api-call"]);
    assert.strictEqual(this.pushPayloadSpy.callCount, 1);
  });

  test("it can invalidate", async function (assert) {
    this.server.post(
      "/api/v1/applicant-confirmation-rounds/:id/invalidate",
      ({ applicantConfirmationRounds }, request) => {
        assert.strictEqual(request.params.id, this.model.id);
        assert.strictEqual(request.queryParams.include, "confirmations");
        assert.step("invalidate-api-call");

        return applicantConfirmationRounds.find(request.params.id);
      },
    );

    await this.model.invalidate();

    assert.verifySteps(["invalidate-api-call"]);
    assert.strictEqual(this.pushPayloadSpy.callCount, 1);
  });

  test("it computes isActive", function (assert) {
    this.model.status = "running";
    assert.true(this.model.isActive);
    this.model.status = "completed";
    assert.true(this.model.isActive);
    this.model.status = "canceled";
    assert.false(this.model.isActive);
    this.model.status = "invalidated";
    assert.false(this.model.isActive);
  });

  test("it computes current user confirmation", async function (assert) {
    const user = this.server.create("user");
    this.owner.lookup("service:session").user = user;

    const confirmation = this.server.create("applicant-confirmation", {
      round: this.mirageModel,
      user,
    });

    // Refetch model to include the newly created confirmation
    const model = await this.store.findRecord(
      "applicant-confirmation-round",
      this.model.id,
      { include: "confirmations", reload: true },
    );

    assert.notOk(model.currentUserConfirmation);

    await settled();

    assert.ok(model.currentUserConfirmation);
    assert.strictEqual(model.currentUserConfirmation.id, confirmation.id);
  });
});
