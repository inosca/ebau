import { module, test } from 'qunit'
import { setupTest } from 'ember-qunit'
import setupMirage from 'ember-cli-mirage/test-support/setup-mirage'

module('Unit | Controller | instances/edit/submit', function(hooks) {
  setupTest(hooks)
  setupMirage(hooks)

  hooks.beforeEach(function() {
    let form = this.server.create('form', { name: 'test' })

    this.instance = this.server.create('instance', {
      formId: form.id
    })

    this.model = { instance: this.instance, meta: { editable: ['form'] } }

    this.router = { urlFor: () => true }

    this.server.get('/api/v1/form-config', () => ({
      forms: {
        test: ['module']
      },
      modules: {
        module: {
          questions: ['question-1', 'question-2', 'question-3']
        }
      },
      questions: {
        'question-1': {
          type: 'text',
          required: true,
          'active-condition': []
        },
        'question-2': {
          type: 'text',
          required: true,
          'active-condition': []
        },
        'question-3': {
          type: 'text',
          required: true,
          'active-condition': []
        }
      }
    }))
  })

  test('it computes if the instance can be submitted', async function(assert) {
    assert.expect(2)

    let editController = this.owner.lookup('controller:instances/edit')
    let controller = this.owner.lookup('controller:instances/edit/submit')
    let store = this.owner.lookup('service:question-store')

    editController.setProperties({ model: this.model, router: this.router })
    controller.setProperties({ model: this.model, router: this.router })

    let q1 = await store.get('find').perform('question-1', this.instance.id)
    let q2 = await store.get('find').perform('question-2', this.instance.id)
    let q3 = await store.get('find').perform('question-3', this.instance.id)

    assert.equal(await controller.get('canSubmit'), false)

    q1.set('model.value', 'test')
    q2.set('model.value', 'test')
    q3.set('model.value', 'test')

    await q1.get('model').save()
    await q2.get('model').save()
    await q3.get('model').save()

    controller.notifyPropertyChange('canSubmit')

    assert.equal(await controller.get('canSubmit'), true)
  })
})
