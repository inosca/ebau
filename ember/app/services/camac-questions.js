import Service from '@ember/service'
import { inject as service } from '@ember/service'
import EmberObject, { computed, getWithDefault } from '@ember/object'
import { reads } from '@ember/object/computed'
import validations from 'citizen-portal/questions/validations'
import conditions from 'citizen-portal/questions/conditions'
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

    let question = getWithDefault(questions, identifier, {})

    let Question = EmberObject.extend({
      display: computed('instance.formFields.@each.value', function() {
        let fn = getWithDefault(conditions, identifier, () => true)

        let findQuestion = name => getWithDefault(questions, name, {})

        let findValue = name => {
          let ff = this.get('instance.formFields').findBy('name', name)

          return (ff && ff.get('value') && ff.get('value')) || null
        }

        return fn(findQuestion, findValue)
      }),
      validate(value) {
        let fn = getWithDefault(validations, identifier, () => true)

        return fn(this, value)
      }
    })

    return Question.create({
      validations,
      identifier,
      instance,
      model,
      ...question
    })
  }
})
