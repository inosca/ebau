import { module, test } from 'qunit'
import { setupRenderingTest } from 'ember-qunit'
import { render } from '@ember/test-helpers'
import hbs from 'htmlbars-inline-precompile'

module('Integration | Component | camac-input-select', function(hooks) {
  setupRenderingTest(hooks)

  test('it renders', async function(assert) {
    // TODO: add real tests

    await render(hbs`{{camac-input-select}}`)

    assert.equal(this.element.textContent.trim(), '')
  })
})
