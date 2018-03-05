import { module, test } from 'qunit'
import { setupTest } from 'ember-qunit'

module('Unit | Route | instances/edit/b/4', function(hooks) {
  setupTest(hooks)

  test('it exists', function(assert) {
    let route = this.owner.lookup('route:instances/edit/b/4')
    assert.ok(route)
  })
})
