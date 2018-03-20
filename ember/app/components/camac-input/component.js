import Component from '@ember/component'
import { inject as service } from '@ember/service'
import { computed } from '@ember/object'
import { task, timeout } from 'ember-concurrency'

const CamacInputComponent = Component.extend({
  classNames: ['uk-margin'],

  identifier: null,

  instance: null,

  error: null,

  questionStore: service('question-store'),

  question: computed('identifier', function() {
    return this.get('questionStore.find').perform(
      this.get('identifier'),
      this.get('instance.id')
    )
  }),

  save: task(function*(value) {
    yield timeout(500)

    let q = yield this.get('question')

    let model = q.get('model')

    model.set('value', value)

    let valid = q.validate()

    if (valid === true) {
      this.set('error', null)

      yield model.save()
    } else {
      this.set('error', valid)
    }
  }).restartable()
})

CamacInputComponent.reopenClass({
  positionalParams: ['identifier']
})

export default CamacInputComponent
