import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

<<<<<<< HEAD:ember-camac-ng/tests/unit/ui/application/route-test.js
module("Unit | Route | application", function(hooks) {
  setupTest(hooks);

  test("it exists", function(assert) {
    const route = this.owner.lookup("route:application");
=======
module("Unit | Route | work-item-list-all", function(hooks) {
  setupTest(hooks);

  test("it exists", function(assert) {
    const route = this.owner.lookup("route:work-item-list-all");
>>>>>>> feat: rename module workitemlist to workitem:ember-camac-ng/tests/unit/ui/work-item-list-all/route-test.js
    assert.ok(route);
  });
});
