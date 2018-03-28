import { module, test } from 'qunit'
import { setupTest } from 'ember-qunit'
import setupMirage from 'ember-cli-mirage/test-support/setup-mirage'

module('Unit | Service | question-store', function(hooks) {
  setupTest(hooks)
  setupMirage(hooks)

  hooks.beforeEach(function() {
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

    let question = await service._buildQuestion('test', 1)

    assert.ok(question.get('name'))
    assert.ok(question.get('field'))
    assert.ok(question.get('model'))

    assert.verifySteps(['backend-call'])
  })

  test('can find a question', async function(assert) {
    assert.expect(1)

    let service = this.owner.lookup('service:question-store')

    let question = await service.get('find').perform('test', 1)

    assert.equal(question.get('name'), 'test')
  })

  test('can find a set of questions', async function(assert) {
    assert.expect(2)

    let service = this.owner.lookup('service:question-store')

    let [test1, test2] = await service
      .get('findSet')
      .perform(['test1', 'test2'], 1)

    assert.equal(test1.get('name'), 'test1')
    assert.equal(test2.get('name'), 'test2')
  })

  test('can validate question', async function(assert) {
    assert.expect(2)

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

    let test1 = await service.get('find').perform('test1', 1)
    let test2 = await service.get('find').perform('test2', 1)

    test1.set('model.value', 'somevalue')
    test2.set('model.value', 'somevalue')

    assert.equal(test1.validate(), 'somevalue is an invalid value!')
    assert.equal(test2.validate(), true)
  })

  test('can compute if question is hidden', async function(assert) {
    assert.expect(5)

    let service = this.owner.lookup('service:question-store')

    this.server.get('/api/v1/form-config', () => ({
      questions: {
        test1: {
          'active-condition': [
            {
              question: 'test2',
              value: {
                in: ['yeah!']
              }
            }
          ]
        },
        test2: {
          'active-condition': [
            {
              question: 'test1',
              value: {
                in: ['yeah!']
              }
            }
          ]
        },
        test3: {
          'active-condition': []
        },
        test4: {
          'active-condition': [
            {
              question: 'test1',
              value: {
                in: ['yeah!']
              }
            },
            {
              question: 'test2',
              value: {
                in: ['yeah!']
              }
            }
          ]
        }
      }
    }))

    let test1 = await service.get('find').perform('test1', 1)
    let test2 = await service.get('find').perform('test2', 1)
    let test3 = await service.get('find').perform('test3', 1)
    let test4 = await service.get('find').perform('test4', 1)

    test1.set('model.value', 'yeah!')
    test2.set('model.value', 'nooo!')

    assert.equal(
      await test1.get('hidden'),
      true,
      'The value of test2 is nooo! which does not meet the condition'
    )
    assert.equal(
      await test2.get('hidden'),
      false,
      'The value of test1 is yeah! which meets the condition'
    )
    assert.equal(
      await test3.get('hidden'),
      false,
      'If no condition is set, it is never hidden'
    )
    assert.equal(
      await test4.get('hidden'),
      true,
      'The values of test1 AND test2 do not meet the condition'
    )
    test2.set('model.value', 'yeah!')
    assert.equal(
      await test4.get('hidden'),
      false,
      'The values of test1 AND test2 meet the condition'
    )
  })
})
