import Service from '@ember/service'
import { inject as service } from '@ember/service'
import EmberObject, { computed, getWithDefault } from '@ember/object'
import { reads } from '@ember/object/computed'
import validations from 'citizen-portal/data/validations'
import fetch from 'fetch'

export default Service.extend({
  session: service(),
  store: service(),

  token: reads('session.data.authenticated.token'),

  questions: computed(async function() {
    return await fetch(`/api/v1/form-config`, {
      headers: {
        Authorization: `JWT ${this.get('token')}`
      }
    }).then(response => {
      return response.json()
    })
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
