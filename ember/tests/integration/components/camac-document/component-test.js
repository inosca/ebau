import { module, test } from 'qunit'
import { setupRenderingTest } from 'ember-qunit'
import { render, find, triggerEvent, click } from '@ember/test-helpers'
import hbs from 'htmlbars-inline-precompile'
import setupMirage from 'ember-cli-mirage/test-support/setup-mirage'
import loadQuestions from 'citizen-portal/tests/helpers/load-questions'

module('Integration | Component | camac-document', function(hooks) {
  setupRenderingTest(hooks)
  setupMirage(hooks)

  hooks.beforeEach(async function() {
    let instance = this.server.create('instance')

    this.set('instance', instance)

    this.server.create('attachment', {
      name: 'test-document',
      instance
    })

    this.server.get('/api/v1/form-config', () => {
      return {
        questions: {
          'test-document': {
            label: 'Test Doc',
            hint: 'Hint hint hint',
            type: 'document',
            required: true,
            config: {}
          }
        }
      }
    })

    await loadQuestions(['test-document'], instance.id)
  })

  test('it renders', async function(assert) {
    assert.expect(2)

    await render(hbs`{{camac-document 'test-document' instance=instance}}`)

    assert.dom('.uk-text-center').hasText('Test Doc *')
    assert.dom('span[uk-icon]').hasAttribute('uk-tooltip', 'Hint hint hint')
  })

  test('it can upload a document', async function(assert) {
    assert.expect(2)

    this.server.post('/api/v1/attachments', ({ attachments }) => {
      assert.step('upload-document')

      return attachments.first()
    })

    await render(hbs`{{camac-document 'test-document'instance=instance}}`)

    let files = [new File([new Blob()], 'testfile.png', { type: 'image/png' })]
    let input = await find('input[type=file')

    input.files.item = i => {
      return files[i]
    }

    await triggerEvent('input[type=file]', 'change')

    assert.verifySteps(['upload-document'])
  })

  test('it can download a document', async function(assert) {
    assert.expect(2)

    this.server.get('/api/v1/attachments/:id/files/:name', () => {
      assert.step('download-document')

      return new Blob()
    })

    await render(hbs`{{camac-document 'test-document'instance=instance}}`)

    await click('[data-test-download-document]')

    assert.verifySteps(['download-document'])
  })
})
