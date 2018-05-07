import { module, test } from 'qunit'
import { setupTest } from 'ember-qunit'
import setupMirage from 'ember-cli-mirage/test-support/setup-mirage'

module('Unit | Service | question-store', function(hooks) {
  setupTest(hooks)
  setupMirage(hooks)

  hooks.beforeEach(function() {
    let { id } = this.server.create('instance')

    this.instanceId = id

    this.server.get('/api/v1/form-config', () => ({
      questions: {}
    }))
  })

  test('can build a question', async function(assert) {
    assert.expect(5)

    let service = this.owner.lookup('service:question-store')

    this.server.get('/api/v1/form-fields', () => {
      assert.step('backend-call')

      return { data: [] }
    })

    let question = await service._buildQuestion('test', this.instanceId)

    assert.ok(question.get('name'))
    assert.ok(question.get('field'))
    assert.ok(question.get('model'))

    assert.verifySteps(['backend-call'])
  })

  test('can find a question', async function(assert) {
    assert.expect(1)

    let service = this.owner.lookup('service:question-store')

    let question = await service.get('find').perform('test', this.instanceId)

    assert.equal(question.get('name'), 'test')
  })

  test('can find a set of questions', async function(assert) {
    assert.expect(2)

    let service = this.owner.lookup('service:question-store')

    let [test1, test2] = await service
      .get('findSet')
      .perform(['test1', 'test2'], this.instanceId)

    assert.equal(test1.get('name'), 'test1')
    assert.equal(test2.get('name'), 'test2')
  })

  test('can validate question', async function(assert) {
    assert.expect(2)

    this.server.get('/api/v1/form-config', () => ({
      questions: {
        test1: {
          type: 'text',
          required: true
        },
        test2: {
          type: 'text',
          required: true
        }
      }
    }))

    let service = this.owner.lookup('service:question-store')

    let validations = {
      test1(_, value) {
        return `${value} is an invalid value!`
      },
      test2(_, value) {
        return value === 'somevalue'
      }
    }

    service.set('_validations', validations)

    let test1 = await service.get('find').perform('test1', this.instanceId)
    let test2 = await service.get('find').perform('test2', this.instanceId)

    test1.set('model.value', 'somevalue')
    test2.set('model.value', 'somevalue')

    assert.equal(test1.validate(), 'somevalue is an invalid value!')
    assert.equal(test2.validate(), true)
  })

  test('can handle active expressions', async function(assert) {
    assert.expect(3)

    this.server.get('/api/v1/form-config', {
      questions: {
        test: {
          'active-expression': "'foo'|value in [1,2] || !('bar'|value > 2)"
        }
      }
    })

    let service = this.owner.lookup('service:question-store')

    let test = await service.get('find').perform('test', this.instanceId)
    let foo = await service.get('find').perform('foo', this.instanceId)
    let bar = await service.get('find').perform('bar', this.instanceId)

    foo.set('model.value', 3)
    bar.set('model.value', 3)
    await test.get('_hiddenTask').perform()
    assert.equal(
      test.get('hidden'),
      true,
      'The values of foo (3) AND bar (3) do not meet the expression'
    )

    foo.set('model.value', 2)
    await test.get('_hiddenTask').perform()
    assert.equal(
      test.get('hidden'),
      false,
      'The values of foo (2) meets the expression but bar (1) does not'
    )

    bar.set('model.value', 1)
    await test.get('_hiddenTask').perform()
    assert.equal(
      test.get('hidden'),
      false,
      'The values of foo (3) AND bar (1) meet the expression'
    )
  })

  test('can save a question', async function(assert) {
    assert.expect(6)

    this.server.get('/api/v1/form-config', {
      questions: {
        test: {
          type: 'number',
          required: true
        }
      }
    })

    let service = this.owner.lookup('service:question-store')

    let question = await service.get('find').perform('test', 1)

    assert.deepEqual(await service.get('saveQuestion').perform(question), [
      'Diese Frage darf nicht leer gelassen werden'
    ])
    assert.equal(question.get('model.isNew'), true)

    question.set('model.value', 'test')
    assert.deepEqual(await service.get('saveQuestion').perform(question), [
      'Der Wert muss eine Zahl sein'
    ])
    assert.equal(question.get('model.isNew'), true)

    question.set('model.value', 5)
    assert.deepEqual(await service.get('saveQuestion').perform(question), null)
    assert.equal(question.get('model.isNew'), false)
  })
})
