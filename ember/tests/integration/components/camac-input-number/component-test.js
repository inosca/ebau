import { module, test } from 'qunit'
import { setupRenderingTest } from 'ember-qunit'
import { render, fillIn } from '@ember/test-helpers'
import hbs from 'htmlbars-inline-precompile'
import EmberObject from '@ember/object'

module('Integration | Component | camac-input-number', function(hooks) {
  setupRenderingTest(hooks)

  test('it renders a number input', async function(assert) {
    assert.expect(4)

    this.set(
      'model',
      EmberObject.create({
        value: 2
      })
    )

    this.set('config', {
      min: 0,
      max: 5,
      step: 1
    })

    await render(hbs`{{camac-input-number config=config model=model}}`)

    assert.dom('input[type=number]').exists()

    assert.dom('input[type=number]').hasAttribute('min', '0')
    assert.dom('input[type=number]').hasAttribute('max', '5')
    assert.dom('input[type=number]').hasAttribute('step', '1')
  })

  test('it renders in readonly mode', async function(assert) {
    assert.expect(1)

    this.set(
      'model',
      EmberObject.create({
        value: 2
      })
    )

    this.set('config', {})

    await render(
      hbs`{{camac-input-number config=config model=model readonly=true}}`
    )

    assert.dom('input[type=number]').isDisabled()
  })

  test('it can change the value', async function(assert) {
    assert.expect(1)

    this.set(
      'model',
      EmberObject.create({
        value: 2
      })
    )

    this.set('config', {})

    await render(
      hbs`{{camac-input-number config=config model=model on-change=(action (mut model.value))}}`
    )

    await fillIn('input[type=number]', 5)

    assert.equal(this.get('model.value'), 5)
  })
})
