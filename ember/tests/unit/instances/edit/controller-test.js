import { module, test } from 'qunit'
import { setupTest } from 'ember-qunit'
import setupMirage from 'ember-cli-mirage/test-support/setup-mirage'

module('Unit | Controller | instances/edit', function(hooks) {
  setupTest(hooks)
  setupMirage(hooks)

  hooks.beforeEach(function() {
    let form = server.create('form', { name: 'test' })

    this.model = server.create('instance', { formId: form.id })
    this.router = { urlFor: () => true }

    this.server.get('/api/v1/form-config', () => ({
      forms: {
        test: [
          'module1',
          'module1.test1',
          'module1.test2',
          'module2',
          'module2.test1',
          'module2.test2',
          'module3'
        ]
      },
      modules: {
        module1: { title: 'Module 1', parent: null, questions: [] },
        'module1.test1': {
          title: 'Module 1: Test 1',
          parent: 'module1',
          questions: []
        },
        'module1.test2': {
          title: 'Module 1: Test 2',
          parent: 'module1',
          questions: ['test-question-1']
        },
        module2: {
          title: 'Module 2',
          parent: null,
          questions: ['test-question-2']
        },
        'module2.test1': {
          title: 'Module 2: Test 1',
          parent: 'module2',
          questions: ['test-question-3']
        },
        'module2.test2': {
          title: 'Module 2: Test 2',
          parent: 'module2',
          questions: ['test-question-4']
        },
        module3: {
          title: 'Module 3',
          parent: null,
          questions: []
        }
      },
      questions: {
        'test-question-1': { required: true, 'active-condition': [] },
        'test-question-2': { required: true, 'active-condition': [] },
        'test-question-3': { required: true, 'active-condition': [] },
        'test-question-4': { required: true, 'active-condition': [] }
      }
    }))
  })

  test('it computes the modules', async function(assert) {
    assert.expect(1)

    let controller = this.owner.lookup('controller:instances/edit')

    controller.set('model', this.model)
    controller.set('router', this.router)

    let modules = await controller.get('modules')

    assert.equal(modules.length, 7)
  })

  test('it computes the active links', async function(assert) {
    assert.expect(1)

    let controller = this.owner.lookup('controller:instances/edit')

    controller.set('model', this.model)
    controller.set('router', this.router)

    let links = await controller.get('links')

    assert.deepEqual(links, [
      'instances.edit', // landing page
      'instances.edit.module1.test2',
      'instances.edit.module2',
      'instances.edit.module2.test1',
      'instances.edit.module2.test2',
      'instances.edit.submit' // submit page
    ])
  })

  test('it computes a hierarchical navigation', async function(assert) {
    assert.expect(5)

    let controller = this.owner.lookup('controller:instances/edit')

    controller.set('model', this.model)
    controller.set('router', this.router)

    let navigation = await controller.get('navigation')

    assert.equal(navigation.length, 3)
    assert.deepEqual(navigation.map(({ name }) => name), [
      'module1',
      'module2',
      'module3'
    ])

    assert.deepEqual(navigation[0].submodules.map(({ name }) => name), [
      'module1.test1',
      'module1.test2'
    ])
    assert.deepEqual(navigation[1].submodules.map(({ name }) => name), [
      'module2.test1',
      'module2.test2'
    ])
    assert.deepEqual(navigation[2].submodules.map(({ name }) => name), [])
  })
})
