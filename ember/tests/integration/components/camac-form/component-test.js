import { module, test } from 'qunit'
import { setupRenderingTest } from 'ember-qunit'
import { render } from '@ember/test-helpers'
import hbs from 'htmlbars-inline-precompile'
import setupMirage from 'ember-cli-mirage/test-support/setup-mirage'

module('Integration | Component | camac-form', function(hooks) {
  setupRenderingTest(hooks)
  setupMirage(hooks)

  hooks.beforeEach(function() {
    this.server.get('/api/v1/form-config', {
      'test-input': {
        label: 'Test input',
        required: true,
        type: 'text',
        config: {}
      },
      'test-table': {
        label: 'Test table',
        required: true,
        type: 'table',
        config: {
          fields: [
            {
              name: 'test-input-in-table',
              title: 'Test input in a table',
              type: 'number',
              required: true,
              config: {}
            }
          ]
        }
      }
    })
  })

  test('it renders', async function(assert) {
    assert.expect(4)

    await render(hbs`
      {{#camac-form instance=(hash id=1) readonly=false as |form|}}
        {{form.input 'test-input'}}
        {{form.table 'test-table'}}
      {{/camac-form}}
    `)

    assert.dom('form').exists()
    assert.dom('input').exists()
    assert.dom('table').exists()
    assert.dom('tfoot').exists()
  })

  test('it renders in readonly mode', async function(assert) {
    assert.expect(4)

    await render(hbs`
      {{#camac-form instance=(hash id=1) readonly=true as |form|}}
        {{form.input 'test-input'}}
        {{form.table 'test-table'}}
      {{/camac-form}}
    `)

    assert.dom('form').exists()
    assert.dom('input:disabled').exists()
    assert.dom('table').exists()
    assert.dom('tfoot').doesNotExist()
  })
})
