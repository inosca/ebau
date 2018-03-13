import Service from '@ember/service'
import { inject as service } from '@ember/service'
import EmberObject, { computed, getWithDefault } from '@ember/object'
import { reads } from '@ember/object/computed'
import validations from 'citizen-portal/data/validations'

export default Service.extend({
  ajax: service(),
  store: service(),

  questions: computed(async function() {
    return await this.get('ajax').request('/api/v1/form-config')
  }),

  async getQuestion(identifier, instance) {
    let questions = await this.get('questions')
    let query = await this.get('store').query('form-field', {
      instance: instance.id,
      name: identifier
    })

    let model = query.getWithDefault(
      'firstObject',
      this.get('store').createRecord('form-field', {
        name: identifier,
        instance
      })
    )

    return EmberObject.create({
      identifier,
      model,
      ...getWithDefault(questions, identifier, {}),
      validate(value) {
        let fn = getWithDefault(validations, identifier, () => true)

        return fn(this, value)
      }
    })
  }
})
