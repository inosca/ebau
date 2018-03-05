import { module, test } from 'qunit'
import { setupTest } from 'ember-qunit'

module('Unit | Route | instances/new/index', function(hooks) {
  setupTest(hooks)

  test('it exists', function(assert) {
    let route = this.owner.lookup('route:instances/new/index')
    assert.ok(route)
  })
})
