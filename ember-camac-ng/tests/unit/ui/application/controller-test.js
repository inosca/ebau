import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

<<<<<<< HEAD:ember-camac-ng/tests/unit/ui/application/controller-test.js
module("Unit | Controller | application", function(hooks) {
=======
module("Unit | Controller | work-item-list-all", function(hooks) {
>>>>>>> feat: rename module workitemlist to workitem:ember-camac-ng/tests/unit/ui/work-item-list-all/controller-test.js
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function(assert) {
<<<<<<< HEAD:ember-camac-ng/tests/unit/ui/application/controller-test.js
    const controller = this.owner.lookup("controller:application");
=======
    const controller = this.owner.lookup("controller:work-item-list-all");
>>>>>>> feat: rename module workitemlist to workitem:ember-camac-ng/tests/unit/ui/work-item-list-all/controller-test.js
    assert.ok(controller);
  });
});
