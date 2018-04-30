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

  test('can handle empty active conditions', async function(assert) {
    assert.expect(1)

    this.server.get('/api/v1/form-config', {
      questions: {
        test: {
          'active-condition': []
        }
      }
    })
    let service = this.owner.lookup('service:question-store')

    let test = await service.get('find').perform('test', this.instanceId)

    assert.equal(
      await test.get('hidden'),
      false,
      'Empty active conditions are never hidden'
    )
  })

  test('can handle contains-any active conditions', async function(assert) {
    assert.expect(2)

    this.server.get('/api/v1/form-config', {
      questions: {
        test: {
          'active-condition': [
            {
              question: 'foo',
              value: { 'contains-not-any': ['test'] }
            }
          ]
        }
      }
    })

    let service = this.owner.lookup('service:question-store')

    let test = await service.get('find').perform('test', this.instanceId)
    let foo = await service.get('find').perform('foo', this.instanceId)

    foo.set('model.value', 'test')
    assert.equal(
      await test.get('hidden'),
      true,
      'The value of foo (test) does not meet the condition'
    )

    foo.set('model.value', 'nottest')
    assert.equal(
      await test.get('hidden'),
      false,
      'The value of foo (nottest) meets the condition'
    )
  })

  test('can handle contains-not-any active conditions', async function(assert) {
    assert.expect(2)

    this.server.get('/api/v1/form-config', {
      questions: {
        test: {
          'active-condition': [
            {
              question: 'foo',
              value: { 'contains-any': ['test'] }
            }
          ]
        }
      }
    })

    let service = this.owner.lookup('service:question-store')

    let test = await service.get('find').perform('test', this.instanceId)
    let foo = await service.get('find').perform('foo', this.instanceId)

    foo.set('model.value', 'nottest')
    assert.equal(
      await test.get('hidden'),
      true,
      'The value of foo (nottest) does not meet the condition'
    )

    foo.set('model.value', 'test')
    assert.equal(
      await test.get('hidden'),
      false,
      'The value of foo (test) meets the condition'
    )
  })

  test('can handle greater-than active conditions', async function(assert) {
    assert.expect(2)

    this.server.get('/api/v1/form-config', {
      questions: {
        test: {
          'active-condition': [
            {
              question: 'foo',
              value: { 'greater-than': 5 }
            }
          ]
        }
      }
    })

    let service = this.owner.lookup('service:question-store')

    let test = await service.get('find').perform('test', this.instanceId)
    let foo = await service.get('find').perform('foo', this.instanceId)

    foo.set('model.value', 5)
    assert.equal(
      await test.get('hidden'),
      true,
      'The value of foo (5) does not meet the condition'
    )

    foo.set('model.value', 6)
    assert.equal(
      await test.get('hidden'),
      false,
      'The value of foo (6) meets the condition'
    )
  })

  test('can handle greater-than-equals active conditions', async function(assert) {
    assert.expect(2)

    this.server.get('/api/v1/form-config', {
      questions: {
        test: {
          'active-condition': [
            {
              question: 'foo',
              value: { 'greater-than-equals': 5 }
            }
          ]
        }
      }
    })

    let service = this.owner.lookup('service:question-store')

    let test = await service.get('find').perform('test', this.instanceId)
    let foo = await service.get('find').perform('foo', this.instanceId)

    foo.set('model.value', 4)
    assert.equal(
      await test.get('hidden'),
      true,
      'The value of foo (4) does not meet the condition'
    )

    foo.set('model.value', 5)
    assert.equal(
      await test.get('hidden'),
      false,
      'The value of foo (5) meets the condition'
    )
  })

  test('can handle lower-than active conditions', async function(assert) {
    assert.expect(2)

    this.server.get('/api/v1/form-config', {
      questions: {
        test: {
          'active-condition': [
            {
              question: 'foo',
              value: { 'lower-than': 5 }
            }
          ]
        }
      }
    })

    let service = this.owner.lookup('service:question-store')

    let test = await service.get('find').perform('test', this.instanceId)
    let foo = await service.get('find').perform('foo', this.instanceId)

    foo.set('model.value', 5)
    assert.equal(
      await test.get('hidden'),
      true,
      'The value of foo (5) does not meet the condition'
    )

    foo.set('model.value', 4)
    assert.equal(
      await test.get('hidden'),
      false,
      'The value of foo (4) meets the condition'
    )
  })

  test('can handle lower-than-equals active conditions', async function(assert) {
    assert.expect(2)

    this.server.get('/api/v1/form-config', {
      questions: {
        test: {
          'active-condition': [
            {
              question: 'foo',
              value: { 'lower-than-equals': 5 }
            }
          ]
        }
      }
    })

    let service = this.owner.lookup('service:question-store')

    let test = await service.get('find').perform('test', this.instanceId)
    let foo = await service.get('find').perform('foo', this.instanceId)

    foo.set('model.value', 6)
    assert.equal(
      await test.get('hidden'),
      true,
      'The value of foo (6) does not meet the condition'
    )

    foo.set('model.value', 5)
    assert.equal(
      await test.get('hidden'),
      false,
      'The value of foo (5) meets the condition'
    )
  })

  test('can handle single and multiple values for active conditions', async function(assert) {
    assert.expect(2)

    this.server.get('/api/v1/form-config', {
      questions: {
        test: {
          'active-condition': [
            {
              question: 'foo',
              value: { 'contains-any': ['test'] }
            }
          ]
        }
      }
    })

    let service = this.owner.lookup('service:question-store')

    let test = await service.get('find').perform('test', this.instanceId)
    let foo = await service.get('find').perform('foo', this.instanceId)

    foo.set('model.value', 'test')
    assert.equal(await test.get('hidden'), false, 'Can handle single values')

    foo.set('model.value', ['test'])
    assert.equal(await test.get('hidden'), false, 'Can handle multiple values')
  })

  test('can handle multiple active conditions', async function(assert) {
    assert.expect(3)

    this.server.get('/api/v1/form-config', {
      questions: {
        test: {
          'active-condition': [
            {
              question: 'foo',
              value: { 'contains-any': ['test'] }
            },
            {
              question: 'bar',
              value: { 'contains-not-any': ['test'] }
            }
          ]
        }
      }
    })

    let service = this.owner.lookup('service:question-store')

    let test = await service.get('find').perform('test', this.instanceId)
    let foo = await service.get('find').perform('foo', this.instanceId)
    let bar = await service.get('find').perform('bar', this.instanceId)

    foo.set('model.value', 'nottest')
    bar.set('model.value', 'test')
    assert.equal(
      await test.get('hidden'),
      true,
      'The values of foo (nottest) AND bar (test) do not meet the condition'
    )

    foo.set('model.value', 'test')
    assert.equal(
      await test.get('hidden'),
      true,
      'The values of foo (test) meets the condition but bar (test) does not'
    )

    bar.set('model.value', 'nottest')
    assert.equal(
      await test.get('hidden'),
      false,
      'The values of foo (test) AND bar (nottest) meet the condition'
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
