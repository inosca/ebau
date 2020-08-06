import { module, test } from 'qunit';
import { setupTest } from 'ember-qunit';

module('Unit | Route | work-item-list-instance', function(hooks) {
  setupTest(hooks);

  test('it exists', function(assert) {
    let route = this.owner.lookup('route:work-item-list-instance');
    assert.ok(route);
  });
});
