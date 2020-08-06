import { module, test } from 'qunit';
import { setupTest } from 'ember-qunit';

module('Unit | Controller | work-item-list-instance', function(hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test('it exists', function(assert) {
    let controller = this.owner.lookup('controller:work-item-list-instance');
    assert.ok(controller);
  });
});
