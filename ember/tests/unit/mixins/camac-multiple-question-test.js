import EmberObject from "@ember/object";
import CamacMultipleQuestionMixin from "citizen-portal/mixins/camac-multiple-question";
import { module, test } from "qunit";

module("Unit | Mixin | camac-multiple-question", function () {
  // Replace this with your real tests.
  test("it works", function (assert) {
    const CamacMultipleQuestionObject = EmberObject.extend(
      CamacMultipleQuestionMixin
    );
    const subject = CamacMultipleQuestionObject.create();
    assert.ok(subject);
  });
});
