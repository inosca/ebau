import Controller from '@ember/controller'
import { task } from 'ember-concurrency'
import { computed } from '@ember/object'

export default Controller.extend({
  forms: computed(function() {
    return this.store.peekAll('form')
  }),

  save: task(function*() {
    let model = this.get('model')

    yield model.save()

    yield this.transitionToRoute('instances.edit', model.id)
  })
})
