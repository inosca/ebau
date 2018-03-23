import { module, test } from 'qunit'
import { setupRenderingTest } from 'ember-qunit'
import { render, pauseTest } from '@ember/test-helpers'
import hbs from 'htmlbars-inline-precompile'
import setupMirage from 'ember-cli-mirage/test-support/setup-mirage'

module('Integration | Component | camac-table', function(hooks) {
  setupRenderingTest(hooks)
  setupMirage(hooks)

  test('it renders', async function(assert) {
    assert.expect(5)

    this.server.get('/api/v1/form-config', () => {
      return {
        test: {
          label: 'only for testing',
          required: 'true',
          type: 'table',
          config: {
            fields: [
              { name: 'f1', label: 'field 1', type: 'text', config: {} },
              { name: 'f2', label: 'field 2', type: 'number', config: {} },
              {
                name: 'f3',
                label: 'field 3',
                type: 'radio',
                config: { options: ['1', '2', '3'] }
              },
              {
                name: 'f4',
                label: 'field 4',
                type: 'checkbox',
                config: { options: ['1', '2', '3'] }
              },
              {
                name: 'f5',
                label: 'field 5',
                type: 'select',
                config: { options: ['1', '2', '3'] }
              },
              {
                name: 'f6',
                label: 'field 6',
                type: 'multiselect',
                config: { options: ['1', '2', '3'] }
              }
            ]
          }
        }
      }
    })

    this.server.get('/api/v1/form-fields', (_, { queryParams: { name } }) => {
      return {
        data: {
          name,
          value: {
            value: [
              {
                f1: 'test',
                f2: 'test',
                f3: '1',
                f4: ['1', '2'],
                f5: '1',
                f6: ['1', '2']
              }
            ]
          }
        }
      }
    })

    await render(hbs`{{camac-table 'test'}}`)

    assert.dom('table').exists()
    assert.dom('tr').exists({ count: 1 })
  })
})
