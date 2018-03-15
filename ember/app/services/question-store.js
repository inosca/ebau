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

  value: reads('model.value'),

  _validations,
  _conditions,

  validate(value) {
    return getWithDefault(
      this.get('_questions._validations'),
      this.get('name'),
      () => true
    )(this.get('field'), value)
  },

  hidden: computed('_questions._store.@each.value', async function() {
    return !await getWithDefault(
      this.get('_questions._conditions'),
      this.get('name'),
      () => true
    )(name => this.get('_questions').find(name, this.get('model.instance.id')))
  })
})

export default Service.extend({
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
    let config = await this.get('_formConfig')

    let query = await this.get('store').query('form-field', {
      instance,
      name
    })

    let model = query.getWithDefault(
      'firstObject',
      this.get('store').createRecord('form-field', {
        name,
        instance
      })
    )

    return Question.create({
      container: getOwner(this).__container__,

      name,
      field: getWithDefault(config, name, {}),
      model
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
