import Service, { inject as service } from '@ember/service'
import EmberObject, { computed, getWithDefault } from '@ember/object'
import { reads } from '@ember/object/computed'
import { getOwner } from '@ember/application'
import { A } from '@ember/array'
import { capitalize } from '@ember/string'
import { all } from 'rsvp'
import { task, taskGroup } from 'ember-concurrency'
import _validations from 'citizen-portal/questions/validations'
import { isArray } from '@ember/array'

const Question = EmberObject.extend({
  _questions: service('question-store'),

  name: null,
  field: null,
  model: null,

  value: reads('model.value'),
  isNew: reads('model.isNew'),

  validate() {
    let name = this.get('name')
    let { type, required: isRequired = false, config = {} } = this.get('field')

    let validations = [
      isRequired
        ? this.getWithDefault(
            '_questions._validations.validateRequired',
            () => true
          )
        : () => true,
      this.getWithDefault(
        `_questions._validations.validate${capitalize(type)}`,
        () => true
      ),
      this.getWithDefault(`_questions._validations.${name}`, () => true)
    ]

    let isValid = validations.map(fn => fn(config, this.get('value')))

    return (
      isValid.every(v => v === true) ||
      isValid.filter(v => typeof v === 'string')
    )
  },

  hidden: computed('_questions._store.@each.value', async function() {
    let conditions = this.getWithDefault('field.active-condition', [])

    let conditionResults = await all(
      conditions.map(
        async ({ question, value: { 'contains-any': possibleValues } }) => {
          let value = (await this.get('_questions.find').perform(
            question,
            this.get('model.instance.id')
          )).get('value')

          return possibleValues.some(v =>
            (isArray(value) ? value : [value]).includes(v)
          )
        }
      )
    )

    return !conditionResults.every(Boolean)
  })
})

export default Service.extend({
  _validations,

  ajax: service(),
  store: service(),

  build: taskGroup().enqueue(),

  init() {
    this._super(...arguments)

    this.set('_store', A())
  },

  config: computed(async function() {
    return await this.get('ajax').request('/api/v1/form-config')
  }),

  async _buildQuestion(name, instance, query = null) {
    if (!query) {
      query = await this.get('store').query('form-field', {
        instance,
        name
      })
    }

    // Get the already saved record or create a new record
    let model = query.get('firstObject')

    if (!model) {
      model = this.get('store').createRecord('form-field', {
        name,
        instance:
          this.get('store').peekRecord('instance', instance) ||
          (await this.get('store').findRecord('instance', instance))
      })
    }

    return Question.create({
      // We need to pass the container of the current service to the question
      // object, to allow it to inject other services, since you can not inject
      // services without container context
      container: getOwner(this).__container__,

      name,
      model,
      field: getWithDefault(await this.get('config'), `questions.${name}`, {})
    })
  },

  peek(name, instance) {
    return this.get('_store').find(
      q => q.get('name') === name && q.get('model.instance.id') === instance
    )
  },

  find: task(function*(name, instance) {
    let cached = this.peek(name, instance)

    if (cached) {
      return cached
    }

    let q = yield this._buildQuestion(name, instance)

    this.get('_store').pushObject(q)

    return q
  }).group('build'),

  peekSet(names, instance) {
    return this.get('_store').filter(
      q =>
        names.includes(q.get('name')) && q.get('model.instance.id') === instance
    )
  },

  findSet: task(function*(names, instance) {
    let cached = this.peekSet(names, instance)

    let cachedNames = cached.map(({ name }) => name)
    let fetchedNames = names.filter(n => !cachedNames.includes(n))

    let query = fetchedNames.length
      ? yield this.get('store').query('form-field', {
          instance,
          name: names.join(',')
        })
      : null

    let fetched = yield all(
      fetchedNames.map(async name => {
        let q = await this._buildQuestion(
          name,
          instance,
          query.filter(
            q => q.get('name') === name && q.get('instance.id') === instance
          )
        )

        this.get('_store').pushObject(q)

        return q
      })
    )

    return [...fetched, ...cached]
  }).group('build')
})
