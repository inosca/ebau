import Service, { inject as service } from '@ember/service'
import EmberObject, { computed, getWithDefault } from '@ember/object'
import { reads } from '@ember/object/computed'
import ObjectProxy from '@ember/object/proxy'
import PromiseProxyMixin from '@ember/object/promise-proxy-mixin'
import _conditions from 'citizen-portal/questions/conditions'
import _validations from 'citizen-portal/questions/validations'
import { getOwner } from '@ember/application'
import { A } from '@ember/array'
import { Promise, resolve } from 'rsvp'

const ObjectPromiseProxy = ObjectProxy.extend(PromiseProxyMixin)

const Question = EmberObject.extend({
  _questions: service('question-store'),

  name: null,
  field: null,
  model: null,

  value: reads('model.value'),

  validate(value) {
    let validationFn = getWithDefault(
      this.get('_questions._validations'),
      this.get('name'),
      () => true
    )

    return validationFn(this.get('field'), value)
  },

  hidden: computed('_questions._store.@each.value', async function() {
    let conditionFn = getWithDefault(
      this.get('_questions._conditions'),
      this.get('name'),
      () => true
    )

    let findFn = name => {
      // Use the question stores find function to find another question of the same instance
      return this.get('_questions').find(name, this.get('model.instance.id'))
    }

    return !await conditionFn(findFn)
  })
})

export default Service.extend({
  _validations,
  _conditions,

  ajax: service(),
  store: service(),

  init() {
    this._super(...arguments)

    this.set('_store', A())
  },

  _formConfig: computed(function() {
    return this.get('ajax').request('/api/v1/form-config')
  }),

  async _buildQuestion(name, instance) {
    let query = await this.get('store').query('form-field', {
      instance,
      name
    })

    // Get the already saved record or create a new record
    let model = query.getWithDefault(
      'firstObject',
      this.get('store').createRecord('form-field', {
        name,
        instance
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

  /**
   * Find a question by a given name and instance id.
   *
   * This checks if the question is already in the internal store and return it
   * instantly if so. If not, it will resolve as soon as the question object is
   * created.
   *
   * @param {String} name The name of the question
   * @param {Number} instance The ID of the instance for the question
   * @return {Object} The asked question
   */
  find(name, instance) {
    let stored = this.get('_store').find(
      q => q.get('name') === name && q.get('model.instance.id') === instance
    )

    return ObjectPromiseProxy.create({
      promise: stored
        ? resolve(stored)
        : new Promise(resolve => {
            this._buildQuestion(name, instance).then(q => {
              this.get('_store').pushObject(q)

              resolve(q)
            })
          })
    })
  }
})
