import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";
import { spy, restore } from "sinon";

import { setupTest } from "dummy/tests/helpers";

module("Unit | Model | applicant confirmation", function (hooks) {
  setupTest(hooks);
  setupMirage(hooks);

  test("it can confirm", async function (assert) {
    const store = this.owner.lookup("service:store");
    const mirageModel = this.server.create("applicant-confirmation");
    const model = await store.findRecord(
      "applicant-confirmation",
      mirageModel.id,
    );

    const pushPayloadSpy = spy(store, "pushPayload");

    this.server.post(
      "/api/v1/applicant-confirmations/:id/confirm",
      ({ applicantConfirmations }, request) => {
        assert.strictEqual(request.params.id, model.id);
        assert.strictEqual(request.queryParams.include, "round");
        assert.step("confirm-api-call");

        return applicantConfirmations.find(request.params.id);
      },
    );

    await model.confirm();

    assert.verifySteps(["confirm-api-call"]);
    assert.strictEqual(pushPayloadSpy.callCount, 1);

    restore();
  });
});
