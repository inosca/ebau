import Service, { inject as service } from '@ember/service'
import EmberObject, { computed, getWithDefault } from '@ember/object'
import { reads } from '@ember/object/computed'
import _conditions from 'citizen-portal/questions/conditions'
import _validations from 'citizen-portal/questions/validations'
import { getOwner } from '@ember/application'
import { A } from '@ember/array'
import { all } from 'rsvp'
import { task, taskGroup } from 'ember-concurrency'

const Question = EmberObject.extend({
  _questions: service('question-store'),

  name: null,
  field: null,
  model: null,

  value: reads('model.value'),
  isNew: reads('model.isNew'),

  validate() {
    let validationFn = getWithDefault(
      this.get('_questions._validations'),
      this.get('name'),
      () => true
    )

    return validationFn(this.get('field'), this.get('value'))
  },

  hidden: computed('_questions._store.@each.value', async function() {
    let conditionFn = getWithDefault(
      this.get('_questions._conditions'),
      this.get('name'),
      async () => true
    )

    let findFn = name => {
      // Use the question stores find function to find another question of the same instance
      return this.get('_questions.find').perform(
        name,
        this.get('model.instance.id')
      )
    }

    return !await conditionFn(findFn)
  })
})

export default Service.extend({
  _validations,
  _conditions,

  ajax: service(),
  store: service(),

  build: taskGroup().enqueue(),

  init() {
    this._super(...arguments)

    this.set('_store', A())
  },

  _formConfig: computed(function() {
    return this.get('ajax').request('/api/v1/form-config')
  }),

  async _buildQuestion(name, instance, query = null) {
    if (!query) {
      query = await this.get('store').query('form-field', {
        instance,
        name
      })
    }

    // Get the already saved record or create a new record
    let model = query.getWithDefault(
      'firstObject',
      this.get('store').createRecord('form-field', {
        name,
        instance: this.get('store').peekRecord('instance', instance)
      })
    )

    return Question.create({
      // We need to pass the container of the current service to the question
      // object, to allow it to inject other services, since you can not inject
      // services without container context
      container: getOwner(this).__container__,

      name,
      model,
      field: getWithDefault(await this.get('_formConfig'), name, {})
    })
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

  peek(name, instance) {
    return this.get('_store').find(
      q => q.get('name') === name && q.get('model.instance.id') === instance
    )
  },

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
        let q = await this._buildQuestion(name, instance, query)

        this.get('_store').pushObject(q)

        return q
      })
    )

    return [...fetched, ...cached]
  }).group('build')
})
