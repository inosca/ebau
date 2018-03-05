import { module, test } from 'qunit'
import { setupRenderingTest } from 'ember-qunit'
import { render } from '@ember/test-helpers'
import hbs from 'htmlbars-inline-precompile'

module('Integration | Component | camac-input', function(hooks) {
  setupRenderingTest(hooks)

  test('it renders', async function(assert) {
    // TODO: add real tests

    await render(hbs`{{camac-input}}`)

    assert.equal(this.element.textContent.trim(), '')
  })
})
