import Component from '@ember/component'
import { inject as service } from '@ember/service'
import { computed } from '@ember/object'
import { task, timeout } from 'ember-concurrency'

const CamacInputComponent = Component.extend({
  classNames: ['uk-margin'],

  identifier: null,

  instance: null,

  questionStore: service('question-store'),

  question: computed('identifier', function() {
    return this.get('questionStore').find(
      this.get('identifier'),
      this.get('instance.id')
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

    let valid = q.validate(value)

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
