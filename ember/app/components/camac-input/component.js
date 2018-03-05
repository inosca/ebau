import Component from '@ember/component'
import { inject as service } from '@ember/service'
import { computed } from '@ember/object'
import { task, timeout } from 'ember-concurrency'
import textSerializer from 'citizen-portal/components/camac-input-text/serializer'
import selectSerializer from 'citizen-portal/components/camac-input-select/serializer'

const serializerMap = {
  text: textSerializer,
  select: selectSerializer
}

const CamacInputComponent = Component.extend({
  classNames: ['uk-margin'],

  identifier: null,

  instance: null,

  questions: service('camac-questions'),

  question: computed('identifier', 'questions.questions.[]', async function() {
    return await this.get('questions').getQuestion(
      this.get('identifier'),
      this.get('instance')
    )
  }),

  error: computed('save.last.value', function() {
    let saveVal = this.get('save.last.value')

    if (saveVal === undefined) {
      return null
    }

    return saveVal === true ? false : saveVal
  }),

  save: task(function*(value) {
    yield timeout(500)

    let q = yield this.get('question')

    let valid = q.validate(serializerMap[q.get('type')].deserialize(value))

    if (valid === true) {
      let model = q.get('model')

      model.set('value', value)

      yield model.save()
    }

    return valid
  }).restartable()
})

CamacInputComponent.reopenClass({
  positionalParams: ['identifier']
})

export default CamacInputComponent
