import { module, test } from 'qunit'
import { setupRenderingTest } from 'ember-qunit'
import { render, click } from '@ember/test-helpers'
import hbs from 'htmlbars-inline-precompile'
import EmberObject from '@ember/object'

module('Integration | Component | camac-input-checkbox', function(hooks) {
  setupRenderingTest(hooks)

  test('it renders checkboxes', async function(assert) {
    assert.expect(2)

    this.set(
      'model',
      EmberObject.create({
        value: ['option 1', 'option 2']
      })
    )

    this.set('config', {
      options: ['option 1', 'option 2', 'option 3']
    })

    await render(hbs`{{camac-input-checkbox config=config model=model}}`)

    assert.dom('input[type=checkbox]').exists({ count: 3 })
    assert.dom('input[type=checkbox]:checked').exists({ count: 2 })
  })

  test('it can be rendered in readonly mode', async function(assert) {
    assert.expect(2)

    this.set(
      'model',
      EmberObject.create({
        value: ['option 1', 'option 2']
      })
    )

    this.set('config', {
      options: ['option 1', 'option 2', 'option 3']
    })

    await render(hbs`{{camac-input-checkbox readonly=true config=config}}`)

    assert.dom('input[type=checkbox]').exists({ count: 3 })
    assert.dom('input[type=checkbox]').isDisabled()
  })

  test('it can change the value', async function(assert) {
    assert.expect(3)

    this.set(
      'model',
      EmberObject.create({
        value: ['option 1']
      })
    )

    this.set('config', {
      options: ['option 1', 'option 2', 'option 3']
    })

    await render(
      hbs`{{camac-input-checkbox config=config model=model on-change=(action (mut model.value))}}`
    )

    assert.equal(this.get('model.value.length'), 1)

    await click('input[type=checkbox][value="option 3"]')

    assert.equal(this.get('model.value.length'), 2)

    await click('input[type=checkbox][value="option 3"]')

    assert.equal(this.get('model.value.length'), 1)
  })
})
