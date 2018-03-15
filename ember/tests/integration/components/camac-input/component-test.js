import { module, test } from 'qunit'
import { setupRenderingTest } from 'ember-qunit'
import { render } from '@ember/test-helpers'
import hbs from 'htmlbars-inline-precompile'
import setupMirage from 'ember-cli-mirage/test-support/setup-mirage'

module('Integration | Component | camac-input', function(hooks) {
  setupRenderingTest(hooks)
  setupMirage(hooks)

  test('it renders', async function(assert) {
    // TODO: add real tests

    await render(hbs`{{camac-input 'test'}}`)

    assert.equal(this.element.textContent.trim(), '')
  })
})
