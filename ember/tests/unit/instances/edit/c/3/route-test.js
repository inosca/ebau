import { module, test } from 'qunit'
import { setupTest } from 'ember-qunit'

module('Unit | Route | instances/edit/c/3', function(hooks) {
  setupTest(hooks)

  test('it exists', function(assert) {
    let route = this.owner.lookup('route:instances/edit/c/3')
    assert.ok(route)
  })
})
