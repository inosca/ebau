import EmberObject from "@ember/object";
import CamacMultipleQuestionRowMixin from "citizen-portal/mixins/camac-multiple-question-row";
import { module, test } from "qunit";

module("Unit | Mixin | camac-multiple-question-row", function() {
  // Replace this with your real tests.
  test("it works", function(assert) {
    let CamacMultipleQuestionRowObject = EmberObject.extend(
      CamacMultipleQuestionRowMixin
    );
    let subject = CamacMultipleQuestionRowObject.create();
    assert.ok(subject);
  });
});
