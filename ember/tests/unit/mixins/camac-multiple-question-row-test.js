import EmberObject from "@ember/object";
import CamacMultipleQuestionRowMixin from "citizen-portal/mixins/camac-multiple-question-row";
import { module, test } from "qunit";

module("Unit | Mixin | camac-multiple-question-row", function() {
  // Replace this with your real tests.
  test("it works", function(assert) {
    const CamacMultipleQuestionRowObject = EmberObject.extend(
      CamacMultipleQuestionRowMixin
    );
    const subject = CamacMultipleQuestionRowObject.create();
    assert.ok(subject);
  });
});
