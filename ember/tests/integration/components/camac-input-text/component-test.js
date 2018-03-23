import { module, test } from 'qunit'
import { setupRenderingTest } from 'ember-qunit'
import { render, fillIn } from '@ember/test-helpers'
import hbs from 'htmlbars-inline-precompile'
import EmberObject from '@ember/object'

module('Integration | Component | camac-input-text', function(hooks) {
  setupRenderingTest(hooks)

  test('it renders a text input', async function(assert) {
    assert.expect(3)

    this.set(
      'model',
      EmberObject.create({
        value: 'foo'
      })
    )

    this.set('config', {
      minlength: 0,
      maxlength: 20
    })

    await render(hbs`{{camac-input-text config=config model=model}}`)

    assert.dom('input[type=text]').exists()

    assert.dom('input[type=text]').hasAttribute('minlength', '0')
    assert.dom('input[type=text]').hasAttribute('maxlength', '20')
  })

  test('it renders in readonly mode', async function(assert) {
    assert.expect(1)

    this.set(
      'model',
      EmberObject.create({
        value: 'foo'
      })
    )

    this.set('config', {})

    await render(
      hbs`{{camac-input-text config=config model=model readonly=true}}`
    )

    assert.dom('input[type=text]:disabled').exists()
  })

  test('it can change the value', async function(assert) {
    assert.expect(1)

    this.set(
      'model',
      EmberObject.create({
        value: 'foo'
      })
    )

    this.set('config', {})

    await render(
      hbs`{{camac-input-text config=config model=model on-change=(action (mut model.value))}}`
    )

    await fillIn('input[type=text]', 'bar')

    assert.equal(this.get('model.value'), 'bar')
  })
})
