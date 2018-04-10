import { module, test } from 'qunit'
import { setupTest } from 'ember-qunit'

module(
  'Unit | Controller | instances/edit/grundinformationen/lokalisierung',
  function(hooks) {
    setupTest(hooks)

    // Replace this with your real tests.
    test('it exists', function(assert) {
      let controller = this.owner.lookup(
        'controller:instances/edit/grundinformationen/lokalisierung'
      )
      assert.ok(controller)
    })
  }
)
