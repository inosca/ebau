import EmberObject from '@ember/object'
import CamacInputComponentMixin from 'citizen-portal/mixins/camac-input-component'
import { module, test } from 'qunit'

module('Unit | Mixin | camac-input-component', function() {
  // Replace this with your real tests.
  test('it works', function(assert) {
    let CamacInputComponentObject = EmberObject.extend(CamacInputComponentMixin)
    let subject = CamacInputComponentObject.create()
    assert.ok(subject)
  })
})
