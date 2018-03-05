import { module, test } from 'qunit'
import { setupTest } from 'ember-qunit'

module('transform:value', 'Unit | Transform | value', function(hooks) {
  setupTest(hooks)

  test('it deserializes', function(assert) {
    let transform = this.owner.lookup('transform:value')

    assert.deepEqual(transform.deserialize({ value: 123 }), 123)
  })

  test('it serializes', function(assert) {
    let transform = this.owner.lookup('transform:value')

    assert.deepEqual(transform.serialize(123), { value: 123 })
  })
})
