import { module, test } from 'qunit'
import { setupRenderingTest } from 'ember-qunit'
import { render } from '@ember/test-helpers'
import hbs from 'htmlbars-inline-precompile'

module('Integration | Helper | format-date', function(hooks) {
  setupRenderingTest(hooks)

  test('it formats the date correctly', async function(assert) {
    this.set('date', new Date(2018, 3, 19, 9, 50))

    await render(hbs`{{format-date date}}`)

    assert.dom(this.element).hasText('19.03.2018 09:50')
  })

  test('it zeropads the parts correctly', async function(assert) {
    this.set('date', new Date(2018, 1, 1, 1, 1))

    await render(hbs`{{format-date date}}`)

    assert.dom(this.element).hasText('01.01.2018 01:01')
  })
})
