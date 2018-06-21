import { module, test } from 'qunit'
import { setupRenderingTest } from 'ember-qunit'
import { render } from '@ember/test-helpers'
import hbs from 'htmlbars-inline-precompile'

module('Integration | Component | camac-hint-dialog', function(hooks) {
  setupRenderingTest(hooks)

  test('it renders', async function(assert) {
    assert.expect(4)

    await render(hbs`
      <div id="modal-container"></div>
      {{camac-hint-dialog '**bold**, *italic*'}}
    `)

    assert.dom('span[uk-icon]').exists()

    assert.dom('#modal-container .uk-modal-body p').hasText('bold, italic')
    assert.dom('#modal-container .uk-modal-body p > strong').hasText('bold')
    assert.dom('#modal-container .uk-modal-body p > em').hasText('italic')
  })

  test('it renders in block style', async function(assert) {
    assert.expect(3)

    await render(hbs`
      <div id="modal-container"></div>
      {{#camac-hint-dialog ''}}<span id="test">test</span>{{/camac-hint-dialog}}
    `)

    assert.dom('span[uk-icon]').doesNotExist()
    assert.dom('#test').hasText('test')

    assert.dom('#modal-container .uk-modal-body').exists()
  })
})
