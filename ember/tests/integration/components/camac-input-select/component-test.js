import { module, test } from 'qunit'
import { setupRenderingTest } from 'ember-qunit'
import { render, click } from '@ember/test-helpers'
import hbs from 'htmlbars-inline-precompile'
import EmberObject from '@ember/object'

module('Integration | Component | camac-input-select', function(hooks) {
  setupRenderingTest(hooks)

  test('it renders a select', async function(assert) {
    assert.expect(2)

    this.set(
      'model',
      EmberObject.create({
        value: 'option 1'
      })
    )

    this.set('config', {
      options: ['option 1', 'option 2', 'option 3']
    })

    await render(hbs`{{camac-input-select config=config model=model}}`)

    await click('.ember-power-select-trigger')

    assert.dom('.ember-power-select-option').exists({ count: 3 })
    assert.dom('.ember-power-select-selected-item').hasText('option 1')
  })

  test('it renders in readonly mode', async function(assert) {
    assert.expect(1)

    this.set(
      'model',
      EmberObject.create({
        value: 'option 1'
      })
    )

    this.set('config', {
      options: ['option 1', 'option 2', 'option 3']
    })

    await render(
      hbs`{{camac-input-select config=config model=model readonly=true}}`
    )

    assert.dom('.ember-power-select-trigger[aria-disabled="true"]').exists()
  })
})
