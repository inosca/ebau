import { module, test } from 'qunit'
import { setupRenderingTest } from 'ember-qunit'
import { render, click, fillIn, triggerKeyEvent } from '@ember/test-helpers'
import hbs from 'htmlbars-inline-precompile'
import EmberObject from '@ember/object'

module('Integration | Component | camac-input-multiselect', function(hooks) {
  setupRenderingTest(hooks)

  test('it renders a multiselect', async function(assert) {
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

    await render(hbs`{{camac-input-multiselect config=config model=model}}`)

    await click('.ember-power-select-trigger')

    assert.dom('.ember-power-select-option').exists({ count: 3 })
    assert.dom('.ember-power-select-multiple-option').exists({ count: 2 })
  })

  test('it renders in readonly mode', async function(assert) {
    assert.expect(1)

    this.set(
      'model',
      EmberObject.create({
        value: ['option 1', 'option 2']
      })
    )

    this.set('config', {
      options: ['option 1', 'option 2', 'option 3']
    })

    await render(
      hbs`{{camac-input-multiselect config=config model=model readonly=true}}`
    )

    assert.dom('.ember-power-select-trigger-multiple-input:disabled').exists()
  })

  test('it can change the value', async function(assert) {
    assert.expect(4)

    this.set(
      'model',
      EmberObject.create({
        value: ['option 1', 'option 2']
      })
    )

    this.set('config', {
      options: ['option 1', 'option 2', 'option 3'],
      allowCustom: true
    })

    await render(
      hbs`{{camac-input-multiselect config=config model=model on-change=(action (mut model.value))}}`
    )

    await click('.ember-power-select-trigger')
    await click('.ember-power-select-option[data-option-index="2"]')

    assert.equal(this.get('model.value').length, 3)

    await click('.ember-power-select-trigger')
    await click('.ember-power-select-option[data-option-index="2"]')

    assert.equal(this.get('model.value').length, 2)

    await click('.ember-power-select-trigger')
    await fillIn('.ember-power-select-trigger-multiple-input', 'test')
    await triggerKeyEvent(
      '.ember-power-select-trigger-multiple-input',
      'keydown',
      13
    )

    assert.equal(this.get('model.value').length, 3)
    assert.ok(this.get('model.value').includes('test'))
  })
})
